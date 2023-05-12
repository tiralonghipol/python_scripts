#!/usr/bin/env python
import numpy as np
import cv2
import argparse
import ruamel.yaml

def main():
    parser = argparse.ArgumentParser(description="Converts a cam info in kalibr yaml format to the expected ROS format for camera_info_manager.")
    parser.add_argument("--camchain", dest="camchain",
                        help="Camchain yaml file with camera info.",
                        required=True)
    parser.add_argument("--div2", dest="div2", help="Compute half resolution",
                        required=True)

    path = parser.parse_args().camchain
    
    with open(path, 'r') as stream:
        try:
            data = ruamel.yaml.safe_load(stream)
        except ruamel.yaml.YAMLError as exc:
            print(exc)

    intrinsics0 = data['cam0']['intrinsics']
    K0 = np.array([[intrinsics0[0], 0, intrinsics0[2]],
                   [0, intrinsics0[1], intrinsics0[3]],
                   [0, 0, 1]])
    d0 = np.array(data['cam0']['distortion_coeffs'])
    resolution = data['cam0']['resolution']
    distortion_model0 = data['cam0']['distortion_model']

    R0 = np.identity(3)
    P0 = np.hstack((K0, np.zeros((3, 1))))
    
    # If stereo, calculate the rectification parameters
    is_stereo = 'cam0' in data and 'cam1' in data
    if is_stereo:
        distortion_model1 = data['cam1']['distortion_model']
        intrinsics1 = data['cam1']['intrinsics']
        K1 = np.array([[intrinsics1[0], 0, intrinsics1[2]],
                             [0, intrinsics1[1], intrinsics1[3]],
                             [0, 0, 1]])
        d1 = np.array(data['cam1']['distortion_coeffs'])
        H_12 = np.array(data['cam1']['T_cn_cnm1'])
        R = H_12[:3, :3]
        t = H_12[:3, 3]

        if distortion_model0 == 'radtan':
          R0, R1, P0, P1,Q = cv2.fisheye.stereoRectify(K0,
                                                     d0,
                                                     K1,
                                                     d1,
                                                     tuple(resolution),
                                                     R,
                                                     t,
                                                     cv2.CALIB_ZERO_DISPARITY)
        else:
          R0, R1, P0, P1,Q = cv2.fisheye.stereoRectify(K0,
                                                       d0,
                                                       K1,
                                                       d1,
                                                       tuple(resolution),
                                                       R,
                                                       t,
                                                       cv2.CALIB_ZERO_DISPARITY)
          
    # Output name will use the input camchain name, without the extension.
    path_split = path.split('.')

    if is_stereo:
        outfile_l = open(path_split[0] + '_left_ros.yaml', 'w')
    else:
        outfile_l = open(path_split[0] + '_ros.yaml', 'w')
    calib0 = {'image_width': resolution[0],
              'image_height': resolution[1],
              'camera_name': "cam0",
              'distortion_model': distortion_model0,
              'distortion_coefficients': {'data': d0.tolist(), 'rows': 1, 'cols': len(d0.tolist())},
              'camera_matrix': {'data': K0.flatten().tolist(), 'rows': 3, 'cols': 3},
              'rectification_matrix': {'data': R0.flatten().tolist(), 'rows': 3, 'cols': 3},
              'projection_matrix': {'data': P0.flatten().tolist(), 'rows': 3, 'cols': 4}}

    ruamel.yaml.safe_dump(calib0, outfile_l)

    if is_stereo:
        outfile_r = open(path_split[0] + '_right_ros.yaml', 'w')
        calib1 = {'image_width': resolution[0],
                  'image_height': resolution[1],
                  'camera_name': "cam1",
                  'distortion_model': distortion_model1,
                  'distortion_coefficients': {'data': d1.tolist(), 'rows': 1, 'cols': len(d1.tolist())},
                  'camera_matrix': {'data': K1.flatten().tolist(), 'rows': 3, 'cols': 3},
                  'rectification_matrix': {'data': R1.flatten().tolist(), 'rows': 3, 'cols': 3},
                  'projection_matrix': {'data': P1.flatten().tolist(), 'rows': 3, 'cols': 4}}
        
        ruamel.yaml.safe_dump(calib1, outfile_r)
        
if __name__ == "__main__":
    main()