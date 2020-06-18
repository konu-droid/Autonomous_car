import serial
import urllib.request, json
from html.parser import HTMLParser
import pandas as pd
import csv
from firebase import firebase
#mydata1=[]
#mydata2=[]
firebase = firebase.FirebaseApplication('https://nanofirebase-f05f2.firebaseio.com/', None)

while True:
       endpoint = 'https://maps.googleapis.com/maps/api/directions/json?'
       api_key = 'AIzaSyAmzIOAIDi0WALXH6NrwVl-gRNlOSjkPTk'
       result1 = firebase.get('location/latLng/position','latitude')
       result2 = firebase.get('location/latLng/position','longitude')
       data1=str(result1)
       data2=str(result2)
       print(result1)
       print(result2)
       result=data1+","+data2
       print(result)
       print("Taken the Vehicle address")
       result5 = firebase.get('Destination','latitude')
       result6 = firebase.get('Destination','longitude')
       print(result5)
       print(result6)
       data3=str(result5)
       data4=str(result6)
       #print(result1)
       #print(result2)
       result1=data3+","+data4
       print(result1)
       print("Taken the Destination address")
       if result=="" and result1=="":
          print("location not identified")
          break
       else:
       #destination = input('Where do you want to go?: ').replace(' ','+')
          nav_request = 'origin={}&destination={}&key={}'.format(result,result1,api_key)
          request = endpoint + nav_request
          response = urllib.request.urlopen(request).read()
          directions = json.loads(response)
          print(directions)
          with open(r"/home/autonomous-car/Documents/gps_csv_files/gps.csv","w+",newline='')as csvfile:
         #writer=csv.writer(csvfile, delimiter=',', lineterminator='\n')
               csvfile.truncate()
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
                       df1.to_csv(r'/home/autonomous-car/Documents/gps_csv_files/gps.csv',mode='a',header=False,index=False)
             #print(df1.head)
     
          break
               