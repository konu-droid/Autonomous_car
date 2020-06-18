import serial
import urllib.request, json
from html.parser import HTMLParser
import pandas as pd
import csv
from firebase import firebase
#mydata1=[]
#mydata2=[]
firebase = firebase.FirebaseApplication('https://nanofirebase-f05f2.firebaseio.com/', None)
arduino = serial.Serial('COM9',9600)
while True:
       endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
       api_key = 'AIzaSyAmzIOAIDi0WALXH6NrwVl-gRNlOSjkPTk'
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
          
          

          result1 = firebase.get('location/latLng/position','latitude')
          result2 = firebase.get('location/latLng/position','longitude')
          data1=str(result1)
          data2=str(result2)
       #print(result1)
       #print(result2)
          result=data1+","+data2
          print(result)
          print("Taken the destination address")
          result3 = firebase.put('/vehicle/-M0HQwBrw89v0aL9cq-E', 'latitude',s1)
          result4 = firebase.put('/vehicle/-M0HQwBrw89v0aL9cq-E', 'longitude',s2)
          print("record updated")
          if result=="":
             print("location not identified")
             break
          else:
       #destination = input('Where do you want to go?: ').replace(' ','+')
             nav_request = 'origin={}&destination={}&key={}'.format(origin,result,api_key)
             request = endpoint + nav_request
             response = urllib.request.urlopen(request).read()
             directions = json.loads(response)
             print(directions)
             with open(r"C:\Users\vemir\OneDrive\Documents\gps2.csv","w+",newline='')as csvfile:
         #writer=csv.writer(csvfile, delimiter=',', lineterminator='\n')
                  csvfile.truncate();
                  csvfile.close()
                  for i in range (0, len (directions['routes'][0]['legs'][0]['steps'])):
                      j = directions['routes'][0]['legs'][0]['steps'][i]['html_instructions']
                      k = directions['routes'][0]['legs'][0]['steps'][i]['distance']['text']
                      print(j)
                      print(k)
                      mydata2=[]
             
                      mydata1=[]
                      mydata2.append(k)
                      class MyHTMLParser(HTMLParser):
                           def handle_starttag(self, tag, attrs):
                               print("Found a start tag:", tag)

                           def handle_endtag(self, tag):
                               print("Found an end tag :", tag)

                           def handle_data(self, data):
                               print("Found some data  :", data)
                               mydata1.append(data)
                          
                      parser = MyHTMLParser()
                      parser.feed(j)
                      for i in mydata1:
                          mydata2.append(i)
                      #asdd
                      df = pd.DataFrame(mydata2)
                      df1=df.transpose()
                      df1.to_csv(r'C:\Users\vemir\OneDrive\Documents\gps2.csv',mode='a',header=False,index=False)
             #print(df1.head)
     
          break
               