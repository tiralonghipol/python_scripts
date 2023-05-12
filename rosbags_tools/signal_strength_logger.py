import rosbag

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
				"/aft_mapped_to_init_CORRECTED",
				]

bag_name = "03_comm_manual_test_comm_topics.bag"

inbag = rosbag.Bag("/home/frank/temp_ws/" + bag_name, 'r')

last_pos = None

wifi_readings = []
xbee_readings = []
# reading in data
print("Reading Bag...")
for topic, msg, t in inbag.read_messages(topics=inbag_topics):
	if "level" in topic and last_pos is not None:
		wifi_readings.append((last_pos.x, last_pos.y, last_pos.z, msg.data))
	elif "local" in topic and last_pos is not None:
		xbee_readings.append((last_pos.x, last_pos.y, last_pos.z, msg.data))
	elif "msf_core/pose" in topic:
		last_pos = msg.pose.pose.position
inbag.close()
#writing data
print("Writing to File...")
outfile = open(bag_name+"_wifi_data.txt", 'w')
for reading in wifi_readings:
	outfile.write(str(reading[0]) + "," + str(reading[1]) + "," + str(reading[2]) + "," + str(reading[3]) + '\n')
outfile.close()


outfile = open(bag_name+"_xbee_data.txt", 'w')
for reading in xbee_readings:
	outfile.write(str(reading[0]) + "," + str(reading[1]) + "," + str(reading[2]) + "," + str(reading[3]) + '\n')
outfile.close()