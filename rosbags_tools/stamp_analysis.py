import rosbag
import matplotlib.pyplot as plt

inbag = rosbag.Bag(
    # "/home/pol/Documents/Dataset/RMF/rosbags/_2020-10-01-01-59-02.bag", 'r')
    "/home/pol/Documents/Dataset/RMF/rosbags/_2020-10-05-10-35-34.bag", 'r')
print("starting")
left_image_stamps = []
right_image_stamps = []
imu_times = []
starting_time = None
for topic, msg, t in inbag.read_messages():
    if topic == "/camera/fisheye1/image_raw_10hz":
        if starting_time is None:
            starting_time = msg.header.stamp.to_sec()
        left_image_stamps.append(msg.header.stamp.to_sec() - starting_time)
    if topic == "/camera/odom_50hz":
        if starting_time is None:
            starting_time = msg.header.stamp.to_sec()
        right_image_stamps.append(msg.header.stamp.to_sec() - starting_time)
    # if topic == "/camera/fisheye1/image_raw_10hz/rectified":
    #     if starting_time is None:
    #         starting_time = msg.header.stamp.to_sec()
    #     right_image_stamps.append(msg.header.stamp.to_sec() - starting_time)

inbag.close()
mismatches_found = 0
for x in left_image_stamps:
    if x not in right_image_stamps:
        print("Left Time ", x, " not in right stamps")
        mismatches_found += 1

for y in left_image_stamps:
    if y not in right_image_stamps:
        print("Right Time ", y, " not in left stamps")
        mismatches_found += 1

if mismatches_found > 0:
    print("Found ", mismatches_found, " mismatched stamps")
else:
    print("No mismatched stampsfound, images are sync'd")

plt.plot(left_image_stamps, 'r*', alpha=0.4)
plt.plot(right_image_stamps, 'b.', alpha=0.4)
plt.show()
plt.waitforbuttonpress
