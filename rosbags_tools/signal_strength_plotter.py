import numpy as np
from scipy.interpolate import griddata
import matplotlib.pyplot as plt
import numpy.ma as ma
import rosbag
import pcl
import rospy
from sensor_msgs.msg import PointCloud2
from std_msgs.msg import Header
import sensor_msgs.point_cloud2 as pc2

def get_sig_str_data(file_name):
	signal_strength_data_file = open(file_name, 'r')
	points = []
	rs = []
	for line in signal_strength_data_file.readlines():
		x,y,z,r = line.split(',')
		if(float(y) > -2.0) or float(x) > 95:
			continue
		if float(r) < -9000:
			r = -100.0
		points.append((float(x), float(y), float(z), float(r)))
		rs.append(float(r))
	signal_strength_data_file.close()
	return points, rs

def get_points(file_name):
	points_data_file = open(file_name, 'r')
	points = []
	for line in points_data_file.readlines():
		x,y,z = line.split(',')
		points.append((float(x), float(y), float(z)))
	points_data_file.close()


	return points

def get_dist(a,b):
	return np.sqrt(np.square(a[0]-b[0]) + np.square(a[1]-b[1]) + np.square(a[2]-b[2]))

str_points, rs = get_sig_str_data("/home/frank/temp_ws/03_comm_manual_test_comm_topics.bag_xbee_data.txt")

cloud_points = get_points("/home/frank/temp_ws/03_comm_manual_test_comm_topics.bag_points.txt")

for i, point in enumerate(cloud_points):
	sm_dist = np.inf
	nearest = None
	for str_pt  in str_points:
		dist = get_dist(point, str_pt)
		if dist < sm_dist:
			sm_dist = dist
			nearest = str_pt
	if not np.isnan(nearest[3] ):
		cloud_points[i] = (point[0], point[1], point[2], nearest[3]*-1.0 / 100)
	else:
		cloud_points[i] = (point[0], point[1], point[2], 100.0)
	print (i, " of ", len(cloud_points))

pcl_data = pcl.PointCloud_PointXYZI()
pcl_data.from_list(cloud_points)

bag_name = "03_comm_manual_test_comm_topics.bag"
inbag = rosbag.Bag("/home/frank/temp_ws/" + bag_name, 'r')
header = None
start_time = None
inbag_topics = ["/velodyne_cloud_registered"]

for topic, msg, t in inbag.read_messages(topics=inbag_topics):
	header = msg.header
	fields = msg.fields
	start_time = t
	break
inbag.close()
header.frame_id = "world"
new_msg = pc2.create_cloud(header, fields, cloud_points)
new_bag = rosbag.Bag(bag_name + "_cloud_colored_xbee.bag", 'w')
new_bag.write("big_cloud_colored", new_msg, start_time)
new_bag.close()
