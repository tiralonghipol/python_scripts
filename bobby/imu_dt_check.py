
#!/usr/bin/env python3

import rosbag
import matplotlib.pyplot as plt

# Function to compute dt between consecutive timestamps
def compute_time_differences(timestamps):
    return [t2 - t1 for t1, t2 in zip(timestamps[:-1], timestamps[1:])]

# Function to compute the frequency of the signal
def compute_frequency(time_differences):
    avg_dt = sum(time_differences) / len(time_differences)
    return 1.0 / avg_dt if avg_dt > 0 else 0

# Function to extract timestamps from a bag file
def extract_timestamps(bag_file, topic_name):
    timestamps = []
    with rosbag.Bag(bag_file, 'r') as bag:
        for topic, msg, t in bag.read_messages(topics=[topic_name]):
            timestamps.append(msg.header.stamp.to_sec())
    return timestamps

# Load the bag files
bag_file1 = '/home/pol/rosbags/imu_comparison/2024-09-02-12-41-53_morphy_5queuesize.bag'
bag_file2 = '/home/pol/rosbags/imu_comparison/2024-09-02-12-33-43_fifo100.bag'
topic_name = '/imu_apps'  # Replace with your IMU topic

# Initialize a list to store timestamps
timestamps1 = []
timestamps2 = []

# Extract timestamps
timestamps_1 = extract_timestamps(bag_file1, topic_name)
timestamps_2 = extract_timestamps(bag_file2, topic_name)

# Compute the time differences
time_differences_1 = compute_time_differences(timestamps_1)
time_differences_2 = compute_time_differences(timestamps_2)

# Compute the frequencies
frequency_1 = compute_frequency(time_differences_1)
frequency_2 = compute_frequency(time_differences_2)

# Print the frequencies
print(f"Frequency of the IMU signal in Bag 1: {frequency_1:.2f} Hz")
print(f"Frequency of the IMU signal in Bag 2: {frequency_2:.2f} Hz")

# Plot the time differences
plt.figure(figsize=(10, 6))
plt.plot(time_differences_1, label='dT with q=5')
plt.plot(time_differences_2, label='dT with q=1', alpha = 0.6, linestyle='--')
plt.xlabel('Sample Index')
plt.ylabel('Time Difference (seconds)')
plt.title('Time Differences between Consecutive IMU Messages')
plt.legend()
plt.grid(True)
plt.show()
