import csv 
import serial
people=[]
people1=[]
temp=0
import time


f=open(r'/home/autonomous-car/Documents/gps_csv_files/gps.csv','r')
reader1=csv.reader(f)
for rows in reader1:
    
    #print(rows[0],rows[2])
    s=rows[0].find("k")
    if(s==-1):
       output=rows[0]
       #print(output,rows[2])
       people.append([int(output),rows[2]])
    else:
        d=rows[0].strip("k")
        s1=float(d)
        #s2=int(s1)
        output=s1*1000
        #print(output,rows[2])
        people.append([int(output),rows[2]])
    

             
def directions_toArduino(a,b):
    print("the first segment is reached with values {} and {}".format(a,b))
    
    
    

sum=0

for item in people:
    print(item[0])
    while True:
      
          a=1
          sum=sum+a
          print(sum)
      
          time.sleep(.1)
          if(sum==item[0]):
             print("reached",item[1])
             directions_toArduino(item[0],item[1])
             break
    
    
 
      
        
    

    
