"""
:copyright: 2019 Geophysics Labs
:author: Joseph Barraud
:license: BSD License
"""
# import system modules
import os, argparse, re

# import numpy
import numpy as np

# import obspy
from obspy.io.segy.segy import _read_segy

# import local modules
from segy_io import loadSHandSTH
from spatial import projectPoints

# 
from pathlib import Path

# coordinate positions in SEGY (lookup dictionary)
coordKeys = {
    'source': ['source_coordinate_x', 'source_coordinate_y'],
    'group': ['group_coordinate_x', 'group_coordinate_y'],
    'cdp': ['x_coordinate_of_ensemble_position_of_this_trace', 'y_coordinate_of_ensemble_position_of_this_trace']
}


#==============================================================================
# convertScaler
#==============================================================================
def convertScaler(scaler, toRead=True):
    '''
    Convert scaler header in SEGY file to a multiplicative coefficient to be
    applied to coordinates.
    With option toRead True, the function returns a scaler for converting
    coordinates from a SEGY, while if False, the function returns a scaler to
    write coordinates to SEGY file.
    The converted scaler must be used as a multiplicator.
    The scaler is normally defined in the trace header of the SEGY file at
    position 71 ("scalar_to_be_applied_to_all_coordinates").
    The function works for both scalars and vectors.

    Usage
    -----
    The convention in SEGY files is that if the header is negative then it is
    applied as a multiplicator to the coordinates. For example, a scaler of -100
    transforms metres to centimetres. So when reading coordinates from a file,
    the coordinates must be divided by the absolute value of the scaler. It is
    the reverse when the scaler is positive.
    In both cases (reading or writing) the coefficients returned by the function
    must be multiplied by the coordinates.
    '''
    if np.any(scaler == 0):  # some SEGY files lack a proper definition of the scaler
        XYscale = 1.
    elif np.any(scaler < 0):  # Positive scaler is multiplier, if negative is divisor
        XYscale = 1 / np.asfarray(np.abs(scaler))  # makes sure the coordinates are turned into floats
    else:
        XYscale = np.asfarray(np.abs(scaler))

    # change operation if scaler used to write coordinates
    if not toRead:
        XYscale = 1 / XYscale

    return XYscale


#==============================================================================
# segyXY
#==============================================================================
def segyXY(inSEGY, o_outputNAVfile, s_srs, coord='Source', force_scaling=False, scaler=1., prefixCol3Nav='', segyName=''):
    '''
    Extract XY coordinates of traces from SEGY file (navigation) and
    return a (ntraces,2) Numpy array.
    '''
    # print(s_srs)
    # retrieve keywords for coordinate headers
    Xcoord, Ycoord = coordKeys[coord.lower()]

    # open file and read it with obspy module (does not read the data)
    SH, STH = loadSHandSTH(inSEGY)
    ntraces = SH['ntraces']

    # define output
    XYarray = np.zeros((ntraces, 2), dtype=float)

    # Retrieve coordinates
    if not force_scaling:  # get scaler from file
        scaler = STH['scalar_to_be_applied_to_all_coordinates']  # this is a vector with ntraces elements

        print('scaler from header:')
        print(scaler)
        XYscale = convertScaler(scaler, toRead=True)

        print('and convert ...')
        print(XYscale)
        # print("Jack1")    
    
    else:
        XYscale = scaler
        # print(XYscale)
        # print("Jack2")

    if s_srs == 4326:
        print('source Coor is "4326"')
        # print("y")
        XYarray[:, 0] = STH[Ycoord] * XYscale / 3600
        XYarray[:, 1] = STH[Xcoord] * XYscale / 3600
    else:
        # print("n")
        XYarray[:, 0] = STH[Xcoord] * XYscale
        XYarray[:, 1] = STH[Ycoord] * XYscale

    # for nav files
    f = open(o_outputNAVfile, "w")
    for i in range(0, len(XYarray), 1):

        lon_nav = str(XYarray[i,1]).replace('[','').replace(']','')
        lat_nav = str(XYarray[i,0]).replace('[','').replace(']','')

        f.write(lon_nav + ',' + lat_nav + ',' + prefixCol3Nav + '_' + segyName + '\n')
    f.close


    return XYarray, XYscale


#==============================================================================
# segy2segy
#==============================================================================
def segy2segy(inSEGY,
              outSEGY,
              o_outputNAVfile='',
              s_srs=23029,
              t_srs=23030,
              s_coord='Source',
              t_coord='CDP',
              force_scaling=False,
              scaler=1.,
              i_interpolate='N',
              p_prefixCol3Nav='',
              segyName=''
              ):
    '''
    Transform coordinates in SEGY files. This function makes use of the GDAL
    library for processing coordinates and projections.

    Parameters
    ----------
    inSEGY : Filename
        Input SEGY file.
    outSEGY : Filename
        Output SEGY file.
    s_srs : Integer
        Spatial reference system of the input (source) file. Must be defined as
        a EPSG code, i.e. 23029 for ED50 / UTM Zone 29N
    t_srs : Integer
        Spatial reference system of the output (target) file. Must be defined
        as a EPSG code, i.e. 23030 for ED50 / UTM Zone 30N
    s_coord : String
        Position of the coordinates in the input SEGY file. The field corresponds
        to a byte position in the binary file.
    t_coord : String
        Position of the coordinates in the output SEGY file. The field corresponds
        to a byte position in the binary file.
    force_scaling : Boolean
        If True, the program will use the number defined by the scaler argument
        to calculate the coordinates. Default is False and so the program will read
        the coordinate scaler from the SEGY file. It will use the same value for
        writing coordinates in the new SEGY file.
    scaler : Float
        Used in combination with force_scaling. The scaler is defined like for
        a SEGY file, for example -100 for dividing by 100 when reading.

    '''
    # read coordinates from input
    XYarray, XYscale = segyXY(inSEGY, o_outputNAVfile, s_srs, s_coord, force_scaling, scaler, p_prefixCol3Nav, segyName) 

    # transform coordinates
    newXYarray = projectPoints(XYarray, s_srs, t_srs, i_interpolate)
    # print('transform coordinates')
    # print(newXYarray)

    # Apply scaling #check_Chin-Yeh Chen
    # newXYarray = newXYarray / np.column_stack((XYscale, XYscale)) # 0.01(NOR1) or 0.001(LGD)
    # print('Apply scaling #check_Chin-Yeh Chen')
    # print(newXYarray)

    # load SEGY object (headers only)
    seis = _read_segy(inSEGY, headonly=True)
    traces = seis.traces

    # get key for coordinates position in output file
    Xcoord, Ycoord = coordKeys[t_coord.lower()]

    # insert new coordinates in SEGY object
    for i, trace in enumerate(traces):
        trace.header.__setattr__(Xcoord, int(newXYarray[i, 0]))
        trace.header.__setattr__(Ycoord, int(newXYarray[i, 1]))

    # write output SEGY with new coordinates
    seis.write(outSEGY)


#==============================================================================
# main function
#==============================================================================
def main():

    parser = argparse.ArgumentParser(
        description='Reproject SEGY coordinates.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'input_file', metavar='Input SEGY file or directory', type=str, help='The path to a SEGY file or a directory.')
    parser.add_argument(
        '-o',
        '--output',
        metavar='Output SEGY file',
        type=str,
        help="The path to the output SEGY file. Files can't be overwritten.")
    parser.add_argument(
        '-s_srs',
        metavar='source spatial reference set',
        type=int,
        default=23029,
        help='The spatial reference of the input file defined as a EPSG code.')
    parser.add_argument(
        '-t_srs',
        metavar='target spatial reference set',
        type=int,
        default=23030,
        help='The spatial reference of the output file defined as a EPSG code.')
    parser.add_argument(
        '-s_coord',
        metavar='Source coordinate position',
        type=str,
        default='Source',
        help="Position of coordinates in the input SEGY headers, to choose in ['Source', 'Group', 'CDP'].")
    parser.add_argument(
        '-t_coord',
        metavar='Target coordinate position',
        type=str,
        default='CDP',
        help="Position of the new coordinates in the output SEGY headers, to choose in ['Source', 'Group', 'CDP'].")
    parser.add_argument(
        '-fs',
        '--force_scaling',
        action='store_true',
        help='If used, the program will use the number defined by the scaler argument to scale the coordinates.')
    parser.add_argument(
        '-sc', '--scaler', metavar='scaler', type=float, default=1.0, help='Scaling factor applied to coordinates.')
    parser.add_argument(
        '-s',
        '--suffix',
        metavar='Suffix to output filename',
        type=str,
        default='',
        help='Suffix to add to the input filename to create the output filename.')
    parser.add_argument(
        '-i_interpolate',
        metavar='Interpolate X and Y coordinate position',
        type=str,
        default='N',
        help="Interpolate")
    parser.add_argument(
        '-o_outputFolder',
        metavar='Output folder for SEGY file',
        type=str,
        help="The path to the output SEGY file.")
    parser.add_argument(
        '-p_prefixCol3Nav',
        metavar='prefix of the col3 of nav file',
        type=str,
        help="The prefix of the col3 of nav file")   
    parser.add_argument(
        '-o_outputFolderForNAV',
        metavar='Output folder for NAV file',
        type=str,
        help="The path to the output NAV file.")                  

    args = parser.parse_args()
    infile = args.input_file
    # --CY--
    outputFolder = args.o_outputFolder
    outputFolderForNAV = args.o_outputFolderForNAV

    # Process file or list of files
    if os.path.isfile(infile):
        print("Processing file: {}".format(os.path.basename(infile)))
        if args.output:
            segy2segy(infile, args.output, args.s_srs, args.t_srs, args.s_coord, args.t_coord, args.force_scaling,
                      args.scaler)
            print("SEGY coordinates successfully projected.")
        elif args.suffix != '':
            segyName, extension = os.path.splitext(infile)
            outfile = segyName + args.suffix + extension
            segy2segy(infile, outfile, args.s_srs, args.t_srs, args.s_coord, args.t_coord, args.force_scaling,
                      args.scaler)
            print("SEGY coordinates successfully projected.")
        else:
            print("Error: output file name or suffix not provided.")  # file cannot be overwritten

    elif os.path.isdir(infile): # list of files
        if args.suffix != '':
            print("Reading SEGY files in {}".format(infile))
            for f in os.listdir(infile):
                if not f.endswith(('.seg','.sgy','.segy','.SEG','.SGY','.SEGY')):
                    print("Please chech the input file extension. (Note: .seg .sgy .segy .SEG .SGY .SEGY are allowed.)")
                    continue
                # if re.search("\\.se?g?y$", f, flags=re.IGNORECASE):
                print("---> init --->")
                print("Processing file: {}".format(f))
                target = os.path.join(infile, f)
                segyName, extension = os.path.splitext(f)
                outfile = os.path.join(outputFolder, segyName + args.suffix + extension)
                outputNAVfile = os.path.join(outputFolderForNAV, "NAV_" + segyName + ".txt") #CY
                segy2segy(target, outfile, outputNAVfile, args.s_srs, args.t_srs, args.s_coord, args.t_coord, args.force_scaling,
                          args.scaler, args.i_interpolate, args.p_prefixCol3Nav, segyName)
                    
                    
                print("Done!")
            print("\nAll SEGY files successfully processed.")
        else:
            print("Error: Please provide a suffix for output files (option -s).")  # files cannot be overwritten
    else:
        print("Error: input is not a file or directory.")


if __name__ == "__main__":
    main()
