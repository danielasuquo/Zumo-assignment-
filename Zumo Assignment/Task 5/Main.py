from tkinter import messagebox
import tkinter.font as tkFont
from time import sleep
import tkinter as tk
import threading
import Connect
import os

class App:
    Robot_MODE = "MANU"
    
    def __init__(self, root):
        #setting title
        root.title("Pololu Zumo Robot Control Interface : Task 5")
        root['background'] = '#d5dff0'
        #setting window size
        width=1524
        height=628
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        ft = tkFont.Font(family='Times',size=10)
        
        self.ForwardButton = tk.Button(root)
        self.ForwardButton["bg"] = "#efefef"
        self.ForwardButton["font"] = ft
        self.ForwardButton["fg"] = "#000000"
        self.ForwardButton["justify"] = "center"
        self.ForwardButton["text"] = "Forward"
        self.ForwardButton.place(x=290,y=160,width=180,height=80)
        self.ForwardButton["command"] = self.Forward

        self.BackwardButton = tk.Button(root)
        self.BackwardButton["bg"] = "#efefef"
        self.BackwardButton["font"] = ft
        self.BackwardButton["fg"] = "#000000"
        self.BackwardButton["justify"] = "center"
        self.BackwardButton["text"] = "Backward"
        self.BackwardButton.place(x=290,y=360,width=180,height=80)
        self.BackwardButton["command"] = self.Backward

        self.RightButton = tk.Button(root)
        self.RightButton["bg"] = "#efefef"
        self.RightButton["font"] = ft
        self.RightButton["fg"] = "#000000"
        self.RightButton["justify"] = "center"
        self.RightButton["text"] = "Right"
        self.RightButton.place(x=490,y=260,width=180,height=80)
        self.RightButton["command"] = self.Right

        self.LeftButton=tk.Button(root)
        self.LeftButton["bg"] = "#efefef"
        self.LeftButton["font"] = ft
        self.LeftButton["fg"] = "#000000"
        self.LeftButton["justify"] = "center"
        self.LeftButton["text"] = "Left"
        self.LeftButton.place(x=90,y=260,width=180,height=80)
        self.LeftButton["command"] = self.Left

        self.StopButton = tk.Button(root)
        self.StopButton["bg"] = "#efefef"
        self.StopButton["font"] = ft
        self.StopButton["fg"] = "#000000"
        self.StopButton["justify"] = "center"
        self.StopButton["text"] = "STOP"
        self.StopButton.place(x=290,y=260,width=180,height=80)
        self.StopButton["command"] = self.Stop

        self.AUTOButton=tk.Button(root)
        self.AUTOButton["bg"] = "#efefef"
        self.AUTOButton["font"] = ft
        self.AUTOButton["fg"] = "#000000"
        self.AUTOButton["justify"] = "center"
        self.AUTOButton["text"] = "Change mode"
        self.AUTOButton.place(x=636,y=460,width=180,height=80)
        self.AUTOButton["command"] = self.ChangeMode

        self.RightGyroButton = tk.Button(root)
        self.RightGyroButton["bg"] = "#efefef"
        self.RightGyroButton["font"] = ft
        self.RightGyroButton["fg"] = "#000000"
        self.RightGyroButton["justify"] = "center"
        self.RightGyroButton["text"] = "90 Degrees Right"
        self.RightGyroButton.place(x=1254,y=210,width=180,height=80)
        self.RightGyroButton["command"] = self.GyroRight

        self.LeftGyroButton = tk.Button(root)
        self.LeftGyroButton["bg"] = "#efefef"
        self.LeftGyroButton["font"] = ft
        self.LeftGyroButton["fg"] = "#000000"
        self.LeftGyroButton["justify"] = "center"
        self.LeftGyroButton["text"] = "90 Degrees Left"
        self.LeftGyroButton.place(x=954,y=210,width=180,height=80)
        self.LeftGyroButton["command"] = self.GyroLeft

        self.RightSearchButton = tk.Button(root)
        self.RightSearchButton["bg"] = "#efefef"
        self.RightSearchButton["font"] = ft
        self.RightSearchButton["fg"] = "#000000"
        self.RightSearchButton["justify"] = "center"
        self.RightSearchButton["text"] = "Search Right Room"
        self.RightSearchButton.place(x=1254,y=310,width=180,height=80)
        self.RightSearchButton["command"] = self.SearchRight

        self.LeftSearchButton = tk.Button(root)
        self.LeftSearchButton["bg"] = "#efefef"
        self.LeftSearchButton["font"] = ft
        self.LeftSearchButton["fg"] = "#000000"
        self.LeftSearchButton["justify"] = "center"
        self.LeftSearchButton["text"] = "Search Left Room"
        self.LeftSearchButton.place(x=954,y=310,width=180,height=80)
        self.LeftSearchButton["command"] = self.SearchLeft

        Main_Label_0=tk.Label(root)
        ft = tkFont.Font(family='Times',size=18)
        Main_Label_0["font"] = ft
        Main_Label_0["fg"] = "#333333"
        Main_Label_0["background"] = "#d5dff0"
        Main_Label_0["justify"] = "center"
        Main_Label_0["text"] = " Pololu Zumo 32U4 robot"
        Main_Label_0.place(x=641,y=10,width=251,height=37)

        Main_Label_1=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        Main_Label_1["font"] = ft
        Main_Label_1["fg"] = "#333333"
        Main_Label_1["background"] = "#d5dff0"
        Main_Label_1["justify"] = "center"
        Main_Label_1["text"] = "Manual control interface"
        Main_Label_1.place(x=690,y=40,width=166,height=30)

        Main_Label_2=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        Main_Label_2["font"] = ft
        Main_Label_2["fg"] = "#333333"
        Main_Label_2["background"] = "#d5dff0"
        Main_Label_2["justify"] = "center"
        Main_Label_2["text"] = "The Zumo can be driven using \n w, a, s, d and  ‘Space’ ‘buttons’ \n or \nthe following buttons"
        Main_Label_2["relief"] = "flat"
        Main_Label_2.place(x=570,y=70,width=400,height=61)

        self.State_Label_0=tk.Label(root)
        ft = tkFont.Font(family='Times',size=10)
        self.State_Label_0["font"] = ft
        self.State_Label_0["fg"] = "#333333"
        self.State_Label_0["justify"] = "center"
        self.State_Label_0["text"] = "Robot Current mode : Manual"
        self.State_Label_0.place(x=630,y=560,width=200,height=30)

    def Forward(self):
        Connect.Forward()


    def Backward(self):
        Connect.Backward()


    def Right(self):
        Connect.Right()

    def GyroRight(self):
        Connect.GyroRight()

    def Left(self):
        Connect.Left()

    def GyroLeft(self):
        Connect.GyroLeft()

    def SearchLeft(self):
        self.State_Label_0["text"] = "Robot Searching Left Room"
        Connect.SearchLeft()

    def SearchRight(self):
        self.State_Label_0["text"] = "Robot Searching Right Room"
        Connect.SearchRight()
        
    def Stop(self):
        Connect.Stop()

    def ChangeMode(self):
        self.Robot_MODE = Connect.Get_Mode()
        if self.Robot_MODE == "MANU":
            self.Robot_MODE = "AUTO"
            self.to_auto()
            Connect.AUTO()
            
        elif self.Robot_MODE == "AUTO":
            self.Robot_MODE = "MANU"
            self.to_Manu()
            Connect.MANU()

    def to_manu(self):
        self.ForwardButton["state"] = "normal"
        self.BackwardButton["state"] = "normal"
        self.LeftButton["state"] = "normal"
        self.RightButton["state"] = "normal"
        self.State_Label_0["text"] = "Robot Current mode : Manual"

    def to_auto(self):
        self.ForwardButton["state"] = "disabled"
        self.BackwardButton["state"] = "disabled"
        self.LeftButton["state"] = "disabled"
        self.RightButton["state"] = "disabled"
        self.State_Label_0["text"] = "Robot Current mode : Autonomous"
            
    def Robot_State(self):
        while True:
            #self.Robot_MODE = Connect.Get_Mode()
            if self.Robot_MODE == "AUTO" and Connect.Get_Mode() == "MANU":
                self.Robot_MODE = "MANU"
                self.to_manu()
                
            sleep(0.5)
        
def event_handle(event):
    # Replace the window's title with event.type: input key
    print("{}: {}".format(str(event.type), event.char))
    if event.char == 'w':
        Connect.Forward()
    elif event.char == 's':
        Connect.Backward()
    elif event.char == 'a':
        Connect.Left()
    elif event.char == 'd':
        Connect.Right()
    elif event.char == 'c':
        Connect.AUTO()
    elif event.char == 'r':
        Connect.GyroRight()
    elif event.char == 'l':
        Connect.GyroLeft()
    else:
        Connect.Stop()
            
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        print("Exiting......")
        print("Good By !!")
        os._exit(0)


if __name__ == "__main__":
    Robot_MODE = "AUTO"
    
    root = tk.Tk()
    event_sequence = '<KeyPress>'
    root.bind(event_sequence, event_handle)
    root.bind('<KeyRelease>', event_handle)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    app = App(root)

    t1 = threading.Thread(target=app.Robot_State)
    # starting thread 1 to keep track of robot state
    t1.start()
    
    root.mainloop()
