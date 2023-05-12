import rosbag
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32

class BagFilter:
    def __init__(self):

        self.bag_name = '/media/pol/Extreme SSD/Datasets/Gagarin/elios_gagarin1_mission_alpha.bag'
        self.inbag = rosbag.Bag(self.bag_name)
        self.outbag = rosbag.Bag("elios_gagarin1_mission_alpha_filtered.bag", 'w')
        self.ranges = []

        for topic, msg, t in self.inbag.read_messages():
            if topic == '/realsense_republisher/camera_info':
                self.outbag.write(topic,msg,t)
            if topic == '/realsense_republisher/image_flipped_and_rectified':
                self.outbag.write(topic,msg,t)
        
        self.inbag.close()
        self.outbag.close()


if __name__ == '__main__':
    print('Bag Filter ON')
    bf = BagFilter()