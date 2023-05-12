import rosbag
from sensor_msgs.msg import Range

class BagFilter:
    def __init__(self):

        self.bag_name = '/home/pol/rosbags/relyOnM10/3_auto_flights/flight2_high_risk/a_2022-03-30-19-29-56_0.bag'
        self.inbag = rosbag.Bag(self.bag_name)
        self.outbag = rosbag.Bag("/home/pol/rosbags/relyOnM10/3_auto_flights/flight2_high_risk/a_2022-03-30-19-29-56_0_tfmini_mod.bag", 'w')
        # self.fov = 1.0

        for topic, msg, t in self.inbag.read_messages():
            if topic == '/mavros/distance_sensor/tfmini':
                msg.field_of_view = 1.0
                # self.ranges = list(msg.ranges)
                # self.ranges[3] += 1.0
                # for idx, val in enumerate(self.ranges):
                #     if self.ranges[idx] > 1.0:
                #         self.ranges[idx] = 999;                    
                
                # msg.ranges = self.ranges
                # print(msg.ranges[3])
                self.outbag.write(topic,msg,t)
            else:
                self.outbag.write(topic,msg,t)
        self.inbag.close()
        self.outbag.close()


if __name__ == '__main__':
    print('Bag Filter ON')
    bf = BagFilter()