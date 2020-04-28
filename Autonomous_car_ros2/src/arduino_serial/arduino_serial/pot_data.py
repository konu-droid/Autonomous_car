#!/usr/bin/env python3
from __future__ import print_function

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Int16MultiArray
from std_msgs.msg import MultiArrayLayout

#python
import serial
from time import sleep 

number_of_val = 3

ard = serial.Serial('/dev/ttyS0',9600, timeout = 1)
sleep(0.2)

class pot_data_publisher(Node):

    def __init__(self):
        super().__init__('pot_pubs')
        self.pot_pubs = self.create_publisher(Int16MultiArray, 'pot_data_pub',10)

    def pub(self):
        ard.write(b'm')

        for i in range(number_of_val):
            array.data[i] = int(ard.readline().decode())

        print(array)

        self.pot_pubs.publish(array)
        

def main():

    rclpy.init()

    global pot_pubs,array
    pot_pubs = pot_data_publisher()

    #init the array
    array = Int16MultiArray()
    array.data = [0,0,0]
    
    print(array)

    while True:

        try:
            pot_pubs.pub()
        except KeyboardInterrupt:
            break

    pot_pubs.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()