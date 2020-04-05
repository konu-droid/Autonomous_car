# start: ros1 bridge,arduino_serial,stereo_yolo3 and ti__radar node and then use this

#!/usr/bin/env python3
from __future__ import print_function

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import PointCloud2
import point_cloud2 as pc2
from cv_bridge import CvBridge, CvBridgeError

import cv2
from datetime import datetime
import numpy as np
import pickle
from time import sleep

# for arduino
import serial

# set these according to run_this.py present in stereo_yolo3
fps = 60
width = 1280
height = 720
len_ard_data = 3

record_length = 1000

store_path = '/home/autonomous-car/Desktop/Autonomous_car_ros2/src/data_store/Data'


class stereo_substriber(Node):
    def __init__(self):
        super().__init__('stereo_graber')

        # reading stereo image data
        self.stereo_sub = self.create_subscription(
            Image, '/stereo_image', self.stereo_callback, 10)

        # To prevent unused variable warning
        self.stereo_sub

    def stereo_callback(self, data):
        bridge = CvBridge()
        global cv_image
        cv_image = bridge.imgmsg_to_cv2(data, "mono8")


class radar_substriber(Node):
    def __init__(self):
        super().__init__('radar_graber')
        # reading radar data from ros1
        self.radar_sub = self.create_subscription(
            PointCloud2, '/ti_mmwave/radar_scan_pcl', self.radar_callback, 10)

        # To prevent unused variable warning
        self.radar_sub

    def radar_callback(self, pointcloud):
        # we will only store the x,y,z values

        # print(pointcloud.data)
        global radar_data
        radar_data = pc2.pointcloud2_to_xyz_array(pointcloud, remove_nans=True)


def add_image_radar(ster_img, radar_data):
    # index of a array must be integer plus int16 for faster gpu processing
    radar_data = radar_data.astype(np.int16)

    # adjusting the range
    radar_data[..., 0][radar_data[..., 0] > 719] = 719
    radar_data[..., 1][radar_data[..., 1] > 1079] = 1079

    ster_img[radar_data[..., 0], radar_data[..., 1]] = radar_data[..., 2] + 255
    # for the second camera image
    ster_img[radar_data[..., 0], radar_data[..., 1] +
             1079] = radar_data[..., 2] + 255

    return ster_img


def main():
    # try-except is very important here as it catches the Ctrl-c command we send
    # from the command line, so that the code can do the pickle operation
    # and shutdown properly

    try:

        # arduino-serial
        #ser = serial.Serial('COM3',baudrate = 9600,timeout=1)

        rclpy.init()

        global radar_subs, stereo_subs, bridge, store

        radar_subs = radar_substriber()
        stereo_subs = stereo_substriber()
        bridge = CvBridge()

        count = 0
        count2 = 0
        store = np.zeros((record_length, (height*width*2) +
                          len_ard_data), dtype=np.int16)

        while True:
            rclpy.spin_once(stereo_subs)
            rclpy.spin_once(radar_subs)

            data_99 = add_image_radar(cv_image, radar_data)
            data = np.reshape(data_99, -1)

            '''
            ser.write(b'm')
            for i in 3:
                arduinoData = ser.readline().decode()
                data_1[i] = int(arduinoData)
            '''

            data_1 = [1, 2, 3]
            store[count, :] = np.append(data, data_1)
            # print(store)
            count = count+1
            print(count)

            '''
            print(np.shape(store))
            print(count)
            print(np.shape(data_99))
            print(np.shape(data_1))
            '''

            if count == record_length:
                '''
                #saving using pickel, takes a lot of space and slow
                with open(store_path + str(now) + '.pickle', 'wb') as f:
                    pickle.dump(store, f)
                '''

                # saving using numpy store in binary, less space and fast
                np.save(store_path + str(count2) + '.npy', store)

                print('storage done')
                count = 0
                count2 = count2 + 1

    except KeyboardInterrupt:
        stereo_subs.destroy_node()
        radar_subs.destroy_node()
        rclpy.shutdown()
        now = datetime.now()

        print('storage started')

        '''
        with open(store_path + str(now) + '.pickle', 'wb') as f:
            pickle.dump(store, f)
        '''

        # saving using numpy store in binary its faster then pickle
        np.save(store_path + str(count2) + '.npy', store)
        print('storage done: ' + str(now))


if __name__ == '__main__':
    main()
