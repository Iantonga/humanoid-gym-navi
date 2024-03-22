from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

import numpy as np

from sklearn import metrics
from scipy.spatial import ConvexHull
from sklearn.cluster import DBSCAN

from pedsim import PedestrianSimulator as pedsim

# centers = [[1, 1], [-1, -1], [1, -1]]
# X, labels_true = make_blobs(
#     n_samples=12, centers=centers, cluster_std=0.1, random_state=0
# )

# print(X[0][0])
# X = StandardScaler().fit_transform(X)



# plt.scatter(X[:, 0], X[:, 1])
# plt.show()

# db = DBSCAN(eps=0.2, min_samples=2).fit(X)
# labels = db.labels_

# # Number of clusters in labels, ignoring noise if present.
# n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
# n_noise_ = list(labels).count(-1)

# print("Estimated number of clusters: %d" % n_clusters_)
# print("Estimated number of noise points: %d" % n_noise_)

# unique_labels = set(labels)
# core_samples_mask = np.zeros_like(labels, dtype=bool)
# core_samples_mask[db.core_sample_indices_] = True

# colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
# for k, col in zip(unique_labels, colors):
#     if k == -1:
#         # Black used for noise.
#         col = [0, 0, 0, 1]

#     class_member_mask = labels == k

#     xy = X[class_member_mask & core_samples_mask]
#     plt.plot(
#         xy[:, 0],
#         xy[:, 1],
#         "o",
#         markerfacecolor=tuple(col),
#         markeredgecolor="k",
#         markersize=14,
#     )

#     xy = X[class_member_mask & ~core_samples_mask]
#     plt.plot(
#         xy[:, 0],
#         xy[:, 1],
#         "o",
#         markerfacecolor=tuple(col),
#         markeredgecolor="k",
#         markersize=6,
#     )

# plt.title(f"Estimated number of clusters: {n_clusters_}")
# plt.show()

class SocialGroup(object):
    def __init__(self, pos, vel):
        self.positions = pos #list of coordinates of agents in the group
        self.velocities = vel
        self.num_agents = len(pos)

    def create_personal_space(self,pos):
        # return the function of personal space given agent position
        #x - h 2 + y - k 2 = r 2
        #f = lambda x, y: 
        pass

    def register_group():
        pass

    def extract_membership(self,e1=0.2,e2=2):
        #pos: ndarray [[pox,posy]]
        db = DBSCAN(eps=e1, min_samples=e2).fit(self.pos)
        labels = db.labels_

        # Number of clusters in labels, ignoring noise if present.
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        n_noise_ = list(labels).count(-1)

        #print("Estimated number of clusters: %d" % n_clusters_)
        #print("Estimated number of noise points: %d" % n_noise_)
        return labels
    
    def boundary_dist(self, velocity, rel_ang, const=0.354163):
        # Parameters from Rachel Kirby's thesis
        front_coeff = 1.0
        side_coeff = 2.0 / 3.0
        rear_coeff = 0.5
        safety_dist = 0.5
        velocity_x = velocity[0]
        velocity_y = velocity[1]

        velocity_magnitude = np.sqrt(velocity_x ** 2 + velocity_y ** 2)
        variance_front = max(0.5, front_coeff * velocity_magnitude)
        variance_side = side_coeff * variance_front
        variance_rear = rear_coeff * variance_front

        rel_ang = rel_ang % (2 * np.pi)
        flag = int(np.floor(rel_ang / (np.pi / 2)))
        if flag == 0:
            prev_variance = variance_front
            next_variance = variance_side
        elif flag == 1:
            prev_variance = variance_rear
            next_variance = variance_side
        elif flag == 2:
            prev_variance = variance_rear
            next_variance = variance_side
        else:
            prev_variance = variance_front
            next_variance = variance_side

        dist = np.sqrt(const / ((np.cos(rel_ang) ** 2 / (2 * prev_variance)) + (np.sin(rel_ang) ** 2 / (2 * next_variance))))
        dist = max(safety_dist, dist)

        return dist
    
    def draw_social_shapes(self, const=0.35):
        # This function draws social group shapes
        # given the positions and velocities of the pedestrians.

        total_increments = 20 # controls the resolution of the blobs
        quater_increments = total_increments / 4
        angle_increment = 2 * np.pi / total_increments

        # Draw a personal space for each pedestrian within the group
        contour_points = []
        position = self.positions
        velocity = self.velocities
        for i in range(len(position)):
            center_x = position[i][0]
            center_y = position[i][1]
            velocity_x = velocity[i][0]
            velocity_y = velocity[i][1]
            velocity_angle = np.arctan2(velocity_y, velocity_x)

            # Draw four quater-ovals with the axis determined by front, side and rear "variances"
            # The overall shape contour does not have discontinuities.
            for j in range(total_increments):

                rel_ang = angle_increment * j
                value = self.boundary_dist(velocity[i], rel_ang, const)
                addition_angle = velocity_angle + rel_ang
                x = center_x + np.cos(addition_angle) * value
                y = center_y + np.sin(addition_angle) * value
                contour_points.append((x, y))

        # Get the convex hull of all the personal spaces
        convex_hull_vertices = []
        hull = ConvexHull(np.array(contour_points))
        for i in hull.vertices:
            hull_vertice = (contour_points[i][0], contour_points[i][1])
            convex_hull_vertices.append(hull_vertice)

        return convex_hull_vertices
    

if __name__ =="__main__":
    sim = pedsim()
    sim.create_scenario(1)
    positions, velocities = sim.step()
    group1pos = positions[4:]
    groups = SocialGroup(group1pos,velocities)
    convex_vert = groups.draw_social_shapes()
    xa = []
    ya = []
    x = []
    y = []
    for a in positions:
        xa.append(a[0])
        ya.append(a[1])
    for v in convex_vert:
        x.append(v[0])
        y.append(v[1])
    #print(sim.getNumAgents(), len(convex_vert))
    plt.scatter(x,y)
    plt.scatter(xa,ya)
    plt.show()


