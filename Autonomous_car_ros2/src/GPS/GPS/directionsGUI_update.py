 
from tkinter import *  
import urllib.request, json
import tkinter as tk  
import pandas as pd
from html.parser import HTMLParser
import csv
import serial
arduino = serial.Serial('COM9',9600)
endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
api_key = 'AIzaSyAmzIOAIDi0WALXH6NrwVl-gRNlOSjkPTk'
def call_result(): 
    data = arduino.readline().strip()
    data1=data.decode('ascii')
    s=str(data1)
    #print(s)
    if s == 'A':
       data = arduino.readline().strip()
       data1=data.decode('ascii')
       s1=str(data1)
       print(s1)
       data = arduino.readline().strip()
       data1=data.decode('ascii')
       s2=str(data1)
       print(s2)
       origin=s1+","+s2
       print(origin)
    #num1 = number1.get().replace(' ','+') 
       num2 = number2.get().replace(' ','+')  
       nav_request = 'origin={}&destination={}&key={}'.format(origin,num2,api_key)
       request = endpoint + nav_request
#Sends the request and reads the response.
       response = urllib.request.urlopen(request).read()
#Loads response as JSON
       directions = json.loads(response)
       with open(r"C:\Users\vemir\OneDrive\Documents\gps2.csv","w+",newline='')as csvfile:
         #writer=csv.writer(csvfile, delimiter=',', lineterminator='\n')
            csvfile.truncate()
            csvfile.close()
            for i in range (0, len (directions['routes'][0]['legs'][0]['steps'])):
                j = directions['routes'][0]['legs'][0]['steps'][i]['html_instructions']
                k1 = directions['routes'][0]['legs'][0]['steps'][i]['distance']['text']
                print(j)
                print(k1)
             
                w=k1.strip("m")
            # mydata1=[None]*len (directions['routes'][0]['legs'][0]['steps'])
                mydata2=[]
             
                mydata1=[]
             
                mydata2.append(w)
                class MyHTMLParser(HTMLParser):
                  
                      def handle_starttag(self, tag, attrs):
                          print("Found a start tag:", tag)

                      def handle_endtag(self, tag):
                          print("Found an end tag :", tag)

                      def handle_data(self, data):
                          print("Found some data  :", data)
                          mydata1.append(data)
                       
                       #self.gps=str(data)
                       

        
                parser = MyHTMLParser()
                parser.feed(j)
                for i in mydata1:
                    mydata2.append(i)
             #writer.writerow([mydata2])
                df = pd.DataFrame(mydata2)
             
                df1=df.transpose()
                df1.to_csv(r'C:\Users\vemir\OneDrive\Documents\gps2.csv',mode='a',header=False,index=False)
                #print(df1.head)
             


   
parent = Tk()  

parent.geometry('400x200+100+200')  
number1 = tk.StringVar()  
number2 = tk.StringVar()  

#Start = Label(parent,text = "Starting address",fg="red").grid(row = 0, column = 0)  
#origin = Entry(parent,textvariable=number1).grid(row = 0, column = 1)  
end = Label(parent,text = "Destination address",fg="red").grid(row = 1, column = 0)  
destination = Entry(parent,textvariable=number2).grid(row = 1, column = 1)  
submit = Button(parent, text = "Submit",command=call_result).grid(row = 4, column = 0) 
 

parent.mainloop()  