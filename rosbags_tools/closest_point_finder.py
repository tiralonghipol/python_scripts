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

def get_dist(a,b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])

for i, cloud_pt in enumerate(cloud_pt_list):
    smallest_dist = 999999.0
    closest_indexes.append(0)
    print "AT i = ", i
    for j, prev_pt in enumerate(prev_cloud_pt_list):
        dist = get_dist(cloud_pt_list[i], prev_cloud_pt_list[j])
        if dist < smallest_dist:
            smallest_dist = dist
            closest_indexes[i] = j

print "Writing to output file"
with open("cloud_0_to_1.txt", 'w+') as outfile:
    for i, idx in enumerate(closest_indexes):
        outfile.write(str(i) + "\t" + str(idx) + '\n')

