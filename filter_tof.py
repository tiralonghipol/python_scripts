import rosbag
from sensor_msgs.msg import LaserScan
from std_msgs.msg import Float32

class BagFilter:
    def __init__(self):

        self.bag_name = '/home/pol/Documents/Dataset/ICRA_2021/ca/rmf_irca_ca.bag'
        self.inbag = rosbag.Bag(self.bag_name)
        self.outbag = rosbag.Bag("rmf_icra_ca_tof_filtered.bag", 'w')
        self.ranges = []

        for topic, msg, t in self.inbag.read_messages():
            if topic == '/vl53l1x/scan_smooth':
                # msg.ranges = msg.ranges[3] + 1.0
                self.ranges = list(msg.ranges)
                self.ranges[3] += 1.0
                for idx, val in enumerate(self.ranges):
                    if self.ranges[idx] > 1.0:
                        self.ranges[idx] = 999;                    
                
                msg.ranges = self.ranges
                # print(msg.ranges[3])
                self.outbag.write(topic,msg,t)
            else:
                self.outbag.write(topic,msg,t)
        self.inbag.close()
        self.outbag.close()


if __name__ == '__main__':
    print('Bag Filter ON')
    bf = BagFilter()