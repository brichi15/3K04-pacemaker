##GROUP ##: PACEMAKER
##DCM

#comment

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from Modes import PARAMETER_SCREEN
from serial import *
from PIL import Image
from PIL import ImageTk

w=270
h=450

LoginScreen = Tk()
LoginScreen.title("Pacemaker")
LoginScreen.geometry(str(w)+"x"+str(h))

#FRAMES
LoginFrame = ttk.LabelFrame(LoginScreen,text="Login",width=w-20,height=120)
RegisterFrame = ttk.LabelFrame(LoginScreen,text="Register",width=w-20,height=175)

#Widgets
E1 = ttk.Entry(LoginFrame)                          #Useraname
E2 = ttk.Entry(LoginFrame,show="*")                 #Password
E3 = ttk.Entry(RegisterFrame)                       #Username
E4 = ttk.Entry(RegisterFrame, show="*")             #Password
E5 = ttk.Entry(RegisterFrame)                       #Verify Username
E6 = ttk.Entry(RegisterFrame, show="*")             #Verify Password

# change title here
titleLogo = ImageTk.PhotoImage(Image.open('icons/red_button.png').resize((w-25,h//4),Image.ANTIALIAS))

def Initialize_User(Username):
    Par_File = open("Parameters.txt","r")
    Parameters = Par_File.readlines()
    Par_File.close()

    # default values of parameters
    defaultValues = ['DDD','60','120','120','150','OFF','OFF','3.5','3.5','0.4','0.4','0.75','2.5','320','250','250','OFF','OFF','OFF','20','OFF','1','Med','30','8','5']
    user_file = open('userdata/'+Username,"w").close()
    user_file = open('userdata/'+Username,"a")
    for i in range(0,len(Parameters)):
        user_file.write(Parameters[i][:-1])
        user_file.write(": ")
        user_file.write(defaultValues[i])
        user_file.write("\n")
    user_file.close()


#validate alpha numeric only
def verify_login_alnum(inp):
    if inp.isalnum():
        return True
    elif inp is "":
        return True
    else:
        return False

def Create_New_User(Username, Password):                                    #Create New User
    Login_File = open("login.txt", "a")
    Login_File.write(Username)
    Login_File.write(" ")
    Login_File.write(Password)
    Login_File.write("\n")
    Login_File.close()


def Search_Username(Username):                                         #Finds Password for User
    Login_File = open("login.txt","r")
    Users = Login_File.readlines()
    if len(Users) == 0:
        return False
    for User in Users:
        Current = User.split(" ")
        if Current[0] == Username:
            return True
    Login_File.close()
    return False

def Check_Cred(Username,Password):
    Login_File = open("login.txt","r")
    Users = Login_File.readlines()
    for User in Users:
        Current = User.split()
        if Current[0] == Username and Current[1] == Password:
            messagebox.showinfo("Login", "You are logged in!")
            LoginScreen.destroy()
            PARAMETER_SCREEN(Username)
            return True
    messagebox.showerror("Invalid Credentials", "Username or Password is incorrect")
    E1.delete(0,END)
    E2.delete(0,END)
    E3.delete(0,END)
    E4.delete(0,END)
    E5.delete(0,END)
    E6.delete(0,END)
    Login_File.close()

def Register(Username1, Password1, Username2, Password2):
    Login_File = open("login.txt","r")
    Users = Login_File.readlines()
    if len(Users)>=10:
        messagebox.showerror("Error", "Maximum number of users registered")
        E1.delete(0,END)
        E2.delete(0,END)
        E3.delete(0,END)
        E4.delete(0,END)
        E5.delete(0,END)
        E6.delete(0,END)
        return
    if Username1 != Username2 or Password1 != Password2:
        messagebox.showerror("Invalid Credentials", "Username or Password do not match")
        E1.delete(0,END)
        E2.delete(0,END)
        E3.delete(0,END)
        E4.delete(0,END)
        E5.delete(0,END)
        E6.delete(0,END)
        return
    print(Search_Username(Username1))
    if Search_Username(Username1) == False:
        messagebox.showinfo("Login", "User Created. You are logged in!")
        LoginScreen.destroy()

        Initialize_User(Username1)
        Create_New_User(Username1,Password1)
        PARAMETER_SCREEN(Username2)

    else:
        messagebox.showerror("Invalid Credentials", "This user already exists")
        E1.delete(0,END)
        E2.delete(0,END)
        E3.delete(0,END)
        E4.delete(0,END)
        E5.delete(0,END)
        E6.delete(0,END)
        return False



def LOGIN_SCREEN():

    LoginFrame.place(x=10,y=h-310)
    RegisterFrame.place(x=10,y=h-185)

    #LOGIN WIDGETS
    #Labels
    L1 = Label(LoginFrame, text="Username: ").place(x=5,y=5)
    L2 = Label(LoginFrame, text="Password: ").place(x=5,y=30)

    title = Label(LoginScreen, image=titleLogo)
    #title.place(x=w+30,y=20)
    title.place(x=10,y=10)


    B1 = ttk.Button(LoginFrame, text="Login",command=lambda :Check_Cred(E1.get(),E2.get()))

    #Place Widgets
    E1.place(x=110, y=5)
    E2.place(x=110, y=30)
    B1.place(x=5, y=65)

    #REGISTER WIDGETS
    #Labels
    L3 = Label(RegisterFrame, text="New Username: ").place(x=5,y=5)
    L4 = Label(RegisterFrame, text="New Password: ").place(x=5,y=30)
    L5 = Label(RegisterFrame, text="Verify Username: ").place(x=5,y=60)
    L6 = Label(RegisterFrame, text="Verify Password: ").place(x=5,y=85)



    B2 = ttk.Button(RegisterFrame, text="Register", command=lambda : Register(E3.get(),E4.get(),E5.get(),E6.get()))
    #B3 = ttk.Button(RegisterFrame, text="Register", command=lambda : Modes.PARAMETER_SCREEN()

    #Place Widgets
    E3.place(x=110, y=5)
    E4.place(x=110, y=30)
    E5.place(x=110, y=60)
    E6.place(x=110, y=85)

    B2.place(x=5, y=120)

    #Check Entry input
    valinp = LoginScreen.register(verify_login_alnum)
    E1.config(validate="key",validatecommand=(valinp,"%P"))
    E2.config(validate="key",validatecommand=(valinp,"%P"))
    E3.config(validate="key",validatecommand=(valinp,"%P"))
    E4.config(validate="key",validatecommand=(valinp,"%P"))
    E5.config(validate="key",validatecommand=(valinp,"%P"))
    E6.config(validate="key",validatecommand=(valinp,"%P"))

    mainloop()

LOGIN_SCREEN()
