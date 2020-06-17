#!/usr/bin/env python3
from __future__ import print_function

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import MultiArrayLayout

# python
import serial
from time import sleep
import numpy as np

# init the array
array = Int16MultiArray()
array.data = [0,0,0]


class pot_data_publisher2(Node):

    def __init__(self):
        super().__init__('pot_pubs2')
        self.pot_pubs2 = self.create_publisher(Int16MultiArray, 'pot_data_pub2', 10)

    def pub(self):
        

        print(array)


        self.pot_pubs2.publish(array)


def main():

    rclpy.init()

    pot_pubs2 = pot_data_publisher2()

    while True:
        try:
            pot_pubs2.pub()
        except:
            break

    pot_pubs2.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
