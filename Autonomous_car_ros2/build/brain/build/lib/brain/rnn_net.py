






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

#lib for NN
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

# set these according to run_this.py present in stereo_yolo3
fps = 60
width = 1280
height = 720
len_ard_data = 3

record_length = 500

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


class RNN(nn.Module):
    def __init__(self, Input_size, H1_size, H2_size, H3_size, Out_size):
        super(RNN, self).__init__()

        self.IN = nn.Linear(Input_size, H1_size)

        self.hidden1 = nn.RNN(
            input_size=H1_size,
            hidden_size=H2_size,
            num_layers=2,
            nonlinearity='relu'
        )

        self.hidden2 = nn.Linear(H2_size, H3_size)

        self.out = nn.Linear(H3_size, Out_size)

    def forward(self, x, h_1):

        input_layer = self.IN(x)
        input_layer = F.relu(input_layer)

        '''
        #one of the method to do it
        # Initialize hidden state with zeros
        # (layer_dim, batch_size, hidden_dim)
        h0 = torch.zeros(1, x.size(0), 40).cuda()

        # We need to detach the hidden state to prevent exploding/vanishing gradients
        # This is part of truncated backpropagation through time (BPTT)
        # rnn layer
        h_2, h_n = self.hidden1(input_layer, h0.detach())
        '''

        # rnn layer
        h_2, h_n = self.hidden1(input_layer, h_1)

        h_3 = self.hidden2(h_2)
        h_3 = F.relu(h_3)
        out_l = self.out(h_3)

        return out_l, h_n


if __name__ == '__main__':
    Input_size = 100
    H1_size = 50
    H2_size = 40
    H3_size = 30
    H4_size = 20
    H5_size = 10
    Out_size = 5

    rnn =RNN(Input_size,H1_size,H2_size,H3_size,H4_size,H5_size,Out_size)
    #print(rnn)

    #load the trained network parameters (edit it for the path and loop)
    # open a file, where you stored the pickled data
    file = open('name_of_the_file', 'rb')

    # dump information to that file
    network_para = pickle.load(file)

    # close the file
    file.close()
    
    #loss func and optimizer
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(rnn.parameters(), lr =0.1)

    #init for rnn hidden
    output,h_n = rnn(input_a,None)

    #make a loop from here
    output1,h = rnn(input_a,h_n)
    print(output)