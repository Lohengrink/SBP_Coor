import os
# os.system("python segy2segy.py D:\programmer_\segy2segyHdconrt_CY\dataHdF3tmp -s_srs 3826 -t_srs 32650 -s_coord Source -t_coord CDP -s _UTM") #蝦轉TM2 121-->UTM50M
# os.system("python segy2segy.py D:\programmer_\segy2segyHdconrt_CY\BigButt -s_srs 3826 -t_srs 32650 -s_coord Source -t_coord CDP -s _UTM")


main = "python segy2segy.py"
input_path = "D:\programmer_\segy2segy_CruiseSBP_CY2\segy2segy-master\SBP_input" #choose what you want

s_srs = "4326"
t_srs = "32650"
s_coord = "Group"
t_coord = "CDP"
s = "_UTM50N"
sc = "0.01"
o_outputFolder = "D:\programmer_\segy2segy_CruiseSBP_CY2\segy2segy-master\SBP_output" #choose what you want
i_interpolate = "N"



arg_s_srs = "-s_srs"
arg_t_srs = "-t_srs"
arg_s_coord = "-s_coord"  # bit
arg_t_coord = "-t_coord"  # bit
arg_s = "-s"  # string
arg_sc = "-sc"
arg_o_outputFolder = "-o_outputFolder"
arg_i_interpolate = "-i_interpolate"
arg_fs = "-fs"



sp = " "
command = main + sp + input_path + sp + \
    arg_s_srs + sp + s_srs + sp + \
    arg_t_srs + sp + t_srs + sp + \
    arg_s_coord + sp + s_coord + sp + \
    arg_t_coord + sp + t_coord + sp + \
    arg_s + sp + s + sp + \
    arg_i_interpolate + sp + i_interpolate + sp + \
    arg_o_outputFolder + sp + o_outputFolder + sp + \
    arg_sc + sp + sc + sp + \
    arg_fs        


# os.system("python segy2segy.py D:\programmer_\segy2segyHdconrt_CY\BigButt -s_srs 4326 -t_srs 32650 -s_coord Source -t_coord CDP -s _UTM")


os.system(command)

