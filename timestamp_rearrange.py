#To replace message timestamps in a bag with header timestamps

import rosbag

with rosbag.Bag('/home/pol/rosbags/vim4_tests/2022-07-28-14-51-10_new_times.bag', 'w') as outbag:
    for topic, msg, t in rosbag.Bag('/home/pol/rosbags/vim4_tests/2022-07-28-14-51-10.bag').read_messages():
        # This also replaces tf timestamps under the assumption 
        # that all transforms in the message share the same timestamp
        if topic == "/tf" and msg.transforms:
            outbag.write(topic, msg, msg.transforms[0].header.stamp)
        else:
            outbag.write(topic, msg, msg.header.stamp if msg._has_header else t)
        