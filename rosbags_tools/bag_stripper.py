
from std_msgs.msg import Time

import rosbag

import os

outbag_name = "08_comm_manual_test_comm_topics.bag"

bag_dir = "/media/frank/HARD DRIVE/ROS_BAGS/Comstock_Aeroconf_10.16.19/08_comm_manual_test/"

inbag_names = os.listdir(bag_dir)

inbag_topics = ["/xbee/remote_RSSI",
				"/xbee/local_RSSI",
				"/velodyne_cloud_registered",
				"/signal_strength/noise",
				"/signal_strength/link",
				"/signal_strength/level",
				"/os1_node/points_raw",
				"/msf_core/pose",
				"/tf",
				"/msf_core/odometry",
				"/aft_mapped_to_init_CORRECTED"]

outbag = rosbag.Bag(outbag_name, 'w')
for i,inbag_name in enumerate(inbag_names):
	inbag = rosbag.Bag(bag_dir+inbag_name, 'r')
	print ("Starting Bag Named : ", inbag_name, ", #", i+1, " of ", len(inbag_names))
	for topic, msg, t in inbag.read_messages(topics=inbag_topics):
			outbag.write(topic, msg, t)
inbag.close()
outbag.close()