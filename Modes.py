##GROUP ##: PACEMAKER
##DCM


from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import time
#from graph import *
import numpy
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.animation as animation
import serial
from struct import *

from PIL import Image
from PIL import ImageTk

import csv

units = ["", "(ppm)", "(ppm)", "(ppm)", "(ms)" , "", "(ms)", 
"(ms)", "(V)","(V)", "(ms)", "(mV)","(ms)","(ms)","(ms)", "(ms)",
"(ppm)","(%)", "","(cc)", "(min)", "(ms)", "", "(sec)", "", "(min)"]
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

##Screen
ParameterScreen = Tk()
ParameterScreen.title("Pacemaker Parameters")
ParameterScreen.geometry("850x330")



#Read in list of modes
with open('Modes.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        Modes.append(row['Mode'])
        Activate.append(row)




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
    fig = Figure(figsize=(7,4), dpi=100)

    a = fig.add_subplot(111)

    # make graph look pretty
    a.grid(True)
    a.set_title("Electrogram for " + Username)
    a.set_xlabel("Time")
    a.set_ylabel("Amplitude")

    ecanvas = FigureCanvasTkAgg(fig, master=Graph)  # A tk.DrawingArea.
    ecanvas.draw()

    # toolbars at bottom
    ecanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
    toolbar = NavigationToolbar2Tk(ecanvas, Graph)
    toolbar.update()
    ecanvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    # write input data to file
    user_file = open('egramdata/'+Username,'w').close()
    global tVal,aVal,vVal
    global tList,aList,vList
    tVal,aVal,vVal = 0,0,0
    tList,aList,vList = [],[],[]
    timeInt = .1

    def _quit():
        Graph.quit()     # stops mainloop
        Graph.destroy()  # this is necessary on Windows to prevent
                        # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    def animate(i):
        user_file = open("egramdata/"+Username,"a")
        global tVal,aVal,vVal
        global tList,aList,vList

        tVal += timeInt       # x is going up in time
        aVal = math.sin(tVal)*1000 # a = atrial, v = ventricular
        vVal = math.cos(tVal)*1000 # HAVE TO BUMP IT UP BC IT WONT PLOT SMALL VALUES, CAN CHANGE AXIS LATER

                                    # change to input values recieved from pacemaker
        tList.append(tVal)              # append to list to graph and write to datafile
        aList.append(aVal)
        vList.append(vVal)

        user_file.write(str(tVal) + "," + str(aVal)+ "," + str(vVal) + "\n")
        a.clear()
        yeet = a.plot(tList[-10:],aList[-10:],tList[-10:],vList[-10:])  # plots last 10 points
        a.set_ylim([-1100,1100])
        a.grid()
        a.set_xlabel("Time")
        a.set_ylabel("Ampltiude")
        a.set_title("Electrogram Data for " + Username)
        return yeet             # blit requires you to return your plot to save resources by not redrawing the whole thing

    button = Button(master=Graph, text="Quit", command=_quit)
    button.pack(side=BOTTOM)


    ani = animation.FuncAnimation(fig,animate,interval=timeInt*100,blit=True)
    mainloop()


###### NOT WORKING
###### WHEN CONNECTION WITH PACEMAKER IS WORKING PLS FILL IN

def isConnected():
    try:
        check = serial.Serial('COM6', baudrate=115200)
        check.close()
        return True
    except:
        return False


def ECHO_PARAMS():
    try:
        ser = serial.Serial('COM6', baudrate=115200)
        ser.timeout =5 
    except:
        messagebox.showmessage("Pacemaker Connection Error", "The pacemaker is not connected!")
        return

    cmd = b'\x16\x45\x49'
    print(ser.write(cmd))
    print(ser.write(bytes(54)))
    a = ser.read(50)
    print(a)
    unpacked = list(unpack('>'+'H'*25,a))
    print(unpacked)
    ser.close()
    out_string= ""
    for i in range(1,len(Parameters)):
        out_string = out_string+Parameters[i]+ ": " +str(unpacked[i-1])


def SEND_PARAMS(Username):
    answer = messagebox.askyesnocancel("Question", "You must save any changes prior to sendinng to pacemaker. Continue?")
    user_file = open('userdata/'+Username,"r")
    p = user_file.readlines()
    a = []
    b = []
    byte_b = []
    byte_length = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
    

    for i in range(0,len(Parameters)):
        a.append(p[i][p[i].find(": ")+2:-1])
        print(p[i][p[i].find(": ")+2:-1])
        
    

    for i in range(0,len(a)):
        if a[i].find('.')>0:
            b.append(int(round(float(a[i]),2)*1000))
        elif a[i] == 'OFF' and i > 0 :
            b.append(0)
        elif a[i] == 'ON': 
            b.append(1)
        elif a[i].find('High')>=0 or a[i].find('Low')>=0 or a[i].find('Med')>=0:
            if a[i] == "V-Low": b.append(1)
            if a[i] == "V-Low": b.append(2)
            if a[i] == "Low": b.append(3)
            if a[i] == "Med-Low": b.append(4)
            if a[i] == "Med": b.append(5)
            if a[i] == "Med-High": b.append(6)
            if a[i] == "High": b.append(7)
            if a[i] == "V-High": b.append(8)
        elif a[i] == "OFF" and i == 0: b.append(bytes(4)) 
        elif a[i] == "AAT": b.append(a[i]+" ") 
        elif a[i] == "VVT": b.append(a[i]+" ")
        elif a[i] == "AOO": b.append(a[i]+" ")
        elif a[i] == "AAI": b.append(a[i]+" ")
        elif a[i] == "VOO": b.append(a[i]+" ")
        elif a[i] == "VVI": b.append(a[i]+" ")
        elif a[i] == "VDD": b.append(a[i]+" ")
        elif a[i] == "DOO": b.append(a[i]+" ")
        elif a[i] == "DDI": b.append(a[i]+" ")
        elif a[i] == "DDD": b.append(a[i]+" ")
        elif a[i] == "AOOR": b.append(a[i])
        elif a[i] == "AAIR": b.append(a[i])
        elif a[i] == "VOOR": b.append(a[i])
        elif a[i] == "VVIR": b.append(a[i])
        elif a[i] == "VDDR": b.append(a[i])
        elif a[i] == "DOOR": b.append(a[i])
        elif a[i] == "DDIR": b.append(a[i])
        elif a[i] == "DDDR": b.append(a[i])
        else:
            try:
                b.append(int(a[i]))
            except ValueError:
                b.append(a[i])
                  
    byte_b.append(b[0].encode())
    
    for i in range(1,26):
        if b[i]>=0:
            byte_b.append(b[i].to_bytes(byte_length[i], byteorder='big',signed=True))
        elif b[i]<0:
            byte_b.append(b[i].to_bytes(byte_length[i], byteorder='big',signed=True))



    print(a)
    print(b)
    print(byte_b)
    print(len(byte_b))
    #print(len(a))

    try:
        ser = serial.Serial('COM6', baudrate=115200)
        ser.timeout =5 
    except:
        messagebox.showinfo("Pacemaker Connection \nError", "The pacemaker is not connected!")
        return
    print(ser.name)
    sum1 = 0 
  
    cmd = b'\x16\x45\x55'

    sum1 = sum1+ ser.write(cmd)
    for i in range(0,len(byte_b)):
        print(repr(byte_b[i]))
        sum1 =sum1 + ser.write(byte_b[i])
    print("total send:" , sum1)

    ser.close()




def PARAMETER_SCREEN(Username):


    # BUTTONS
    Save_Button = ttk.Button(ParameterScreen,text="Save",command=lambda: Values_To_File(Username))
    Load_Button = ttk.Button(ParameterScreen,text="Load",command=lambda: Load_Values(Username))
    Show_Graph = ttk.Button(ParameterScreen, text="Show Graph",command=lambda: showegram(Username))
    To_Pacemaker = ttk.Button(ParameterScreen,text="To Pacemaker",command= lambda:SEND_PARAMS(Username))
    Echo_Parameter = ttk.Button(ParameterScreen, text="Echo",command= lambda:ECHO_PARAMS())
    Load_Button.place(x=95,y=290)
    Save_Button.place(x=15,y=290)
    Show_Graph.place(x=175,y=290)
    To_Pacemaker.place(x=257, y=290)
    Echo_Parameter.place(x=350,y=290)

    # pictures
    green = ImageTk.PhotoImage(Image.open('icons/green_button.png').resize((25,25),Image.ANTIALIAS))
    red = ImageTk.PhotoImage(Image.open('icons/red_button.png').resize((25,25),Image.ANTIALIAS))

    cON = Label(ParameterScreen, image=green)           # need multiple bc cant place twice
    cOFF = Label(ParameterScreen, image=red)
    configON = Label(ParameterScreen, image=green)
    configOFF = Label(ParameterScreen, image=red)



    def validcmd(wid,arr):
        for i in arr:
            if wid.get() == str(i):
                wid.config(background="#ccffcc")
                To_Pacemaker.config(state="normal")
                return True
        wid.config(background="#ff8080")
        To_Pacemaker.config(state=DISABLED)
        return False


    def connection():
        if (isConnected() == True): # DEACTIVATE BUTTONS WHENS FALSE STILL NEEDS TO BE DONE
            cText = "CONNECTED        "
            cpText = "CONNECTED TO PRECONFIGURED DEVICE          "
            cON.place(x=300,y=10)
            cOFF.place_forget()
            configON.place(x=450,y=10)
            configOFF.place_forget()
        else:
            cText = "NOT CONNECTED"
            cpText = "NOT CONNECTED TO PRECONFIGURED DEVICE"
            cOFF.place(x=300,y=10)
            cON.place_forget()
            configOFF.place(x=450,y=10)
            configON.place_forget()

        cLabel = Label(ParameterScreen, text=cText)
        configLabel = Label(ParameterScreen, text=cpText)
        cLabel.place(x=335, y=13)
        configLabel.place(x=485,y=13)
        ParameterScreen.after(1000,connection)
    
    

    #Generate Entires and Labels
    VAR = []
    VAR.append(StringVar())
    Parameter_Entries.append(Spinbox(ParameterScreen,width=13,values=RANGE_INC[0],command=lambda : Activate_Entries(Parameter_Entries[0].get())))
    Parameter_Labels.append(Label(ParameterScreen,text=Parameters[0][:-1]+" "+units[0]))



    for i in range(1,26):
        VAR.append(StringVar())
        Parameter_Entries.append(Spinbox(ParameterScreen,width=13,buttondownrelief=GROOVE,buttonuprelief=GROOVE,textvariable=VAR[i],values=RANGE_INC[i]))
        Parameter_Labels.append(Label(ParameterScreen,text=Parameters[i][:-1]+" "+units[i]))

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
        Parameter_Entries[j].place(x=175+280*xm,y=(j+ym)*30+50)



    #variable = StringVar(ParameterScreen)
    #Mode_Select = ttk.OptionMenu(ParameterScreen, variable,*Modes,command= lambda a :Activate_Entries(variable.get()))
    #variable.set(Modes[9]) # default value
    Activate_Entries(Parameter_Entries[0].get())
    
    ParameterScreen.after(1000, connection)
    ParameterScreen.mainloop()

    #Mode_Select.place(x=30,y=10)





PARAMETER_SCREEN("oscar")
