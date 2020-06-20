#!/usr/bin/env python3
from __future__ import print_function

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_msgs.msg import Int16
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

import torch
import cv2
import numpy as np
from torch.autograd import Variable
from darknet import Darknet
from util import process_result, load_images, resize_image, cv_image2tensor, transform_result
import pickle as pkl
import argparse
import math
import random
import os.path as osp
import os
import sys
from datetime import datetime

desired_height = 720
desired_width = 1280


class my_stereo_image_publisher(Node):

    def __init__(self,model,args):
        super().__init__('my_stereo_image_publisher')
        self.img_pub = self.create_publisher(Image, 'stereo_image', 10)
        self.ed_pub = self.create_publisher(Image, 'edge_image', 10)

    def image_pub(self,data,data2):

        try:
            self.img_pub.publish(bridge.cv2_to_imgmsg(data, "mono8"))
        except CvBridgeError as e:
            print(e)
        try:
            self.ed_pub.publish(bridge.cv2_to_imgmsg(data2, "mono8"))
        except CvBridgeError as e:
            print(e)

def load_classes(namesfile):
    fp = open(namesfile, "r")
    names = fp.read().split("\n")[:-1]
    return names


def parse_args():
    parser = argparse.ArgumentParser(description='YOLOv3 object detection')
    #parser.add_argument('-i', '--input', required=True, help='input image or directory or video')
    parser.add_argument('-i', '--input', default=0,
                        help='input image or directory or video')
    parser.add_argument('-t', '--obj-thresh', type=float,
                        default=0.5, help='objectness threshold, DEFAULT: 0.5')
    parser.add_argument('-n', '--nms-thresh', type=float, default=0.4,
                        help='non max suppression threshold, DEFAULT: 0.4')
    parser.add_argument('-o', '--outdir', default='/home/konu/Desktop/Autonomous_car_ros2/src/stereo_yolo3/stereo_yolo3/detection',
                        help='output directory, DEFAULT: detection/')
    parser.add_argument('-v', '--video', action='store_true',
                        default=True, help='flag for detecting a video input')
    parser.add_argument('-w', '--webcam', action='store_true',  default=True,
                        help='flag for detecting from webcam. Specify webcam ID in the input. usually 0 for a single webcam connected')
    parser.add_argument('--cuda', action='store_true',
                        default=True, help='flag for running on GPU')
    parser.add_argument('--no-show', action='store_true', default=False,
                        help='do not show the detected video in real time')
    parser.add_argument('--ros-args', action='store_true',
                        default=True, help='ROS argument')

    args = parser.parse_args()

    return args


def create_batches(imgs, batch_size):
    num_batches = math.ceil(len(imgs) // batch_size)
    batches = [imgs[i*batch_size: (i+1)*batch_size]
               for i in range(num_batches)]

    return batches


def draw_bbox(imgs, bbox, colors, classes):
    img = imgs[int(bbox[0])]
    label = classes[int(bbox[-1])]
    p1 = tuple(bbox[1:3].int())
    p2 = tuple(bbox[3:5].int())
    color = random.choice(colors)
    cv2.rectangle(img, p1, p2, color, 2)

    text_size = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1, 1)[0]
    p3 = (p1[0], p1[1] - text_size[1] - 4)
    p4 = (p1[0] + text_size[0] + 4, p1[1])
    cv2.rectangle(img, p3, p4, color, -1)
    cv2.putText(img, label, p1, cv2.FONT_HERSHEY_SIMPLEX,
                1, [225, 255, 255], 1)


def detect_video(model, args):
    input_size = [int(model.net_info['height']), int(model.net_info['width'])]

    colors = pkl.load(open(
        "/home/autonomous-car/Desktop/Autonomous_car_ros2/src/stereo_yolo3/stereo_yolo3/pallete", "rb"))
    classes = load_classes(
        "/home/autonomous-car/Desktop/Autonomous_car_ros2/src/stereo_yolo3/stereo_yolo3/data/coco.names")
    colors = [colors[1]]
    if args.webcam:
        cap1 = cv2.VideoCapture(int(args.input))
        cap2 = cv2.VideoCapture(int(args.input)+2)
        output_path = osp.join(args.outdir, 'dete_webcam.avi')
    else:
        cap1 = cv2.VideoCapture(int(args.input))
        cap2 = cv2.VideoCapture(int(args.input)+2)
        output_path = osp.join(args.outdir, 'dete_' +
                               osp.basename(args.input).rsplit('.')[0] + '.avi')

    cap1.set(3, desired_width)
    cap1.set(4, desired_height)
    cap2.set(3, desired_width)
    cap2.set(4, desired_height)
    width, height = int(cap1.get(3))*2, int(cap1.get(4))
    fps = cap1.get(cv2.CAP_PROP_FPS)
    print(width)
    print(height)

    print('Detecting...')

    while cap1.isOpened():
        retflag, frame1 = cap1.read()
        retflag, frame2 = cap2.read()
        frame = np.concatenate((frame1, frame2), axis=1)

        # edge detection
        edge = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edge = cv2.Canny(edge, 100, 200)

        
        if retflag:
            frame_tensor = cv_image2tensor(frame, input_size).unsqueeze(0)
            frame_tensor = Variable(frame_tensor)

            if args.cuda:
                frame_tensor = frame_tensor.cuda()

            detections = model(frame_tensor, args.cuda).cpu()
            detections = process_result(
                detections, args.obj_thresh, args.nms_thresh)
            if len(detections) != 0:
                detections = transform_result(detections, [frame], input_size)
                for detection in detections:
                    draw_bbox([frame], detection, colors, classes)

            if not args.no_show:
                cv2.imshow('frame', frame)

            gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            stereo_image_pub.image_pub(gray_scale,edge)

            if not args.no_show and cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    cap1.release()
    cap2.release()
    if not args.no_show:
        cv2.destroyAllWindows()
    

    return


def detect_image(model, args):

    print('Loading input image(s)...')
    input_size = [int(model.net_info['height']), int(model.net_info['width'])]
    batch_size = int(model.net_info['batch'])

    imlist, imgs = load_images(args.input)
    print('Input image(s) loaded')

    img_batches = create_batches(imgs, batch_size)

    # load colors and classes
    colors = pkl.load(open(
        "/home/autonomous-car/Desktop/Autonomous_car_ros2/src/stereo_yolo3/stereo_yolo3/pallete", "rb"))
    classes = load_classes(
        "/home/autonomous-car/Desktop/Autonomous_car_ros2/src/stereo_yolo3/stereo_yolo3/data/coco.names")

    if not osp.exists(args.outdir):
        os.makedirs(args.outdir)

    start_time = datetime.now()
    print('Detecting...')
    for batchi, img_batch in enumerate(img_batches):
        img_tensors = [cv_image2tensor(img, input_size) for img in img_batch]
        img_tensors = torch.stack(img_tensors)
        img_tensors = Variable(img_tensors)
        if args.cuda:
            img_tensors = img_tensors.cuda()
        detections = model(img_tensors, args.cuda).cpu()
        detections = process_result(
            detections, args.obj_thresh, args.nms_thresh)
        if len(detections) == 0:
            continue

        detections = transform_result(detections, img_batch, input_size)
        for detection in detections:
            draw_bbox(img_batch, detection, colors, classes)

        for i, img in enumerate(img_batch):
            save_path = osp.join(args.outdir, 'dete_' +
                                 osp.basename(imlist[batchi*batch_size + i]))
            cv2.imwrite(save_path, img)

    end_time = datetime.now()
    print('Detection finished in %s' % (end_time - start_time))

    return


def main():
    args = parse_args()

    if args.cuda and not torch.cuda.is_available():
        print("ERROR: cuda is not available, try running on CPU")
        sys.exit(1)

    print('Loading network...')
    model = Darknet(
        '/home/autonomous-car/Desktop/Autonomous_car_ros2/src/stereo_yolo3/stereo_yolo3/cfg/yolov3.cfg')
    model.load_weights(
        '/home/autonomous-car/Desktop/Autonomous_car_ros2/src/stereo_yolo3/stereo_yolo3/weights/yolov3.weights')
    if args.cuda:
        model.cuda()

    model.eval()
    print('Network loaded')

    # ros code
    rclpy.init()

    global stereo_image_pub, bridge

    stereo_image_pub = my_stereo_image_publisher(model,args)
    bridge = CvBridge()
    
    detect_video(model,args)

    print('shuting down')

    stereo_image_pub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
