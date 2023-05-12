#!/usr/bin/env python3
import rospy
from geometry_msgs.msg import PoseStamped
from std_srvs.srv import Empty

def poseStampedPublisher():
    # pub_poseStamped = rospy.Publisher('/command/pose', PoseStamped, latch=True, queue_size=1)   
    pub_poseStamped = rospy.Publisher('/mavros/local_position/pose', PoseStamped, latch=True, queue_size=1)   
    

    p = PoseStamped()
    p.header.frame_id = "world"

    p.pose.position.x = 0.0   
    p.pose.position.y = 0.0
    p.pose.position.z = 0.0
    p.pose.orientation.x = 0.0
    p.pose.orientation.y = 0.0
    p.pose.orientation.z = 0.0
    p.pose.orientation.w = 1.0


    # service = rospy.ServiceProxy('/back_to_position_hold', Empty)
    # response = service()
    # print("service called")
    # rospy.sleep(0.5)
    p.header.stamp = rospy.Time.now()
    pub_poseStamped.publish(p)
    print("pose published")


if __name__ == '__main__':
    
    rospy.init_node("poseStampedPublisher")
    rate = rospy.Rate(50)

    try:
        while(not rospy.is_shutdown()):
            poseStampedPublisher()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
