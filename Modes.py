##GROUP ##: PACEMAKER
##DCM


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
#from graph import *
import numpy

from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.animation as animation

from PIL import Image
from PIL import ImageTk

import csv


####Variables
Modes = []
Activate = []
RANGE_INC = []
#Mode
RANGE_INC.append("OFF DDD VDD DDI DOO AOO AAI VOO VVI AAT VVT DDDR VDDR DDIR DOOR AOOR AAIR VOOR VVIR".split())
#Lower Rate Limit
RANGE_INC.append(list(numpy.arange(30,50,5))+list(numpy.arange(50,90,1))+list(numpy.arange(90,176,5)))
#Upper Rate LImit
RANGE_INC.append(list(numpy.arange(50,176,5)))
#MSR
RANGE_INC.append(list(numpy.arange(50,176,5)))
#FixedAV
RANGE_INC.append(list(numpy.arange(70,301,10)))
#Dynamic AV Delay
RANGE_INC.append(["ON","OFF"])
#Sensed AV
RANGE_INC.append(["OFF"]+(list(numpy.arange(-10,-100,-10))))
#Atrial Amplitude
RANGE_INC.append(["OFF"]+(list(numpy.arange(0.5,3.3,0.1)))+(list(numpy.arange(3.5,7.1,0.5))))
#Ventricular Amplitude
RANGE_INC.append(list(numpy.arange(3.5,7.1,0.5)))
#Atrial Pulse width
RANGE_INC.append([0.05]+(list(numpy.arange(0.1,2.1,0.1))))
#Ventricular Pulse width
RANGE_INC.append(list(numpy.arange(0.1,2.0,0.1)))
#Atrial Sensitivity
RANGE_INC.append([0.25,0.5,0.75])
#Ventricular Sensitivity
RANGE_INC.append(list(numpy.arange(1.0,10.1,0.5)))
#VRP
RANGE_INC.append(list(numpy.arange(150,501,10)))
#ARP
RANGE_INC.append(list(numpy.arange(150,501,10)))
#PVARP
RANGE_INC.append(list(numpy.arange(150,501,10)))
#PVARP Extension
RANGE_INC.append(["OFF"]+(list(numpy.arange(50,401,50))))
#Hysteresis
RANGE_INC.append(["OFF"]+list(numpy.arange(30,50,5))+list(numpy.arange(50,90,1))+list(numpy.arange(90,176,5)))
#Rate Smoothing
RANGE_INC.append(["OFF",3,6,9,12,15,18,21,25])
#ATR Duration
RANGE_INC.append([10]+list(numpy.arange(20,81,20))+list(numpy.arange(100,2001,100)))
#ATR Fallback Mode
RANGE_INC.append(["ON","OFF"])
#ATR Fallback Time
RANGE_INC.append([1,2,3,4,5])
#AThresh
RANGE_INC.append(["V-Low", "Low", "Med-Low", "Med", "Med-High", "High", "V-High"])
#ReactionTime
RANGE_INC.append([10,20,30,40,50])
#ResponseFactor
RANGE_INC.append(list(numpy.arange(1,17,1)))
#Recovery Time
RANGE_INC.append(list(numpy.arange(2,17,1)))


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

def validcmd(wid,arr):
    for i in arr:
        if wid.get() == str(i):
            wid.config(background="#ccffcc")
            return True
    wid.config(background="#ff8080")
    return False


def Activate_Entries(Mode):
    for Current in Activate:
        if Current['Mode'] == Mode:
            for i in range(1,len(Parameters)):
                if Current[Parameters[i][:-1]] == "":
                    Parameter_Entries[i].config(state=DISABLED)
                else:
                    Parameter_Entries[i].config(state=NORMAL)

def Values_To_File(Username):
    user_file = open('userdata/'+Username,"w").close()
    user_file = open('userdata/'+Username,"a")
    for i in range(0,len(Parameters)):
        user_file.write(Parameters[i][:-1])
        user_file.write(": ")
        user_file.write(Parameter_Entries[i].get())
        user_file.write("\n")
    user_file.close()

def Load_Values(Username):
    user_file = open('userdata/'+Username,"r")
    p = user_file.readlines()
    a =""
    for i in range(0,len(Parameters)):
        Parameter_Entries[i].delete(0,END)
        a = p[i][p[i].find(": ")+2:-1]
        Parameter_Entries[i].insert(0,a)

def showegram(Username):
    #Graph Variables
    Graph = Tk()
    Graph.wm_title("egram")
    fig = Figure(figsize=(5,4), dpi=100)
    t = numpy.arange(0, 3, .01)
    a = fig.add_subplot(111)
    ecanvas = FigureCanvasTkAgg(fig, master=Graph)  # A tk.DrawingArea.
    ecanvas.draw()
    ecanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(ecanvas, Graph)
    toolbar.update()
    ecanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def _quit():
        Graph.quit()     # stops mainloop
        Graph.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    def animate(i):
        pullData = open("egramdata/sample.txt","r").read()
        dataList = pullData.split('\n')
        xList = []
        yList = []
        for eachLine in dataList:
            if len(eachLine) > 1:
                x,y = eachLine.split(',')
                xList.append(int(x))
                yList.append(int(y))

        a.clear()
        a.plot(xList,yList)

    button = Button(master=Graph, text="Quit", command=_quit)
    button.pack(side=BOTTOM)

    ani = animation.FuncAnimation(fig,animate,interval=1000)
    mainloop()


###### NOT WORKING
###### WHEN CONNECTION WITH PACEMAKER IS WORKING PLS FILL IN

def isConnected():
    # if connected here then
    return False
    #else:
    #return False

def PARAMETER_SCREEN(Username):
    ParameterScreen = Tk()
    ParameterScreen.title("Pacemaker Parameters")
    ParameterScreen.geometry("850x330")

    # BUTTONS
    Save_Button = ttk.Button(ParameterScreen,text="Save",command=lambda: Values_To_File(Username))
    Load_Button = ttk.Button(ParameterScreen,text="Load",command=lambda: Load_Values(Username))
    Show_Graph = ttk.Button(ParameterScreen, text="Show Graph",command=lambda: showegram(Username))
    Load_Button.place(x=95,y=290)
    Save_Button.place(x=15,y=290)
    Show_Graph.place(x=175,y=290)
    # pictures
    green = ImageTk.PhotoImage(Image.open('icons/green_button.png').resize((25,25),Image.ANTIALIAS))
    red = ImageTk.PhotoImage(Image.open('icons/red_button.png').resize((25,25),Image.ANTIALIAS))

    cON = Label(ParameterScreen, image=green)           # need multiple bc cant place twice
    cOFF = Label(ParameterScreen, image=red)
    configON = Label(ParameterScreen, image=green)
    configOFF = Label(ParameterScreen, image=red)

    if (isConnected() == True):
        cText = "CONNECTED"
        cpText = "CONNECTED TO PRECONFIGURED DEVICE"
        cON.place(x=300,y=10)
        configON.place(x=450,y=10)
    else:
        cText = "NOT CONNECTED"
        cpText = "NOT CONNECTED TO PRECONFIGURED DEVICE"
        cOFF.place(x=300,y=10)
        configOFF.place(x=450,y=10)

    cLabel = Label(ParameterScreen, text=cText)
    configLabel = Label(ParameterScreen, text=cpText)
    cLabel.place(x=335, y=13)
    configLabel.place(x=485,y=13)

    #Generate Entires and Labels
    VAR = []
    VAR.append(StringVar())
    Parameter_Entries.append(Spinbox(ParameterScreen,values=RANGE_INC[0],command=lambda : Activate_Entries(Parameter_Entries[0].get())))
    Parameter_Labels.append(Label(ParameterScreen,text=Parameters[0][:-1]))



    for i in range(1,26):
        VAR.append(StringVar())
        Parameter_Entries.append(Spinbox(ParameterScreen,buttondownrelief=GROOVE,buttonuprelief=GROOVE,textvariable=VAR[i],values=RANGE_INC[i]))
        Parameter_Labels.append(Label(ParameterScreen,text=Parameters[i][:-1]))

    VAR[1].trace('w',lambda a,b,c:validcmd(Parameter_Entries[1],RANGE_INC[1]))
    VAR[2].trace('w',lambda a,b,c:validcmd(Parameter_Entries[2],RANGE_INC[2]))
    VAR[3].trace('w',lambda a,b,c:validcmd(Parameter_Entries[3],RANGE_INC[3]))
    VAR[4].trace('w',lambda a,b,c:validcmd(Parameter_Entries[4],RANGE_INC[4]))
    VAR[5].trace('w',lambda a,b,c:validcmd(Parameter_Entries[5],RANGE_INC[5]))
    VAR[6].trace('w',lambda a,b,c:validcmd(Parameter_Entries[6],RANGE_INC[6]))
    VAR[7].trace('w',lambda a,b,c:validcmd(Parameter_Entries[7],RANGE_INC[7]))
    VAR[8].trace('w',lambda a,b,c:validcmd(Parameter_Entries[8],RANGE_INC[8]))
    VAR[9].trace('w',lambda a,b,c:validcmd(Parameter_Entries[9],RANGE_INC[9]))
    VAR[10].trace('w',lambda a,b,c:validcmd(Parameter_Entries[10],RANGE_INC[10]))
    VAR[11].trace('w',lambda a,b,c:validcmd(Parameter_Entries[11],RANGE_INC[11]))
    VAR[12].trace('w',lambda a,b,c:validcmd(Parameter_Entries[12],RANGE_INC[12]))
    VAR[13].trace('w',lambda a,b,c:validcmd(Parameter_Entries[13],RANGE_INC[13]))
    VAR[14].trace('w',lambda a,b,c:validcmd(Parameter_Entries[14],RANGE_INC[14]))
    VAR[15].trace('w',lambda a,b,c:validcmd(Parameter_Entries[15],RANGE_INC[15]))
    VAR[16].trace('w',lambda a,b,c:validcmd(Parameter_Entries[16],RANGE_INC[16]))
    VAR[17].trace('w',lambda a,b,c:validcmd(Parameter_Entries[17],RANGE_INC[17]))
    VAR[18].trace('w',lambda a,b,c:validcmd(Parameter_Entries[18],RANGE_INC[18]))
    VAR[19].trace('w',lambda a,b,c:validcmd(Parameter_Entries[19],RANGE_INC[19]))
    VAR[20].trace('w',lambda a,b,c:validcmd(Parameter_Entries[20],RANGE_INC[20]))
    VAR[21].trace('w',lambda a,b,c:validcmd(Parameter_Entries[21],RANGE_INC[21]))
    VAR[22].trace('w',lambda a,b,c:validcmd(Parameter_Entries[22],RANGE_INC[22]))
    VAR[23].trace('w',lambda a,b,c:validcmd(Parameter_Entries[23],RANGE_INC[23]))
    VAR[24].trace('w',lambda a,b,c:validcmd(Parameter_Entries[24],RANGE_INC[24]))
    VAR[25].trace('w',lambda a,b,c:validcmd(Parameter_Entries[25],RANGE_INC[25]))



    #Parameter_Entries[0].config(command=lambda : Activate_Entries(Parameter_Entries[0].get()))
    Load_Values(Username)
    Parameter_Entries[0].config(state="readonly")


    xm = 0
    ym = -1

    #Parameter_Labels[0].place(x=15+280,y=30)
    #Parameter_Entries[0].place(x=145+280,y=30)
    for j in range(0,len(Parameter_Entries)):
        ## Multipliers and adders for placing entries and labels
        if j<9: xm=0
        if j>=9 and j<17: xm=1
        if j >= 17: xm=2
        if j==9: ym = -9
        if j==17: ym = -17
        #Parameter_Entries[j].config(validate="key",validatecommand=(valinp,"%P"))
        Parameter_Labels[j].place(x=15+280*xm,y=(j+ym)*30+50)
        Parameter_Entries[j].place(x=145+280*xm,y=(j+ym)*30+50)



    #variable = StringVar(ParameterScreen)
    #Mode_Select = ttk.OptionMenu(ParameterScreen, variable,*Modes,command= lambda a :Activate_Entries(variable.get()))
    #variable.set(Modes[9]) # default value
    Activate_Entries(Parameter_Entries[0].get())

    #Mode_Select.place(x=30,y=10)


    mainloop()

#PARAMETER_SCREEN("kathan")
