##GROUP ##: PACEMAKER
##DCM


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

import csv

#Variables
Modes = []
Activate = []

#Entries Array
Parameter_Entries = []
Parameter_Labels = []

#Read in list of parameters
Par_File = open("Parameters.txt","r")
Parameters = Par_File.readlines()
Par_File.close()

#Read in list of modes
with open('Modes.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        Modes.append(row['Mode'])
        Activate.append(row)
        

def Activate_Entries(Mode):
    for Current in Activate:
        if Current['Mode'] == Mode:
            for i in range(0,len(Parameters)):
                if Current[Parameters[i][:-1]] == "X":
                    Parameter_Entries[i].config(state="NORMAL")
                else:
                    Parameter_Entries[i].config(state="readonly")


def PARAMETER_SCREEN():
    ParameterScreen = Tk()
    ParameterScreen.title("Pacemaker Parameters")
    ParameterScreen.geometry("850x330")

    Connect_Button = Button(ParameterScreen,text="CONNECTED", fg="green") ##Not Connected to BOARD BUTTON DOES NOT WORK
    Status_Button = Button(ParameterScreen,text="CONNECTED TO PRECONFIGURED DEVICE",fg="green")
    Connect_Button.place(x=150,y=10)
    Status_Button.place(x=300,y=10)

    #Generate Entires and Labels
    for i in Parameters:
        Parameter_Entries.append(ttk.Entry(ParameterScreen))
        Parameter_Labels.append(Label(ParameterScreen,text=i[:-1]))

    xm = 0
    ym = 0
    for j in range(0,len(Parameter_Entries)):
        ## Multipliers and adders for placing entries and labels
        if j<8: xm=0
        if j>=8 and j<16: xm=1
        if j >= 16: xm=2
        if j==8: ym = -8
        if j==16: ym = -16
        
        Parameter_Labels[j].place(x=15+280*xm,y=(j+ym)*30+50)
        Parameter_Entries[j].place(x=145+280*xm,y=(j+ym)*30+50)

    variable = StringVar(ParameterScreen)
    Mode_Select = ttk.OptionMenu(ParameterScreen, variable,*Modes,command= lambda a :Activate_Entries(variable.get()))
    variable.set(Modes[9]) # default value
    Activate_Entries(variable.get())

    Mode_Select.place(x=30,y=10)

                                 
    mainloop()

#PARAMETER_SCREEN()

