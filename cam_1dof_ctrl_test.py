import rospy
import numpy as np
from mavros_msgs.msg import ActuatorControl


class Gimbal_test():

    def __init__(self, ):

        self.message_pub = rospy.Publisher("/mavros/actuator_control",
                                           ActuatorControl,
                                           queue_size=10)

        self.actuator_control_message = ActuatorControl()
        self.seq = 0

    def run(self):

        r = rospy.Rate(1)
        val = 800  #   r    p    y?
        # inputs = np.array((0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5))
        inputs = np.array((val, val, val, val, val, val, val, val))
        self.actuator_control_message.group_mix = 4
        self.actuator_control_message.controls = inputs

        while not rospy.is_shutdown():

            self.actuator_control_message.header.stamp = rospy.Time.now()
            self.actuator_control_message.header.seq = self.seq
            # doc: https://docs.px4.io/v1.12/en/concept/mixing.html
            rospy.loginfo_throttle(3, inputs)
            self.message_pub.publish(self.actuator_control_message)

            self.seq = self.seq + 1
            r.sleep()


if __name__ == '__main__':

    rospy.init_node('cam_1dof_ctrl_test', anonymous=True, log_level=rospy.INFO)
    gt = Gimbal_test()
    gt.run()