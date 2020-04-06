#!/usr/bin/env python3
from __future__ import print_function

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

#python
import serial
from time import sleep 

ard = serial.Serial('/dev/ttyUSB0',9600)
sleep(0.2)

class cam_stop_substriber(Node):
    def __init__(self):
        super().__init__('stop_cam')
        #reading radar data from ros1
        self.cam_stop_sub = self.create_subscription(String,
        '/brake_pub', 
        self.cam_stop_callback,
        10)

        #To prevent unused variable warning
        self.cam_stop_sub
            
    def cam_stop_callback(self, data):
        msg.data = data.data

def main():
    #ros code
    rclpy.init()

    global cam_stop,msg

    msg = String()
    cam_stop = cam_stop_substriber()
    
    while True:
        rclpy.spin_once(cam_stop)
        if(msg.data == "Stop"):
            print("Stop")
            ard.write('0'.encode())
        else:
            print("Moving")
            ard.write('1'.encode())
        msg.data = "Move"


    cam_stop.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()