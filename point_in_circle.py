#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import random
    
def main():
    u = random.random();
    v = random.random();
    theta = u * 2.0 * np.pi;
    phi = np.arccos(2.0 * v - 1.0);
    r = np.cbrt(random.random());
    sinTheta = np.sin(theta);
    cosTheta = np.cos(theta);
    sinPhi = np.sin(phi);
    cosPhi = np.cos(phi);
    x = r * sinPhi * cosTheta;
    y = r * sinPhi * sinTheta;
    z = r * cosPhi;

    print('x: ', x ,' y: ',y, ' z: ', z)

if __name__ == "__main__":    
    main()


    