#ROS2 Lib
#!/usr/bin/env python3
from __future__ import print_function

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Int64

#python files
import tkinter as tk                # python 3
from tkinter import font  as tkfont # python 3
#import Tkinter as tk     # python 2
#import tkFont as tkfont  # python 2
from tkinter import *
import time
from tkinter import ttk
import webbrowser as wb
from time import sleep
import serial

ard = serial.Serial('/dev/ttyACM0', 9600)
sleep(2)

class action_publisher(Node):

    def __init__(self):
        super().__init__('my_action_pub')
        self.act_pubs = self.create_publisher(String, 'action_pub',10)

    def act_pub(self,data):
        self.act_pubs.publish(data)

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, Windows, HeadLights,AboutUs,FOR_REV,Indicators,power):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    

    


class StartPage(tk.Frame):

    def getBatteryInfo(self):
        global percentBar
        percentBar["value"]=90


    def GPS(self,url):
        wb.open_new(url)
   
    def SPEED(self):
        global SPEED
        print('50km/h')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        TOPS1 =Frame(self,width =1500,height =50,bg="Black",relief="raise",bd=8)
        TOPS1.pack(side=TOP,fill="both",expand="yes")

        BOTTOMS =Frame(self,width =1600,height =100,bg="orange",relief="raise",bd=8)
        BOTTOMS.pack(side=BOTTOM,fill="both")

        SIDELEFT =Frame(self,width =200,height =150,bg="Grey",relief="raise",bd=8)
        SIDELEFT.pack(side=LEFT,fill="both")


        SIDERIGHT =Frame(self,width =300,height =150,bg="powderBlue",relief="raise",bd=8)
        SIDERIGHT.pack(side=RIGHT,fill="both")

        MIDDLE =Frame(self,width =700,height =450,bg="Yellow",relief="raise",bd=8)
        MIDDLE.pack(side=TOP,fill="both")


        LOWER =Frame(self,width =700,height =150,bg="green",relief="raise",bd=8)
        LOWER.pack(side=BOTTOM,fill="both")

        lblinfo =Label(TOPS1,text="Autonomous Car",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        lblinfo.pack(side=LEFT,fill="both",expand="yes")

        #photo1 = #photoImage(file = r"C:\Users\Satyam\Downloads\google.png")
        
        button1 = Button(SIDERIGHT, text="GPS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        button1.pack(side=TOP,fill="both",expand="yes")

        button1.bind("<Button-1>",lambda e: self.GPS("/home/autonomous-car/Documents/gps/NanoGps.html"))
        
        #photo2 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\icons8-music-64.png')
        button2 =Button(SIDERIGHT,text="About Us",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("AboutUs"))
        button2.pack(side=TOP,fill="both",expand="yes")

        #photo3 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\telephone.png')
        button3 =Button(SIDERIGHT,text="HOME",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        button3.pack(side=TOP,fill="both",expand="yes")

        #photo4 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\speed.png')
        button4 =Button(LOWER,text="SPEED",font=('arial',20,'bold italic'),fg='Steel Blue',bd=2)
        button4.pack(side=LEFT,fill="both",expand="yes")
        StartPage.SPEED(self)

        button5=Button(LOWER,text="INDICATORS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("Indicators"))
        button5.pack(side=LEFT,fill="both",expand="yes")



        button6=Button(SIDELEFT,text="WINDOW",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("Windows"))
        button6.pack(side=TOP,fill="both",expand="yes")


        button7=Button(SIDELEFT,text="LIGHTS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("HeadLights"))
        button7.pack(side=TOP,fill="both",expand="yes")

 
        button8=Button(SIDELEFT,text="POWER",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,
        command=lambda: controller.show_frame("power"))
        button8.pack(side=TOP,fill="both",expand="yes")


        button9=Button(SIDELEFT,text="REVERSE",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("FOR_REV"))
        button9.pack(side=TOP,fill="both",expand="yes")
    
        labelinfo =Label(BOTTOMS,text="BATTERY STATUS",font=('Helvertica',30,'bold italic'),fg='Steel Blue',bd=2)
        labelinfo.pack(side=LEFT)

        percentBar= ttk.Progressbar(BOTTOMS,length=100 ,orient="horizontal",mode="determinate")
        percentBar.pack(side=TOP,fill="both",expand="yes")
        percentBar["maximum"]=100                      
        percentBar["value"]=00


class Windows(tk.Frame):

    

    def getBatteryInfo(self):
        global percentBar
        percentBar["value"]=90


    def GPS(url):
        webbrowser.open_new(url)
   
    def SPEED(self):
        global SPEED
        print('50km/h')
        
    def leftWindowUp(self):
        ard.write('a'.encode())
        sleep(0.1)
        data=ard.read(0)

    def leftWindowDown(self): 
        ard.write('b'.encode())
        sleep(0.1)
        data=ard.read(0)

    def rightWindowUp(self):
        ard.write('3'.encode())
        sleep(0.1)
        data=ard.read(0)

    def rightWindowDown(self):
        ard.write('4'.encode())
        sleep(0.1)
        data=ard.read(0)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        TOPS1 =Frame(self,width =1500,height =50,bg="Black",relief="raise",bd=8)
        TOPS1.pack(side=TOP,fill="both",expand="yes")

        BOTTOMS =Frame(self,width =1600,height =100,bg="orange",relief="raise",bd=8)
        BOTTOMS.pack(side=BOTTOM,fill="both")

        SIDELEFT =Frame(self,width =200,height =150,bg="Grey",relief="raise",bd=8)
        SIDELEFT.pack(side=LEFT,fill="both")


        SIDERIGHT =Frame(self,width =300,height =150,bg="powderBlue",relief="raise",bd=8)
        SIDERIGHT.pack(side=RIGHT,fill="both")

        MIDDLE =Frame(self,width =700,height =450,bg="Yellow",relief="raise",bd=8)
        MIDDLE.pack(side=TOP,fill="both")

        #photo1 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')

        #photoimage1 = #photo1.subsample(3, 3)

        button11 =Button(MIDDLE,padx=16,pady=14,text="Up",font=('Helvertica',20,'bold '),fg='Grey',bd=5,compound=LEFT, command=lambda : self.leftWindowUp())
        
        button11.place(x=170, y=130)

        #photo2 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        #photoimage2 = #photo2.subsample(3, 3)
        button12 =Button(MIDDLE,padx=14,pady=14,text="Down",font=('Helvertica',20,'bold'),fg='Grey',bd=5,compound=LEFT, command=lambda : self.leftWindowDown())
        
        button12.place(x=150,y=270)

        button13 =Button(MIDDLE,padx=16,pady=14,text="Up",font=('Helvertica',20,'bold '),fg='Grey',bd=5,compound=LEFT, command=lambda : self.rightWindowUp())
        #button1.pack(side=TOP,fill="both",expand="yes")
        button13.place(x=750, y=130)

        #photo4 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        #photoimage4 = #photo4.subsample(3, 3)
        button14 =Button(MIDDLE,padx=14,pady=14,text="Down",font=('Helvertica',20,'bold'),fg='Grey',bd=5,compound=LEFT, command=lambda : self.rightWindowDown())
        #button2.pack(side=LEFT,fill="both",expand="yes")
        button14.place(x=740,y=270)


        LOWER =Frame(self,width =700,height =150,bg="green",relief="raise",bd=8)
        LOWER.pack(side=BOTTOM,fill="both")

        lblinfo =Label(TOPS1,text="Autonomous Car",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        lblinfo.pack(side=LEFT,fill="both",expand="yes")


        #photo1 = tk.#photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        button1 = tk.Button(SIDERIGHT, text="GPS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        button1.pack(side=TOP,fill="both",expand="yes")
        
        #photo2 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\icons8-music-64.png')
        button2 =Button(SIDERIGHT,text="About Us",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("AboutUs"))
        button2.pack(side=TOP,fill="both",expand="yes")



        #photo3 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\telephone.png')
        button3 =Button(SIDERIGHT,text="HOME",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("StartPage"))
        button3.pack(side=TOP,fill="both",expand="yes")

        #photo4 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\speed.png')
        button4 =Button(LOWER,text="SPEED",font=('arial',20,'bold italic'),fg='Steel Blue',bd=2)
        button4.pack(side=LEFT,fill="both",expand="yes")
        

        button5=Button(LOWER,text="INDICATORS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("Indicators"))
        button5.pack(side=LEFT,fill="both",expand="yes")



        button6=Button(SIDELEFT,text="WINDOW",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,
                       command=lambda: controller.show_frame("Windows"))
        button6.pack(side=TOP,fill="both",expand="yes")


        button7=Button(SIDELEFT,text="LIGHTS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("HeadLights"))
        button7.pack(side=TOP,fill="both",expand="yes")

 
        button8=Button(SIDELEFT,text="POWER",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,
        command=lambda: controller.show_frame("power"))
        button8.pack(side=TOP,fill="both",expand="yes")


        button9=Button(SIDELEFT,text="REVERSE",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("FOR_REV"))
        button9.pack(side=TOP,fill="both",expand="yes")
    
        labelinfo =Label(BOTTOMS,text="BATTERY STATUS",font=('Helvertica',30,'bold italic'),fg='Steel Blue',bd=2)
        labelinfo.pack(side=LEFT)

        percentBar= ttk.Progressbar(BOTTOMS,length=100 ,orient="horizontal",mode="determinate")
        percentBar.pack(side=TOP,fill="both",expand="yes")
        percentBar["maximum"]=100                      
        percentBar["value"]=00
        
       


class HeadLights(tk.Frame):

   
    def getBatteryInfo(self):
        global percentBar
        percentBar["value"]=90


    def GPS(url):
        webbrowser.open_new(url)
   
    def SPEED(self):
        global SPEED
        print('50km/h')

    def headlightsOn(self):
        ard.write('5'.encode())
        sleep(0.1)
        data=ard.read(0)

    def headlightsOff(self):
        ard.write('6'.encode())
        sleep(0.1)
        data=ard.read(0)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        TOPS1 =Frame(self,width =1500,height =50,bg="Black",relief="raise",bd=8)
        TOPS1.pack(side=TOP,fill="both",expand="yes")

        BOTTOMS =Frame(self,width =1600,height =100,bg="orange",relief="raise",bd=8)
        BOTTOMS.pack(side=BOTTOM,fill="both")

        SIDELEFT =Frame(self,width =200,height =150,bg="Grey",relief="raise",bd=8)
        SIDELEFT.pack(side=LEFT,fill="both")


        SIDERIGHT =Frame(self,width =300,height =150,bg="powderBlue",relief="raise",bd=8)
        SIDERIGHT.pack(side=RIGHT,fill="both")

        MIDDLE =Frame(self,width =700,height =450,bg="Yellow",relief="raise",bd=8)
        MIDDLE.pack(side=TOP,fill="both")

        
        button11 =Button(MIDDLE,padx=16,pady=14,text="ON",font=('Helvertica',20,'bold '),fg='Grey',bd=5,compound=LEFT, command=lambda : self.headlightsOn())
        #button1.pack(side=TOP,fill="both",expand="yes")
        button11.place(x=350, y=200)

        #photo2 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        #photoimage2 = #photo2.subsample(3, 3)
        button12 =Button(MIDDLE,padx=14,pady=14,text="OFF",font=('Helvertica',20,'bold'),fg='Grey',bd=5,compound=LEFT, command=lambda : self.headlightsOff())
        #button2.pack(side=LEFT,fill="both",expand="yes")
        button12.place(x=500,y=200)


        LOWER =Frame(self,width =700,height =150,bg="green",relief="raise",bd=8)
        LOWER.pack(side=BOTTOM,fill="both")

        lblinfo =Label(TOPS1,text="Autonomous Car",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        lblinfo.pack(side=LEFT,fill="both",expand="yes")


        #photo1 = tk.#photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        button1 = tk.Button(SIDERIGHT, text="GPS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        button1.pack(side=TOP,fill="both",expand="yes")
        
        #photo2 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\icons8-music-64.png')
        button2 =Button(SIDERIGHT,text="About Us",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("AboutUs"))
        button2.pack(side=TOP,fill="both",expand="yes")

        #photo3 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\telephone.png')
        button3 =Button(SIDERIGHT,text="HOME",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("StartPage"))
        button3.pack(side=TOP,fill="both",expand="yes")

        #photo4 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\speed.png')
        button4 =Button(LOWER,text="SPEED",font=('arial',20,'bold italic'),fg='Steel Blue',bd=2)
        button4.pack(side=LEFT,fill="both",expand="yes")
        

        button5=Button(LOWER,text="INDICATORS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("Indicators"))
        button5.pack(side=LEFT,fill="both",expand="yes")

        button6=Button(SIDELEFT,text="WINDOW",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,
                       command=lambda: controller.show_frame("Windows"))
        button6.pack(side=TOP,fill="both",expand="yes")


        button7=Button(SIDELEFT,text="LIGHTS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("HeadLights"))
        button7.pack(side=TOP,fill="both",expand="yes")

 
        button8=Button(SIDELEFT,text="POWER",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,
        command=lambda: controller.show_frame("power"))
        button8.pack(side=TOP,fill="both",expand="yes")


        button9=Button(SIDELEFT,text="REVERSE",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("FOR_REV"))
        button9.pack(side=TOP,fill="both",expand="yes")
    
        labelinfo =Label(BOTTOMS,text="BATTERY STATUS",font=('Helvertica',30,'bold italic'),fg='Steel Blue',bd=2)
        labelinfo.pack(side=LEFT)

        percentBar= ttk.Progressbar(BOTTOMS,length=100 ,orient="horizontal",mode="determinate")
        percentBar.pack(side=TOP,fill="both",expand="yes")
        percentBar["maximum"]=100                      
        percentBar["value"]=00


class AboutUs(tk.Frame):


    def getBatteryInfo(self):
        global percentBar
        percentBar["value"]=90


    def GPS(url):
        webbrowser.open_new(url)
   
    def SPEED(self):
        global SPEED
        print('50km/h')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        TOPS1 =Frame(self,width =1500,height =50,bg="Black",relief="raise",bd=8)
        TOPS1.pack(side=TOP,fill="both",expand="yes")

        BOTTOMS =Frame(self,width =1600,height =100,bg="orange",relief="raise",bd=8)
        BOTTOMS.pack(side=BOTTOM,fill="both")

        SIDELEFT =Frame(self,width =200,height =150,bg="Grey",relief="raise",bd=8)
        SIDELEFT.pack(side=LEFT,fill="both")


        SIDERIGHT =Frame(self,width =300,height =150,bg="powderBlue",relief="raise",bd=8)
        SIDERIGHT.pack(side=RIGHT,fill="both")

        MIDDLE =Frame(self,width =700,height =450,bg="Yellow",relief="raise",bd=8)
        MIDDLE.pack(side=TOP,fill="both")

        
        button11 =Button(MIDDLE,padx=16,pady=14,text="ON",font=('Helvertica',20,'bold '),fg='Grey',bd=5,compound=LEFT)
        #button1.pack(side=TOP,fill="both",expand="yes")
        button11.place(x=350, y=200)

        #photo2 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        #photoimage2 = #photo2.subsample(3, 3)
        button12 =Button(MIDDLE,padx=14,pady=14,text="OFF",font=('Helvertica',20,'bold'),fg='Grey',bd=5,compound=LEFT)
        #button2.pack(side=LEFT,fill="both",expand="yes")
        button12.place(x=500,y=200)


        LOWER =Frame(self,width =700,height =150,bg="green",relief="raise",bd=8)
        LOWER.pack(side=BOTTOM,fill="both")

        lblinfo =Label(TOPS1,text="Autonomous Car",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        lblinfo.pack(side=LEFT,fill="both",expand="yes")


        #photo1 = tk.#photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        button1 = tk.Button(SIDERIGHT, text="GPS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        button1.pack(side=TOP,fill="both",expand="yes")
        
        #photo2 = tk.#photoImage(file = 'C:\\Users\\Satyam\\Downloads\\icons8-music-64.png')
        button2 =tk.Button(SIDERIGHT,text="About Us",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        button2.pack(side=TOP,fill="both",expand="yes")



        #photo3 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\telephone.png')
        button3 =Button(SIDERIGHT,text="HOME",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("StartPage"))
        button3.pack(side=TOP,fill="both",expand="yes")

        #photo4 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\speed.png')
        button4 =Button(LOWER,text="SPEED",font=('arial',20,'bold italic'),fg='Steel Blue',bd=2)
        button4.pack(side=LEFT,fill="both",expand="yes")
        

        button5=Button(LOWER,text="INDICATORS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("Indicators"))
        button5.pack(side=LEFT,fill="both",expand="yes")



        button6=Button(SIDELEFT,text="WINDOW",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,
                       command=lambda: controller.show_frame("Windows"))
        button6.pack(side=TOP,fill="both",expand="yes")


        button7=Button(SIDELEFT,text="LIGHTS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("HeadLights"))
        button7.pack(side=TOP,fill="both",expand="yes")

 
        button8=Button(SIDELEFT,text="POWER",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,
        command=lambda: controller.show_frame("power"))
        button8.pack(side=TOP,fill="both",expand="yes")


        button9=Button(SIDELEFT,text="REVERSE",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("FOR_REV"))
        button9.pack(side=TOP,fill="both",expand="yes")
    
        labelinfo =Label(BOTTOMS,text="BATTERY STATUS",font=('Helvertica',30,'bold italic'),fg='Steel Blue',bd=2)
        labelinfo.pack(side=LEFT)

        percentBar= ttk.Progressbar(BOTTOMS,length=100 ,orient="horizontal",mode="determinate")
        percentBar.pack(side=TOP,fill="both",expand="yes")
        percentBar["maximum"]=100                      
        percentBar["value"]=00

class FOR_REV(tk.Frame):

    def getBatteryInfo(self):
        global percentBar
        percentBar["value"]=90


    def GPS(url):
        webbrowser.open_new(url)
   
    def SPEED(self):
        global SPEED
        print('50km/h')

    def forward(self):
        ard.write("11".encode())
        sleep(0.1)
        msg.data = "Stop_cam"
        action_pubs.act_pub(msg)
        data=ard.read(0)

    def reverse(self):
        ard.write("12".encode())
        sleep(0.1)
        msg.data = "Rev_cam"
        action_pubs.act_pub(msg)
        data=ard.read(0)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        TOPS1 =Frame(self,width =1500,height =50,bg="Black",relief="raise",bd=8)
        TOPS1.pack(side=TOP,fill="both",expand="yes")

        BOTTOMS =Frame(self,width =1600,height =100,bg="orange",relief="raise",bd=8)
        BOTTOMS.pack(side=BOTTOM,fill="both")

        SIDELEFT =Frame(self,width =200,height =150,bg="Grey",relief="raise",bd=8)
        SIDELEFT.pack(side=LEFT,fill="both")


        SIDERIGHT =Frame(self,width =300,height =150,bg="powderBlue",relief="raise",bd=8)
        SIDERIGHT.pack(side=RIGHT,fill="both")

        MIDDLE =Frame(self,width =700,height =450,bg="Yellow",relief="raise",bd=8)
        MIDDLE.pack(side=TOP,fill="both")

        
        button11 =Button(MIDDLE,padx=16,pady=14,text="Forward",font=('Helvertica',20,'bold '),fg='Grey',bd=5,compound=LEFT, command=lambda : self.forward())
        #button1.pack(side=TOP,fill="both",expand="yes")
        button11.place(x=300, y=200)

        #photo2 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        #photoimage2 = #photo2.subsample(3, 3)
        button12 =Button(MIDDLE,padx=14,pady=14,text="Reverse",font=('Helvertica',20,'bold'),fg='Grey',bd=5,compound=LEFT, command=lambda : self.reverse())
        #button2.pack(side=LEFT,fill="both",expand="yes")
        button12.place(x=500, y=200)


        LOWER =Frame(self,width =700,height =150,bg="green",relief="raise",bd=8)
        LOWER.pack(side=BOTTOM,fill="both")

        lblinfo =Label(TOPS1,text="Autonomous Car",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        lblinfo.pack(side=LEFT,fill="both",expand="yes")


        #photo1 = tk.#photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        button1 = tk.Button(SIDERIGHT, text="GPS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        button1.pack(side=TOP,fill="both",expand="yes")
        
        #photo2 = tk.#photoImage(file = 'C:\\Users\\Satyam\\Downloads\\icons8-music-64.png')
        button2 =tk.Button(SIDERIGHT,text="About Us",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("AboutUs"))
        button2.pack(side=TOP,fill="both",expand="yes")



        #photo3 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\telephone.png')
        button3 =Button(SIDERIGHT,text="HOME",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("StartPage"))
        button3.pack(side=TOP,fill="both",expand="yes")

        #photo4 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\speed.png')
        button4 =Button(LOWER,text="SPEED",font=('arial',20,'bold italic'),fg='Steel Blue',bd=2)
        button4.pack(side=LEFT,fill="both",expand="yes")
        

        button5=Button(LOWER,text="INDICATORS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("Indicators"))
        button5.pack(side=LEFT,fill="both",expand="yes")



        button6=Button(SIDELEFT,text="WINDOW",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,
                       command=lambda: controller.show_frame("Windows"))
        button6.pack(side=TOP,fill="both",expand="yes")


        button7=Button(SIDELEFT,text="LIGHTS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("HeadLights"))
        button7.pack(side=TOP,fill="both",expand="yes")

 
        button8=Button(SIDELEFT,text="POWER",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,
        command=lambda: controller.show_frame("power"))
        button8.pack(side=TOP,fill="both",expand="yes")


        button9=Button(SIDELEFT,text="REVERSE",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("FOR_REV"))
        button9.pack(side=TOP,fill="both",expand="yes")
    
        labelinfo =Label(BOTTOMS,text="BATTERY STATUS",font=('Helvertica',30,'bold italic'),fg='Steel Blue',bd=2)
        labelinfo.pack(side=LEFT)

        percentBar= ttk.Progressbar(BOTTOMS,length=100 ,orient="horizontal",mode="determinate")
        percentBar.pack(side=TOP,fill="both",expand="yes")
        percentBar["maximum"]=100                      
        percentBar["value"]=00

class Indicators(tk.Frame):

    

    def getBatteryInfo(self):
        global percentBar
        percentBar["value"]=90


    def GPS(url):
        webbrowser.open_new(url)
   
    def SPEED(self):
        global SPEED
        print('50km/h')
        
    def leftIndicatorOn(self):
        ard.write('7'.encode())
        sleep(0.1)
        data=ard.read(0)

    def leftIndicatorOff(self):
        ard.write('8'.encode())
        sleep(0.1)
        data=ard.read(0)

    def rightIndicatorOn(self):
        ard.write('9'.encode())
        sleep(0.1)
        data=ard.read(0)

    def rightIndicatorOff(self):
        ard.write('0'.encode())
        sleep(0.1)
        data=ard.read(0)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        TOPS1 =Frame(self,width =1500,height =50,bg="Black",relief="raise",bd=8)
        TOPS1.pack(side=TOP,fill="both",expand="yes")

        BOTTOMS =Frame(self,width =1600,height =100,bg="orange",relief="raise",bd=8)
        BOTTOMS.pack(side=BOTTOM,fill="both")

        SIDELEFT =Frame(self,width =200,height =150,bg="Grey",relief="raise",bd=8)
        SIDELEFT.pack(side=LEFT,fill="both")


        SIDERIGHT =Frame(self,width =300,height =150,bg="powderBlue",relief="raise",bd=8)
        SIDERIGHT.pack(side=RIGHT,fill="both")

        MIDDLE =Frame(self,width =700,height =450,bg="Yellow",relief="raise",bd=8)
        MIDDLE.pack(side=TOP,fill="both")

        #photo1 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')

        #photoimage1 = #photo1.subsample(3, 3)

        button11 =Button(MIDDLE,padx=16,pady=14,text="On",font=('Helvertica',20,'bold '),fg='Grey',bd=5,compound=LEFT, command=lambda : self.leftIndicatorOn())
        
        button11.place(x=170, y=130)

        #photo2 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        #photoimage2 = #photo2.subsample(3, 3)
        button12 =Button(MIDDLE,padx=14,pady=14,text="Off",font=('Helvertica',20,'bold'),fg='Grey',bd=5,compound=LEFT, command=lambda : self.leftIndicatorOff())
        
        button12.place(x=150,y=270)

        button13 =Button(MIDDLE,padx=16,pady=14,text="On",font=('Helvertica',20,'bold '),fg='Grey',bd=5,compound=LEFT, command=lambda : self.rightIndicatorOn())
        #button1.pack(side=TOP,fill="both",expand="yes")
        button13.place(x=750, y=130)

        #photo4 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        #photoimage4 = #photo4.subsample(3, 3)
        button14 =Button(MIDDLE,padx=14,pady=14,text="Off",font=('Helvertica',20,'bold'),fg='Grey',bd=5,compound=LEFT, command=lambda : self.rightIndicatorOff())
        #button2.pack(side=LEFT,fill="both",expand="yes")
        button14.place(x=740,y=270)


        LOWER =Frame(self,width =700,height =150,bg="green",relief="raise",bd=8)
        LOWER.pack(side=BOTTOM,fill="both")

        lblinfo =Label(TOPS1,text="Autonomous Car",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        lblinfo.pack(side=LEFT,fill="both",expand="yes")


        #photo1 = tk.#photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        button1 = tk.Button(SIDERIGHT, text="GPS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        button1.pack(side=TOP,fill="both",expand="yes")
        
        #photo2 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\icons8-music-64.png')
        button2 =Button(SIDERIGHT,text="About Us",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("AboutUs"))
        button2.pack(side=TOP,fill="both",expand="yes")



        #photo3 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\telephone.png')
        button3 =Button(SIDERIGHT,text="HOME",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("StartPage"))
        button3.pack(side=TOP,fill="both",expand="yes")

        #photo4 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\speed.png')
        button4 =Button(LOWER,text="SPEED",font=('arial',20,'bold italic'),fg='Steel Blue',bd=2)
        button4.pack(side=LEFT,fill="both",expand="yes")
        

        button5=Button(LOWER,text="INDICATORS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        button5.pack(side=LEFT,fill="both",expand="yes")



        button6=Button(SIDELEFT,text="WINDOW",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,
                       command=lambda: controller.show_frame("Windows"))
        button6.pack(side=TOP,fill="both",expand="yes")


        button7=Button(SIDELEFT,text="LIGHTS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("HeadLights"))
        button7.pack(side=TOP,fill="both",expand="yes")

 
        button8=Button(SIDELEFT,text="POWER",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,
        command=lambda: controller.show_frame("power"))
        button8.pack(side=TOP,fill="both",expand="yes")


        button9=Button(SIDELEFT,text="REVERSE",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("FOR_REV"))
        button9.pack(side=TOP,fill="both",expand="yes")
    
        labelinfo =Label(BOTTOMS,text="BATTERY STATUS",font=('Helvertica',30,'bold italic'),fg='Steel Blue',bd=2)
        labelinfo.pack(side=LEFT)

        percentBar= ttk.Progressbar(BOTTOMS,length=100 ,orient="horizontal",mode="determinate")
        percentBar.pack(side=TOP,fill="both",expand="yes")
        percentBar["maximum"]=100                      
        percentBar["value"]=00

class power(tk.Frame):


    def getBatteryInfo(self):
        global percentBar
        percentBar["value"]=90


    def GPS(url):
        webbrowser.open_new(url)
   
    def SPEED(self):
        global SPEED
        print('50km/h')

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        TOPS1 =Frame(self,width =1500,height =50,bg="Black",relief="raise",bd=8)
        TOPS1.pack(side=TOP,fill="both",expand="yes")

        BOTTOMS =Frame(self,width =1600,height =100,bg="orange",relief="raise",bd=8)
        BOTTOMS.pack(side=BOTTOM,fill="both")

        SIDELEFT =Frame(self,width =200,height =150,bg="Grey",relief="raise",bd=8)
        SIDELEFT.pack(side=LEFT,fill="both")


        SIDERIGHT =Frame(self,width =300,height =150,bg="powderBlue",relief="raise",bd=8)
        SIDERIGHT.pack(side=RIGHT,fill="both")

        MIDDLE =Frame(self,width =700,height =450,bg="Yellow",relief="raise",bd=8)
        MIDDLE.pack(side=TOP,fill="both")

        
        button11 =Button(MIDDLE,padx=16,pady=14,text="ON",font=('Helvertica',20,'bold '),fg='Grey',bd=5,compound=LEFT)
        #button1.pack(side=TOP,fill="both",expand="yes")
        button11.place(x=350, y=200)

        #photo2 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        #photoimage2 = #photo2.subsample(3, 3)
        button12 =Button(MIDDLE,padx=14,pady=14,text="OFF",font=('Helvertica',20,'bold'),fg='Grey',bd=5,compound=LEFT)
        #button2.pack(side=LEFT,fill="both",expand="yes")
        button12.place(x=500,y=200)


        LOWER =Frame(self,width =700,height =150,bg="green",relief="raise",bd=8)
        LOWER.pack(side=BOTTOM,fill="both")

        lblinfo =Label(TOPS1,text="Autonomous Car",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        lblinfo.pack(side=LEFT,fill="both",expand="yes")


        #photo1 = tk.#photoImage(file = 'C:\\Users\\Satyam\\Downloads\\google.png')
        button1 = tk.Button(SIDERIGHT, text="GPS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        button1.pack(side=TOP,fill="both",expand="yes")
        
        #photo2 = tk.#photoImage(file = 'C:\\Users\\Satyam\\Downloads\\icons8-music-64.png')
        button2 =tk.Button(SIDERIGHT,text="About Us",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        button2.pack(side=TOP,fill="both",expand="yes")



        #photo3 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\telephone.png')
        button3 =Button(SIDERIGHT,text="HOME",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("StartPage"))
        button3.pack(side=TOP,fill="both",expand="yes")

        #photo4 = #photoImage(file = 'C:\\Users\\Satyam\\Downloads\\speed.png')
        button4 =Button(LOWER,text="SPEED",font=('arial',20,'bold italic'),fg='Steel Blue',bd=2)
        button4.pack(side=LEFT,fill="both",expand="yes")
        

        button5=Button(LOWER,text="INDICATORS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("Indicators"))
        button5.pack(side=LEFT,fill="both",expand="yes")



        button6=Button(SIDELEFT,text="WINDOW",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,
                       command=lambda: controller.show_frame("Windows"))
        button6.pack(side=TOP,fill="both",expand="yes")


        button7=Button(SIDELEFT,text="LIGHTS",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("HeadLights"))
        button7.pack(side=TOP,fill="both",expand="yes")

 
        button8=Button(SIDELEFT,text="POWER",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2)
        button8.pack(side=TOP,fill="both",expand="yes")


        button9=Button(SIDELEFT,text="REVERSE",font=('Helvertica',20,'bold italic'),fg='Steel Blue',bd=2,command=lambda: controller.show_frame("FOR_REV"))
        button9.pack(side=TOP,fill="both",expand="yes")
    
        labelinfo =Label(BOTTOMS,text="BATTERY STATUS",font=('Helvertica',30,'bold italic'),fg='Steel Blue',bd=2)
        labelinfo.pack(side=LEFT)

        percentBar= ttk.Progressbar(BOTTOMS,length=100 ,orient="horizontal",mode="determinate")
        percentBar.pack(side=TOP,fill="both",expand="yes")
        percentBar["maximum"]=100                      
        percentBar["value"]=00
        
def main():
    #ros code
    rclpy.init()
    global action_pubs,msg
    action_pubs = action_publisher()

    msg = String()
    app = SampleApp()
    app.mainloop()

    #paste this everywhere to want
    #action_pubs.act_pub(action)

    action_pubs.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()