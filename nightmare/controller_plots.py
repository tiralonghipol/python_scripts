import rosbag
import matplotlib.pyplot as plt
from nav_msgs.msg import Path
from nav_msgs.msg import Odometry

def read_bag_and_plot(bag_file):
    bag = rosbag.Bag(bag_file, 'r')

    path_data = {'timestamps': [], 'poses_x': [], 'poses_y': []}
    odom_data = {'timestamps': [], 'positions_x': [], 'positions_y': []}

    topic_path = '/path'
    topic_odom = '/qualisys/nightmare/odom'
    for topic, msg, t in bag.read_messages(topics=[topic_path, 
                                                   topic_odom]):
        if topic == topic_path and isinstance(msg, Path):
            for pose in msg.poses:
                path_data['timestamps'].append(pose.header.stamp.to_sec())
                path_data['poses_x'].append(pose.pose.position.x)
                path_data['poses_y'].append(pose.pose.position.y)

        elif topic == topic_odom and isinstance(msg, Odometry):
            odom_data['timestamps'].append(msg.header.stamp.to_sec())
            odom_data['positions_x'].append(msg.pose.pose.position.x)
            odom_data['positions_y'].append(msg.pose.pose.position.y)

    bag.close()

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(path_data['poses_x'], path_data['poses_y'], label='Path')
    plt.scatter(odom_data['positions_x'], odom_data['positions_y'], color='red', marker='o', label='Odometry')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.title('Path vs Odometry')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    bag_file_path = '/home/pol/rosbags/nightmare/a_2024-01-23-17-07-16_0.bag'
    read_bag_and_plot(bag_file_path)
