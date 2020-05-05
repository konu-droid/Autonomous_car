# start: ros1 bridge,arduino_serial,stereo_yolo3 and ti__radar node and then use this

#!/usr/bin/env python3
from __future__ import print_function

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from sensor_msgs.msg import Image
from std_msgs.msg import Int16MultiArray
from sensor_msgs.msg import PointCloud2
import point_cloud2 as pc2
from cv_bridge import CvBridge, CvBridgeError

import cv2
from datetime import datetime
import numpy as np
import pickle
from time import sleep

# set these according to run_this.py present in stereo_yolo3
fps = 60
width = 1280
height = 720
len_ard_data = 3

record_length = 500

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


class edge_substriber(Node):
    def __init__(self):
        super().__init__('edge_graber')

        # reading stereo image data
        self.edge_sub = self.create_subscription(
            Image, '/edge_image', self.edge_callback, 10)

        # To prevent unused variable warning
        self.edge_sub

    def edge_callback(self, data):
        bridge = CvBridge()
        global edge_image
        edge_image = bridge.imgmsg_to_cv2(data, "mono8")


class ard_substriber(Node):
    def __init__(self):
        super().__init__('ard_serial_graber')

        # reading stereo image data
        self.ard_sub = self.create_subscription(
            Int16MultiArray, '/pot_data_pub', self.ard_callback, 10)

        # To prevent unused variable warning
        self.ard_sub

    def ard_callback(self, data):
        global ard_data
        ard_data = data


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


def add_image_radar(img, img2, radar_data):

    #For faster compute
    img = img.astype(np.float16)
    img2 = img2.astype(np.float16)

    #Normalization
    img = np.divide(img, 255)
    img2 = np.divide(img2, 255)

    #had to copy it since float cant be index and we need meters as z axis, plus the array is pretty small radar doesnt pick many points
    radar_data1 = radar_data.astype(np.float16)

    # index of a array must be integer plus int16 for faster gpu processing, note: tried to change the dtype of just z axis but not possible
    radar_data = radar_data.astype(np.int16)

    # adjusting the range
    radar_data[..., 0][radar_data[..., 0] > height] = height - 1
    radar_data[..., 1][radar_data[..., 1] > width*2] = width*2 - 1

    img2[radar_data[..., 0], radar_data[..., 1]] = + radar_data1[..., 2]

    data = np.append(img,img2)

    return data


def main():
    # try-except is very important here as it catches the Ctrl-c command we send
    # from the command line, so that the code can do the pickle operation
    # and shutdown properly

    try:

        rclpy.init()

        global radar_subs, stereo_subs, edge_subs, ard_subs, bridge, store

        radar_subs = radar_substriber()
        stereo_subs = stereo_substriber()
        edge_subs = edge_substriber()
        #ard_subs = ard_substriber()
        bridge = CvBridge()

        count = 0
        count2 = 0
        store = np.zeros((record_length, (height*width*2)*2 +
                          len_ard_data), dtype=np.float16)

        while True:
            
            #rclpy.spin_once(ard_subs)
            rclpy.spin_once(edge_subs)
            rclpy.spin_once(radar_subs)
            rclpy.spin_once(stereo_subs)

            # normalization and sensor fusion
            data_99 = add_image_radar(cv_image,edge_image,radar_data)
            data = np.reshape(data_99, -1)

            #data_1 = ard_data
            data_1 = [1,2,3]

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
        edge_subs.destroy_node()
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
