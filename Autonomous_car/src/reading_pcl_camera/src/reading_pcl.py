
#!/usr/bin/env python3
import numpy as np
import rospy
from std_msgs.msg import String
from reading_pcl_camera.msg import RadarScan 
import cv2

def callback(data):
    rospy.loginfo(data.point_id)
    if data.point_id != 0:
        cloud_data[data.x,data.y] = data.z
    else:
        rospy.loginfo(cloud_data)
        cloud_data.fill(0)

def listener():
    rospy.init_node('pcl_reader')
    rospy.Subscriber('/ti_mmwave/radar_scan', RadarScan , callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    cloud_data = np.zeros((1280,720))
    listener()