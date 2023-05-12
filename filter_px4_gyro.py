#!/usr/bin/env python
import math
import time
import rospy
import numpy as np
from std_msgs.msg import Float32, Int32, String, ColorRGBA, Float32, Header, Float32MultiArray
from sensor_msgs.msg import Imu
from tf.transformations import euler_from_quaternion, quaternion_from_euler


class StatVisualizer:
    def __init__(self):
        rospy.init_node("imu_filter")

        rospy.Subscriber('/mavros/imu/data', Imu, self.mavros_imu_cb)
        self.pub_imu_filtered = rospy.Publisher("imu_filtered",
                                                Imu,
                                                queue_size=5)
        self.imu_filtered = ()

    def mavros_imu_cb(self, msg):
        orientation_q = msg.orientation
        curr_ang_vel_y = msg.angular_velocity.y
        rospy.loginfo('angular_velocity_y = ' + np.str(angular_velocity_y))

        # self.pub_imu_filtered.publish(self.imu_filtered)


if __name__ == '__main__':
    sv = StatVisualizer()
    rospy.loginfo('IMU Filter ON')
    r = rospy.Rate(0.5)  # 100hz

    while not rospy.is_shutdown():
        r.sleep()
