import pickle
__author__ = 'kmalarski'


class Point:

    def __init__(self, dim_list):
        self.dims = dim_list
        self.visited = False
        self.in_cluster = False

    def __len__(self):
        return len(self.dims)

    def __getitem__(self, item):
        return self.dims[item]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def mark_visited(self):
        self.visited = True

    def mark_noise(self):
        self.visited = False


class Cluster:
    def __init__(self):
        self.members = []

    def __iter__(self):
        for member in self.members:
            yield member

    def __len__(self):
        return len(self.members)

    def is_in_cluster(self, point):
        for pnt in self.members:
            if pnt == point:
                return True
        return False

    def expand_cluster(self, point, neighbour_points, eps, min_pts):
        point.in_cluster = True
        self.members.append(point)
        for pt in neighbour_points:
            if pt.visited is False:
                pt.mark_visited()
                neighbour_pts = region_query(pt, eps)
                if len(neighbour_pts) >= min_pts:
                    neighbour_points += neighbour_pts
            if pt.in_cluster is False:
                pt.in_cluster = True
                self.members.append(pt)


def prepare_points(data):
    return [Point(dim_row) for dim_row in data]


def dbscan(d, eps, min_pts):
    C = []
    cnt = 0
    for point in d:
        print(cnt)
        cnt += 1
        if point.visited is True:
            continue
        point.visited = True
        neighbour_pts = region_query(point, eps)
        if len(neighbour_pts) < min_pts:
            point.mark_noise()
        else:
            # new cluster
            C.append(Cluster())
            C[-1].expand_cluster(point, neighbour_pts, eps, min_pts)
    return C


def compute_jaccard_distance(point, ref_point):
    suma = 0
    product = 0
    for i in range(len(point)):
        if point[i] == 1 and ref_point[i] == 1:
            product += 1
            suma += 1
        elif point[i] == 1 and ref_point[i] == 0 or point[i] == 0 and ref_point[i] == 1:
            suma += 1
    return 1 - product / suma if suma != 0 else 0


def region_query(P, eps):

    pts_to_return = []
    for point in matrix:
        tmp_jdist = compute_jaccard_distance(point, P)
        if tmp_jdist <= eps:
            pts_to_return.append(point)
    return pts_to_return
import datetime

start_time = datetime.datetime.now()

mat = pickle.load(open("/home/kmalarski/Desktop/DTU/bigdata/tfbd/w4/test_files/data_10000points_10000dims.dat", "rb"),
                  encoding='latin1')

matr = mat.toarray()
r1 = matr[0]
r2 = matr[2]


matrix = prepare_points(matr)

clusters = dbscan(d=matrix, eps=0.15, min_pts=2)

print("There are {} clusters.".format(len(clusters)))

unclustered_pts = 0
for point in matrix:
    if point.visited == False:
        # print("Helo")
        unclustered_pts = 1

print(len(clusters) + unclustered_pts)

print("cluster length coming soon")
biggest_len = 0
for cluster in clusters:

    print(len(cluster))
    if len(cluster) > biggest_len:
        biggest_len = len(cluster)

print("The biggest cluster contains {} points".format(biggest_len))
stop_time = datetime.datetime.now()
print("The operation lasted {}".format(stop_time - start_time))
