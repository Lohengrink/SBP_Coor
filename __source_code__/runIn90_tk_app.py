from tkinter import *
from tkinter import filedialog
import os
import tkinter.font as font
from tkinter import messagebox
from tkinter import PhotoImage

window = Tk()
window.title("Welcome to Segy2Segy app!!!!")

# for open file explorer
def open_dialog(txt_input_object):
    dir = filedialog.askdirectory()
    txt_input_object.insert(0, dir)
    return dir

# run 
def submit_run():
    s_srs = txt_s_srs.get()
    t_srs = txt_t_srs.get()
    s_coord = txt_s_coord.get()
    t_coord = txt_t_coord.get()
    s = txt_s.get()
    input_path = txt_input_path.get()
    output_path = txt_output_path.get()
    prefix_col3_nav = txt_prefix_col3_nav.get()
    output_path_NAV = txt_output_path_NAV.get()

    # ---
    main = "python .\\__source_code__\\segy2segy.py"

    sc = "0.01"
    i_interpolate = "N"

    arg_s_srs = "-s_srs"
    arg_t_srs = "-t_srs"
    arg_s_coord = "-s_coord"  # bit
    arg_t_coord = "-t_coord"  # bit
    arg_s = "-s"  # string
    arg_sc = "-sc"
    arg_output_path = "-o_outputFolder"
    arg_i_interpolate = "-i_interpolate"
    arg_fs = "-fs"
    arg_prefix_col3_nav = "-p_prefixCol3Nav"
    arg_o_outputFolderForNAV = "-o_outputFolderForNAV"


    sp = " "
    # forcing scalar
    # command = main + sp + input_path + sp + \
    #     arg_s_srs + sp + s_srs + sp + \
    #     arg_t_srs + sp + t_srs + sp + \
    #     arg_s_coord + sp + s_coord + sp + \
    #     arg_t_coord + sp + t_coord + sp + \
    #     arg_s + sp + s + sp + \
    #     arg_i_interpolate + sp + i_interpolate + sp + \
    #     arg_output_path + sp + output_path + sp + \
    #     arg_sc + sp + sc + sp + \
    #     arg_prefix_col3_nav + sp + prefix_col3_nav + sp + \
    #     arg_o_outputFolderForNAV + sp + output_path_NAV + sp + \
    #     arg_fs

    # Instead of forcing scalar, follow from header # 2023.01.09
    command = main + sp + input_path + sp + \
        arg_s_srs + sp + s_srs + sp + \
        arg_t_srs + sp + t_srs + sp + \
        arg_s_coord + sp + s_coord + sp + \
        arg_t_coord + sp + t_coord + sp + \
        arg_s + sp + s + sp + \
        arg_i_interpolate + sp + i_interpolate + sp + \
        arg_output_path + sp + output_path + sp + \
        arg_prefix_col3_nav + sp + prefix_col3_nav + sp + \
        arg_o_outputFolderForNAV + sp + output_path_NAV

    # print(command)
    os.system(command)
    window.destroy()

def do_nothing():
    messagebox.showinfo(title=">/////<", message="Yada~ We still work on it. But I just wanna veg out in front of the TV all weekend.xdd")

# define font
myFont = font.Font(size=14)


#
tool_bar = Menu(window)
window.config(menu=tool_bar)

##
file_menu = Menu(tool_bar, tearoff=0)
###
file_menu.add_command(label="New", command=do_nothing)
file_menu.add_command(label="Open", command=do_nothing)
file_menu.add_command(label="Save", command=do_nothing)
file_menu.add_command(label="Save as...", command=do_nothing)
file_menu.add_command(label="Close", command=do_nothing)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=window.quit)
tool_bar.add_cascade(label="File", menu=file_menu)

##
edit_menu = Menu(tool_bar, tearoff=0)
###
edit_menu.add_command(label="Undo", command=do_nothing)
tool_bar.add_cascade(label="Edit", menu=edit_menu)

##
help_menu = Menu(tool_bar, tearoff=0)
###
help_menu.add_command(label="Help Index", command=do_nothing)
help_menu.add_command(label="About...", command=do_nothing)
tool_bar.add_cascade(label="Help", menu=help_menu)

# s_srs
lbl_s_srs = Label(window, text="Coor. code of the input ex: 4326 (i.e. Lon, Lat)")
lbl_s_srs.grid(column=0, row=0)
lbl_s_srs['font'] = myFont
txt_s_srs = Entry(window, width=80)
txt_s_srs.grid(column=1, row=0)
txt_s_srs.insert(0, "4326")
txt_s_srs['font'] = myFont

# t_srs
lbl_t_srs = Label(window, text="Coor. code of the output ex: 32650 (i.e. UTM50N)")
lbl_t_srs.grid(column=0, row=1)
lbl_t_srs['font'] = myFont
txt_t_srs = Entry(window, width=80)
txt_t_srs.grid(column=1, row=1)
txt_t_srs.insert(0, "32650")
txt_t_srs['font'] = myFont

# s_coord
lbl_s_coord = Label(window, text="input Header ('Source', 'Group', or 'CDP')")
lbl_s_coord.grid(column=0, row=2)
lbl_s_coord['font'] = myFont
txt_s_coord = Entry(window, width=80)
txt_s_coord.grid(column=1, row=2)
txt_s_coord.insert(0, "Source")
txt_s_coord['font'] = myFont

# t_coord
lbl_t_coord = Label(window, text="output Header ('Source', 'Group', or 'CDP')")
lbl_t_coord.grid(column=0, row=3)
lbl_t_coord['font'] = myFont
txt_t_coord = Entry(window, width=80)
txt_t_coord.grid(column=1, row=3)
txt_t_coord.insert(0, "CDP")
txt_t_coord['font'] = myFont

# s
lbl_s = Label(window, text="suffix for the output file name ex: '_UTM50N'")
lbl_s.grid(column=0, row=4)
lbl_s['font'] = myFont
txt_s = Entry(window, width=80)
txt_s.grid(column=1, row=4)
txt_s.insert(0, "_UTM50N")
txt_s['font'] = myFont

# input_path
lbl_input_path = Label(window, text="Choose the folder for input segy files")
lbl_input_path.grid(column=0, row=5)
lbl_input_path['font'] = myFont
txt_input_path = Entry(window, width=80)
txt_input_path.grid(column=1, row=5)
txt_input_path['font'] = myFont
btn_input_path = Button(window, text="Open folder", command=lambda:open_dialog(txt_input_path))
btn_input_path.grid(column=2, row=5)
btn_input_path['font'] = myFont

# output_path
lbl_output_path = Label(window, text="Choose the folder for output segy files")
lbl_output_path.grid(column=0, row=6)
lbl_output_path['font'] = myFont
txt_output_path = Entry(window, width=80)
txt_output_path.grid(column=1, row=6)
txt_output_path['font'] = myFont
btn_output_path = Button(window, text="Open folder", command=lambda:open_dialog(txt_output_path))
btn_output_path.grid(column=2, row=6)
btn_output_path['font'] = myFont

# prefix_col3_nav
lbl_prefix_col3_nav = Label(window, text="prefix for col3 of NAV file ex: SBPNOR1-0030 (ex of clo3: SBPNOR1-0030_filename)")
lbl_prefix_col3_nav.grid(column=0, row=7)
lbl_prefix_col3_nav['font'] = myFont
txt_prefix_col3_nav = Entry(window, width=80)
txt_prefix_col3_nav.grid(column=1, row=7)
txt_prefix_col3_nav.insert(0, "SBPNOR1-0030")
txt_prefix_col3_nav['font'] = myFont

# output_path for NAV
lbl_output_path_NAV = Label(window, text="Choose the folder for output NAV files (before converting)")
lbl_output_path_NAV.grid(column=0, row=8)
lbl_output_path_NAV['font'] = myFont
txt_output_path_NAV = Entry(window, width=80)
txt_output_path_NAV.grid(column=1, row=8)
txt_output_path_NAV['font'] = myFont
btn_output_path_NAV = Button(window, text="Open folder", command=lambda:open_dialog(txt_output_path_NAV))
btn_output_path_NAV.grid(column=2, row=8)
btn_output_path_NAV['font'] = myFont


btn_run = Button(window, text="RUN", bg='#0052cc', fg='#ffffff', command=lambda:submit_run())
btn_run.grid(column=1, row=9)
btn_run['font'] = myFont

window.geometry('1480x680')

window.mainloop()