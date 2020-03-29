#!/usr/bin/env python3
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def ttrl():
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        try:
          image_pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
        except CvBridgeError as e:
            print(e)

        # Display the resulting frame
        cv2.imshow('frame',gray)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == '__main__':
    image_pub = rospy.Publisher("image_topic_2",Image,queue_size=1)
    bridge = CvBridge()
    rospy.init_node('image_converter', anonymous=False)
    rate = rospy.Rate(10) # 10hz
    cap = cv2.VideoCapture(0)
    ttrl()
    cap.release()
    cv2.destroyAllWindows()
