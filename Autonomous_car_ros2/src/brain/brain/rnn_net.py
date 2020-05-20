






# STILL NOT COMPLETED, SEE TRAIN.PY






















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

# lib for NN
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# set these according to gather_data.py 
scaling_factor = 0.75

width = 1280
height = 720
len_ard_data = 3

record_length = 500

save_net_path = '/home/autonomous-car/Desktop/Autonomous_car_ros2/src/data_store/network_store/rnn_net.pth'

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

    #resized (for a bigger network size)
    img = cv2.resize(img, (0,0), fx=scaling_factor, fy=scaling_factor)
    img2 = cv2.resize(img2, (0,0), fx=scaling_factor, fy=scaling_factor)

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
    radar_data[..., 0][radar_data[..., 0] >= height*scaling_factor] = (height*scaling_factor - 1)
    radar_data[..., 1][radar_data[..., 1] >= width*scaling_factor*2] = (width*scaling_factor*2 - 1) 

    img2[radar_data[..., 0], radar_data[..., 1]] = + radar_data1[..., 2]

    return img,img2


class RNN(nn.Module):
    def __init__(self, Input_size, H1_size, H2_size, H3_size, Out_size):
        super(RNN, self).__init__()

        self.IN = nn.Linear(Input_size, H1_size)

        self.hidden1 = nn.RNN(
            input_size=H1_size,
            hidden_size=H2_size,
            num_layers=3,
            nonlinearity='relu'
        )

        self.hidden2 = nn.Linear(H2_size, H3_size)

        self.out = nn.Linear(H3_size, Out_size)

    def forward(self, x, h_1):

        input_layer = F.relu(self.IN(x))

        # rnn layer
        h_2, h_n = self.hidden1(input_layer, h_1)

        h_3 = F.relu(self.hidden2(h_2))
        out_l = self.out(h_3)

        return out_l, h_n

def main():

    Input_size = int((height*scaling_factor)*(width*scaling_factor*2))
    H1_size = 300
    H2_size = 500
    H3_size = 500
    Out_size = 3

    final_Input_size = Out_size*3
    final_H1_size = 10
    final_H2_size = 10
    final_H3_size = 10

    rnn = RNN(Input_size, H1_size, H2_size,
              H3_size, Out_size)

    rnn2 = RNN(Input_size, H1_size, H2_size,
               H3_size, Out_size)

    rnn3 = RNN(len_ard_data, final_H1_size, final_H2_size,
               final_H3_size, Out_size)

    final = FF(final_Input_size, final_H1_size,
               final_H2_size, final_H3_size, Out_size)

    rclpy.init()

    global radar_subs, stereo_subs, edge_subs, ard_subs, bridge, store

    radar_subs = radar_substriber()
    stereo_subs = stereo_substriber()
    edge_subs = edge_substriber()
    #ard_subs = ard_substriber()
    bridge = CvBridge()

    count = 0
    count2 = 0
    store = np.zeros((int((height*scaling_factor)*(width*scaling_factor)*2)*2 + len_ard_data), dtype=np.float16)

    h_n = None
    h_n2 = None
    h_n3 = None

    start = datetime.now()

    for i in range(500):

        rnn.zero_grad()
            
        #rclpy.spin_once(ard_subs)
        rclpy.spin_once(edge_subs)
        rclpy.spin_once(radar_subs)
        rclpy.spin_once(stereo_subs)

        # normalization and sensor fusion
        input_a,input_b = add_image_radar(cv_image,edge_image,radar_data)

        input_a = torch.from_numpy(input_a)
        input_a = input_a.reshape(1, 1, Input_size).half().cuda()

        input_b = torch.from_numpy(input_b)
        input_b = input_b.reshape(1, 1, Input_size).half().cuda()

        #data_1 = ard_data
        #please normalize
        input_c = [1,2,3]
        input_c = torch.from_numpy(input_c)
        input_c = input_c.reshape(1, 1, len_ard_data).half().cuda()


        #The variables output and h_n were filling up the gpu
        #since these were directly generated they had required_grad = True
        #So with torch.no_grad() helps save the gpu ram by not recording these
        with torch.no_grad():
            output_a,h_n = rnn(input_a,h_n)
            output_b,h_n2 = rnn2(input_b,h_n2)
            output_c,h_n3 = rnn3(input_c,h_n3)

            #input
            final_input = torch.cat((output_a,output_b,output_c),1)
            final_input = final_input.reshape(1, 1, final_Input_size)

            output = final(final_input.cuda())

            '''
            #debuging the variable problem
            print(output.requires_grad)
            print(input.grad_fn)
            print(h_n.grad_fn)
            '''

        #print("output")
        print(output)
        

    done = datetime.now()

    time_taken = done - start
    print(str(time_taken) + "  Divide by 300")

if __name__ == '__main__':
    main()