import numpy as np 
import time
from scipy.spatial.transform import Rotation as R
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def get_cloud(file_name):
	cloud_file = open(file_name)
	cloud = []
	for line in cloud_file.readlines():
		x,y,z,i = line.split('\t')
		x = float(x)
		y = float(y)
		z = float(z)
		i = float(i)
		cloud.append([x,y,z])
	cloud_file.close()
	return np.array(cloud)

def get_dist(a, b):
	return np.sum(np.square(np.abs(a-b)))

def get_correspondences(a, b):
	dists = np.ones(len(a)) * 99999.999999
	coresp = np.ones(len(a)) * -1.0
	for i, pt_a in enumerate(a):
		for j, pt_b in enumerate(b):
			dist = get_dist(pt_a,pt_b)
			if dist < dists[i]:
				dists[i] = dist
				coresp[i] = int(j)
	avg_error = np.average(dists)
	closest = []
	for idx in coresp:
		if idx == -1:
			print ("ERROR")
		else:
			closest.append(b[int(idx)])
	return np.array(closest), avg_error

#cloud_a = get_cloud("cloud_0.txt")
#cloud_b = get_cloud("cloud_1.txt")

cloud_a = np.array([[ 0,  0,  0], 
					[ 3,  3,  3],
					[-3, -5, -9],
					[-9,  1, -12],
					[-6, -1,  12],
					[ 8, -5, -9]])
				
cloud_b = cloud_a + 2

def get_centroid(a):
	return np.sum(a, 0) / float(len(a))

def shift_to_centroid(a):
	centroid = get_centroid(a)
	return a - centroid

def apply_rotation(cloud, rotation):
	new_cloud = []
	for pt in cloud:
		new_cloud.append(rotation.apply(pt))
	return np.array(new_cloud)

def run_icp_iteration(cloud_a, cloud_b):
	start = time.time()
	print ("Starting Time : ", start)
	centered_cloud_a = shift_to_centroid(cloud_a)
	centered_cloud_b = shift_to_centroid(cloud_b)

	closest, avg_error = get_correspondences(centered_cloud_a, centered_cloud_b)

	sxx = np.sum(cloud_a[:,0] * closest[:,0])
	sxy = np.sum(cloud_a[:,0] * closest[:,1])
	sxz = np.sum(cloud_a[:,0] * closest[:,2])
	syx = np.sum(cloud_a[:,1] * closest[:,0])
	syy = np.sum(cloud_a[:,1] * closest[:,1])
	syz = np.sum(cloud_a[:,1] * closest[:,2])
	szx = np.sum(cloud_a[:,2] * closest[:,0])
	szy = np.sum(cloud_a[:,2] * closest[:,1])
	szz = np.sum(cloud_a[:,2] * closest[:,2])

	N_MAT = np.array([	[sxx+syy+szz, syz-szy, szx-sxz, sxy-syz],
						[syz-szy, sxx-szz-syy, sxy-syx, sxz-szx],
						[szx-sxz, syz+sxy, syy-szz-sxx, syz+szy],
						[sxy-syx, szx+sxz, szy+syz, szz-syy-sxx]])

	vals, vects = np.linalg.eig(N_MAT)

	largest_eig_idx = np.argmax(vals)
	largest_eig_vec = vects[largest_eig_idx]

	print ("ICP ITERATION TOOK: ", time.time() - start)
	print ("Found Largest Eigen Vector : ", largest_eig_vec)
	print ("Average Error Before Alignment : ", avg_error)

	rotation = R.from_quat(largest_eig_vec)

	rot_cloud_a = apply_rotation(cloud_a, rotation)

	centered_rot_cloud_a = shift_to_centroid(rot_cloud_a)

	closest, new_avg_error = get_correspondences(centered_rot_cloud_a, centered_cloud_b)
	print ("\tAfter Applying Rotation, Average Error = ", new_avg_error)
	print ("\tDifference = ", avg_error-new_avg_error)
	return rot_cloud_a


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(cloud_a[:,0], cloud_a[:,1], cloud_a[:,2], marker='o')
plt.show()

for i in range(1,5):
	cloud_a = run_icp_iteration(cloud_a, cloud_b)
	fig = plt.figure()
	ax = fig.add_subplot(111, projection='3d')
	ax.scatter(cloud_a[:,0], cloud_a[:,1], cloud_a[:,2], marker='o')
	plt.show()

