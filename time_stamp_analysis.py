#!/usr/bin/env python3
import math
import numpy as np
import matplotlib.pyplot as plt
import csv
import itertools


def Diff(li1, li2): 
    return (list(set(li1) - set(li2))) 
  
def Average(lst): 
    return sum(lst) / len(lst) 
  
imu = []
vision = []
diff = []
def main():
    

    with open("/home/pol/time_imu.txt") as fp:

        lines = fp.readlines()
        desired_lines = lines[2::4]
        # print(desired_lines)
    fp.close()
    for data in desired_lines:
        imu.append(float(data))
    print(imu)

    with open("/home/pol/time_vision.txt") as fp:
        lines = fp.readlines()
        desired_lines = lines[2::4]
        # print(desired_lines)
    fp.close()
    for data in desired_lines:
        vision.append(float(data))
    print(vision)

    diff = Diff(imu, vision)
    average = Average(diff) 
  
    # Printing average of the list 
    print("Average of the list =", round(average, 3)) 
    print("Max = ",max(diff))

if __name__ == "__main__":    
    main()