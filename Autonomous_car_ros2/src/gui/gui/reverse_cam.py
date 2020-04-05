#!/usr/bin/env python3
from __future__ import print_function

import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import cv2
from time import sleep

class rev_cam_substriber(Node):
    def __init__(self):
        super().__init__('rev_cam')
        #reading radar data from ros1
        self.rev_cam_sub = self.create_subscription(String,
        '/action_pub', 
        self.rev_cam_callback,
        10)

        #To prevent unused variable warning
        self.rev_cam_sub
            
    def rev_cam_callback(self, data):
        msg.data = data.data
        pass

def main():
    #ros code
    rclpy.init()

    global rev_cam,msg

    msg = String()
    rev_cam = rev_cam_substriber()
    flag = 0
    while True:
        rclpy.spin_once(rev_cam)
        if msg.data == "Rev_cam":
            cap=cv2.VideoCapture(2)
            while True:
                ret, frame = cap.read()
                cv2.imshow('Reverse_Camera',frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cap.release()
            cv2.destroyAllWindows()
            
    rev_cam.destroy_node()
    rclpy.shutdown()
    

if __name__ == '__main__':
    main()
