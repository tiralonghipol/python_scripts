#!/usr/local/bin/python3
import rosbag
import numpy as np
import pcl
import rospy
from sensor_msgs.msg import PointCloud2, PointField
from std_msgs.msg import Header
import sensor_msgs.point_cloud2 as pc2
inbag_topics = ["/velodyne_cloud_registered"]

bag_name = "03_comm_manual_test_comm_topics.bag"
#bag_name = "08_comm_manual_test_comm_topics.bag"
inbag = rosbag.Bag("/home/frank/temp_ws/" + bag_name, 'r')

# reading in data
print("Reading Bag...")
big_points_list = []
counter = 0
last_time = None
header = None
start_time = None
for topic, msg, t in inbag.read_messages(topics=inbag_topics):
	if start_time is None or t < start_time:
		start_time = t
	if (t - start_time) > rospy.Duration(550.0):
		print("Stopping")
		break
	if counter % 10 == 0:
		header = msg.header
		fields = msg.fields
		last_time = t
		for data in pc2.read_points(msg, skip_nans=True):
			#swap some axis for world frame
			x = data[0]
			y = data[1]
			z = data[2]
			r = data[3]
			if z > -4.0:
				big_points_list.append([z, x, y, data[3]])
		
		pcl_data = pcl.PointCloud_PointXYZI()
		pcl_data.from_list(big_points_list)
		sor = pcl_data.make_voxel_grid_filter()
		leaf_size = 0.5
		sor.set_leaf_size(leaf_size,leaf_size,leaf_size)
		cloud_filtered = sor.filter()
		big_points_list = []
		for pt in cloud_filtered:
			big_points_list.append(pt)

		print(t-start_time)
		print("on Cloud #", counter, "Cloud size = ", len(big_points_list))
	counter += 1


inbag.close()
print("Writing Cloud")
outfile = open(bag_name+"_points.txt", 'w')
for pt in big_points_list:
	outfile.write(str(pt[0]) + "," + str(pt[1]) + "," + str(pt[2]) + '\n')
outfile.close()

new_msg = pc2.create_cloud(header, fields, big_points_list)

new_bag = rosbag.Bag(bag_name + "_cloud.bag", 'w')
new_msg.header.stamp = start_time
new_msg.header.frame_id = "world"
new_bag.write("big_cloud", new_msg, start_time)
new_bag.close()


