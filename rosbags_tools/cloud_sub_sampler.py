import numpy as np
cloud_file = open("cloud_0.txt")
prev_file = open("cloud_1.txt")

cloud_pt_list = []
for line in cloud_file.readlines():
    x,y,z,i = line.split('\t')
    x = float(x)
    y = float(y)
    z = float(z)
    i = float(i)
    cloud_pt_list.append([x,y,z,i])


prev_cloud_pt_list = []
for line in prev_file.readlines():
    x,y,z,i = line.split('\t')
    x = float(x)
    y = float(y)
    z = float(z)
    i = float(i)
    prev_cloud_pt_list.append([x,y,z,i])

print "Got 2 clouds lens : ", len(cloud_pt_list), " - ", len(prev_cloud_pt_list)

closest_indexes = []

new_points_a = []
new_points_b = []

out_arr = np.random.randint(low = 0, high = 300000, size = 3000)

for index in out_arr:
    if index < len(cloud_pt_list) and index < len(prev_cloud_pt_list):
        new_points_a.append(cloud_pt_list[index])
        new_points_b.append(prev_cloud_pt_list[index])
        
closest_indexes = []

def get_dist(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])

for i, cloud_pt in enumerate(new_points_a):
    smallest_dist = 999999.0
    closest_indexes.append(0)
    print "AT i = ", i
    for j, prev_pt in enumerate(new_points_b):
        dist = get_dist(new_points_a[i], new_points_b[j])
        if dist < smallest_dist:
            smallest_dist = dist
            closest_indexes[i] = j

print "Writing to output file"
with open("gold_cloud_0_to_1_reduced.txt", 'w+') as outfile:
    for i, idx in enumerate(closest_indexes):
        outfile.write(str(i) + "\t" + str(idx) + '\n')

with open("cloud_0_reduced.txt", 'w+') as outfile:
    for i, pt in enumerate(new_points_a):
        outfile.write(str(pt[0]) + "\t" + str(pt[1]) + "\t" + str(pt[2]) + "\t" + str(pt[3]) + '\n')

with open("cloud_1_reduced.txt", 'w+') as outfile:
    for i, pt in enumerate(new_points_b):
        outfile.write(str(pt[0]) + "\t" + str(pt[1]) + "\t" + str(pt[2]) + "\t" + str(pt[3]) + '\n')
