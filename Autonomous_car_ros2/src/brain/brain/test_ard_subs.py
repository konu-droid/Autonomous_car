#!/usr/bin/env python3
from __future__ import print_function

import rclpy
from rclpy.node import Node

from std_msgs.msg import Int16MultiArray


import cv2
from datetime import datetime
import numpy as np
import pickle
from time import sleep


# set these according to gather_data.py 
scaling_factor = 0.75

width = 1280
height = 720
len_ard_data = 3

record_length = 500

save_net_path = '/home/autonomous-car/Desktop/Autonomous_car_ros2/src/data_store/network_store/rnn_net.pth'

# init the array
ard_data = Int16MultiArray()
ard_data.data = [0,0,0]


class ard_substriber(Node):
    def __init__(self):
        super().__init__('ard_grabber')

        # reading arduino data
        self.ard_sub = self.create_subscription(
            Int16MultiArray, '/pot_data_pub', self.ard_callback, 10)

        # To prevent unused variable warning
        self.ard_sub

    def ard_callback(self, data):
        global ard_data
        ard_data = data


def main():
    rclpy.init()
    ard_subs = ard_substriber()

    while(1):
        rclpy.spin_once(ard_subs)
        print(ard_data)


if __name__ == '__main__':
    main()