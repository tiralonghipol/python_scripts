import rospy
import rosbag 
import os
import numpy as np
import matplotlib.pyplot as plt



def get_bag_names(path, prefix=""):
	bag_names = []
	files = os.listdir(path)
	for file_name in files:
		if prefix=="" or file_name.startswith(prefix):
			full_path = os.path.join(path, file_name)
			bag_names.append(full_path)
	return bag_names




bag_names = get_bag_names("/home/frank/ROSBAGS/IntegrationWeek/Alpha/Level_1_0/", "ZURICH_BUNKER_DAY_3")
topic_names = [	'/vn100/imu', 
				'/camera/image_raw']

timestamps = {}

for bag_name in bag_names:
	bag = rosbag.Bag(bag_name)
	print("Opening Bag : " + str(bag_name))
	for topic, msg, t in bag.read_messages(topics=topic_names):
		if topic not in timestamps.keys():
			timestamps[topic] = []
		timestamps[topic].append(msg.header.stamp.to_sec())
	bag.close()

for topic_name in timestamps.keys():
	timestamps[topic_name].sort()

num_zeros = 0
num_readings = 0

for i, topic in enumerate(timestamps.keys()):
	diffs = []
	last = None
	for timestamp in timestamps[topic]:
		if last is not None:
			diff = timestamp - last
			diffs.append(diff)
		last = timestamp
	plt.subplot(len(timestamps.keys()), 1, i+1)
	plt.title(topic)
	plt.xlabel('Readings')
	plt.xlabel('Time Difference between Readings')
	plt.plot(diffs)
	plt.ylim((0.0, 0.15))
plt.show()
