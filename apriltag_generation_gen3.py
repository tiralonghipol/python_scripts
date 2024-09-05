#!/usr/bin/env python3
from moms_apriltag import ApriltagBoard
import imageio
from moms_apriltag import TagGenerator3
from matplotlib import pyplot as plt
import numpy as np
import cv2

merged_img = []

tg = TagGenerator3("tagCircle21h7")
for i in range(6):
    tag = tg.generate(i)
    padd_size = 2
    img_size = tag.shape[0]
    # print(tag.shape)

    # pad =np.zeros((img_size+2*padd_size, img_size+2*padd_size)) +255
    pad =np.zeros((img_size+2*padd_size, img_size+2*padd_size))
    pad[padd_size:img_size+padd_size, padd_size:img_size+padd_size] = tag
    merged_img.append(pad)

merge = np.concatenate(merged_img)

file_name = "images/merged_tags.png"
# img_uint8 = merge.astype(np.uint8)
# imageio.imwrite(file_name, img_uint8)

plt.imshow(merge, cmap="gray")
# plt.show()
plt.savefig(file_name)