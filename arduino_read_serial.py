# import serial
# import numpy as np

# ser = serial.Serial('/dev/ttyACM0',9600)
# ser.close()
# ser.open()
# while True:

#     data = ser.readline()
#     print(data.decode())
#     with open("test.txt","w") as f:
#         f.write(data.decode())

#     # x.append(i)
#     # y.append(data.decode())

#     # plt.scatter(i, float(data.decode()))
#     # i += 1
#     # plt.show()
#     # plt.pause(0.0001)  # Note this correction

import serial
import time
import csv
import rospy
from sensor_msgs.msg import Imu

ser = serial.Serial('/dev/ttyACM0')
ser.flushInput()


def talker():
    pub_mpu1 = rospy.Publisher('mpu1', Imu, queue_size=10)
    pub_mpu2 = rospy.Publisher('mpu2', Imu, queue_size=10)


# while True:
#     try:
#         ser_bytes = ser.readline()
#         decoded_bytes = ser_bytes.decode()
#         print(decoded_bytes)
#         with open("test_data.csv","a") as f:
#             writer = csv.writer(f,delimiter=",")
#             writer.writerow([time.time(),decoded_bytes])
#     except:
#         print("Keyboard Interrupt")
#         break

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
