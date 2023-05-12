import rosbag
import matplotlib.pyplot as plt
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2, PointField

def ros_to_pcl(ros_cloud):
    points_list = []
    max_num_points = 25000
    counter = 0
    for data in pc2.read_points(ros_cloud, skip_nans=True):
        if counter % 100 == 0:
            point = [data[0], data[1], data[2], data[3]]
            points_list.append(point)
            if len(points_list) >= max_num_points:
                return points_list
        counter  += 1
    return points_list
counter = 0
inbag = rosbag.Bag("/home/frank/temp_ws/full_data.bag", 'r')
for topic, msg, t in inbag.read_messages():
    if topic == "/velodyne_points":
        with open("cloud_"+str(counter)+".txt", 'w+') as f:
            pcl_cloud = ros_to_pcl(msg)
            print ("Got Cloud with ", len(pcl_cloud), " points")
            for pt in pcl_cloud:
                f.write(str(pt[0]) + "\t" + str(pt[1]) + "\t" + str(pt[2]) + "\t" + str(pt[3]) + '\n')
            counter += 1
    if counter > 4:
        exit()