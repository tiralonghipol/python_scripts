#!/usr/bin/env python3
from moms_apriltag import ApriltagBoard
import imageio
from matplotlib import pyplot as plt

board = ApriltagBoard.create(1,6,"tagCircle21h7", 0.02)
tgt = board.board
plt.imshow(tgt, cmap="gray")
plt.show()

filename = "apriltag_target.png"
imageio.imwrite(filename, tgt)
