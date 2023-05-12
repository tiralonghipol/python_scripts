#!/usr/bin/env python
import os.path
import sys
import rospy
import rosbag

num_files = len(sys.argv)

# Check number of arguments provided
if len(sys.argv) < num_files:
    print "Must provide at least 3 arguments, 2 input files, 1 output file"
    sys.exit(0)

# Add all input file names to an array
inbags = []
for i in range(1, num_files-1):
    file_name = str(sys.argv[i])
    print "GOT FILE : ", file_name
    if os.path.isfile(file_name):
        inbags.append(file_name)
    else:
        print "Cannot find input file : ", file_name
        sys.exit(0)

# Get output filename
file_name = str(sys.argv[num_files-1])
if not os.path.isfile(file_name):
    outbag = file_name
else:
    print "Outbag already exists : ", file_name
    sys.exit(0)


topic_names = ["/camera/image_raw", "/vn100/imu"]
# Loop through input files and loop through every topic,msg in them and write to output file
with rosbag.Bag(outbag, 'w') as outbag:
    for inbag in inbags:
        print("Processing bag: ", inbag)
        for topic, msg, t in rosbag.Bag(inbag).read_messages(topics=topic_names):
                outbag.write(topic, msg, t)
