#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
from reading_pcl_camera.msg import RadarScan 
import cv2

def callback(data):
    rospy.loginfo(data)
    
def listener():

    rospy.init_node('pcl_reader')

    rospy.Subscriber('/ti_mmwave/radar_scan', RadarScan , callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()