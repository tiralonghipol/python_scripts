import rosbag
import pprint
pp = pprint.PrettyPrinter(indent=1)

bag = rosbag.Bag('/home/pol/rosbags/collisions_arena52/test.bag')
info = bag.get_type_and_topic_info().topics

for topic_name in bag.get_type_and_topic_info().topics:
    print(topic_name + ": " + str(info[topic_name][3]))

bag.close()