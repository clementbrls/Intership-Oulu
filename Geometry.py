import numpy as np
import matplotlib.pyplot as plt
from mic import Mic


class Circle:
    def __init__(self, center, r, normal):
        self.center = center
        self.r = r
        self.normal = normal

    def draw(self, res):
        normal = self.normal
        center = self.center
        radius = self.r

        # Create an orthonormal basis with the normal vector as the z-axis
        z_axis = normal / np.linalg.norm(normal)
        x_axis = np.array([1, 0, 0])
        if np.allclose(z_axis, x_axis):
            x_axis = np.array([0, 1, 0])
        y_axis = np.cross(z_axis, x_axis)
        x_axis = np.cross(y_axis, z_axis)

        # Generate points on a flat circle
        t = np.linspace(0, 2*np.pi, res)
        x = radius * np.cos(t)
        y = radius * np.sin(t)

        # Rotate the points to account for the orientation of the circle in 3D space
        points = np.column_stack((x, y, np.zeros_like(t)))
        points = np.dot(points, np.array([x_axis, y_axis, z_axis]))

        # Translate the points to the origin of the circle
        points += center

        return points


def find(mic0, mic1, delta, dist):
    x1 = mic0.x
    y1 = mic0.y
    r1 = dist

    x2 = mic1.x
    y2 = mic1.y
    r2 = dist+delta

    d = np.sqrt((x2-x1)**2+(y2-y1)**2)
    a = (r1**2-r2**2+d**2)/(2*d)
    x_mid = x1+a*(x2-x1)/d
    y_mid = y1+a*(y2-y1)/d

    h = np.sqrt(r1**2-a**2)

    xa = x_mid+h*(y2-y1)/d
    ya = y_mid+h*(x2-x1)/d

    xb = x_mid-h*(y2-y1)/d
    yb = y_mid-h*(x2-x1)/d

    return xa, ya, xb, yb


def find3D(mic0, mic1, delta, dist):
    x1 = mic0.x
    y1 = mic0.y
    z1 = mic0.z
    r1 = dist

    x2 = mic1.x
    y2 = mic1.y
    z2 = mic1.z
    r2 = dist+delta

    d = np.sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)

    a = (r1**2-r2**2+d**2)/(2*d)
    x_mid = x1+a*(x2-x1)/d
    y_mid = y1+a*(y2-y1)/d
    z_mid = z1+a*(z2-z1)/d

    h = np.sqrt(r1**2-a**2)

    vector_orthogonal = np.array([x2-x1, y2-y1, z2-z1])
    vector_orthogonal = vector_orthogonal/np.linalg.norm(vector_orthogonal)

    circle = Circle((x_mid, y_mid, z_mid), h, vector_orthogonal)
    return circle


def whereItCouldBe(mic0, mic1, delta):
    x = np.empty(0)
    y = np.empty(0)

    distmin = (mic0.dist(mic1)-delta)/2
    distmax = 1000
    res = 1000
    for i in np.logspace(np.log10(distmin+(1/res)), np.log10(distmax), res):
        u = find(mic0, mic1, delta, i)
        x = np.append(x, u[0])
        y = np.append(y, u[1])
        x = np.append(u[2], x)
        y = np.append(u[3], y)
    return x, y


def whereItCouldBe3D(mic0, mic1, delta, res=400, distmin=None, distmax=None):
    surface = np.empty((0, 3))  # Initialize with an empty 2D array
    if distmin is None:
        distmin = (mic0.dist(mic1) - delta) / 2

    if distmax is None:
        distmax = mic0.dist(mic1)*5
    for i in np.logspace(np.log10(distmin + (1 / res)), np.log10(distmax), res):
        circle = find3D(mic0, mic1, delta, i)
        res_circle = (i/distmax)*(res)
        u = circle.draw(int(res_circle))
        surface = np.append(surface, u, axis=0)
    return surface


def reduce(points1, points2, points3, lim=100):
    print("taille :", len(points1), len(points2), len(points3))
    stop = False
    while not stop:
        limits1 = np.array([np.min(points1, axis=0), np.max(points1, axis=0)])
        limits2 = np.array([np.min(points2, axis=0), np.max(points2, axis=0)])
        limits3 = np.array([np.min(points3, axis=0), np.max(points3, axis=0)])

        # agrandir la limite de 30%
        limits1[0] = limits1[0] - 0.1*(limits1[1]-limits1[0])
        limits1[1] = limits1[1] + 0.1*(limits1[1]-limits1[0])
        limits2[0] = limits2[0] - 0.1*(limits2[1]-limits2[0])
        limits2[1] = limits2[1] + 0.1*(limits2[1]-limits2[0])
        limits3[0] = limits3[0] - 0.1*(limits3[1]-limits3[0])
        limits3[1] = limits3[1] + 0.1*(limits3[1]-limits3[0])

        # create boolean masks for each set of points
        mask1 = np.logical_and(points1 >= limits2[0], points1 <= limits2[1]).all(axis=1) \
            & np.logical_and(points1 >= limits3[0], points1 <= limits3[1]).all(axis=1)
        mask2 = np.logical_and(points2 >= limits1[0], points2 <= limits1[1]).all(axis=1) \
            & np.logical_and(points2 >= limits3[0], points2 <= limits3[1]).all(axis=1)
        mask3 = np.logical_and(points3 >= limits1[0], points3 <= limits1[1]).all(axis=1) \
            & np.logical_and(points3 >= limits2[0], points3 <= limits2[1]).all(axis=1)

        old_points1 = points1.copy()
        old_points2 = points2.copy()
        old_points3 = points3.copy()

        stop1 = False
        stop2 = False
        stop3 = False
        # filter out the points that are outside the limits
        if len(points1[mask1]) > lim:
            points1 = points1[mask1]
        if len(points2[mask2]) > lim:
            points2 = points2[mask2]
        if len(points3[mask3]) > lim:
            points3 = points3[mask3]

        if np.array_equal(old_points1, points1) and np.array_equal(old_points2, points2) and np.array_equal(old_points3, points3):
            stop = True

        print("taille :", len(points1), len(points2), len(points3))
    # find the list with the smallest number of points
    stop2 = False
    min_len = min(len(points1), len(points2), len(points3))
    while (not stop2):
        old_points1 = points1.copy()
        old_points2 = points2.copy()
        old_points3 = points3.copy()
        if len(points1) == min_len:
            limits2 = np.array(
                [np.min(points2, axis=0), np.max(points2, axis=0)])
            limits3 = np.array(
                [np.min(points3, axis=0), np.max(points3, axis=0)])
            mask2 = np.logical_and(
                points2 >= limits3[0], points2 <= limits3[1]).all(axis=1)
            mask3 = np.logical_and(
                points3 >= limits2[0], points3 <= limits2[1]).all(axis=1)
            if len(points2[mask2]) > lim:
                points2 = points2[mask2]
            if len(points3[mask3]) > lim:
                points3 = points3[mask3]
        elif len(points2) == min_len:
            limits1 = np.array(
                [np.min(points1, axis=0), np.max(points1, axis=0)])
            limits3 = np.array(
                [np.min(points3, axis=0), np.max(points3, axis=0)])
            mask1 = np.logical_and(
                points1 >= limits3[0], points1 <= limits3[1]).all(axis=1)
            mask3 = np.logical_and(
                points3 >= limits1[0], points3 <= limits1[1]).all(axis=1)
            if len(points1[mask1]) > lim:
                points1 = points1[mask1]
            if len(points3[mask3]) > lim:
                points3 = points3[mask3]
        elif len(points3) == min_len:
            limits1 = np.array(
                [np.min(points1, axis=0), np.max(points1, axis=0)])
            limits2 = np.array(
                [np.min(points2, axis=0), np.max(points2, axis=0)])
            mask1 = np.logical_and(
                points1 >= limits2[0], points1 <= limits2[1]).all(axis=1)
            mask2 = np.logical_and(
                points2 >= limits1[0], points2 <= limits1[1]).all(axis=1)
            if len(points1[mask1]) > lim:
                points1 = points1[mask1]
            if len(points2[mask2]) > lim:
                points2 = points2[mask2]
        min_len_new = min(len(points1), len(points2), len(points3))
        if min_len_new != min_len or np.array_equal(old_points1, points1) and np.array_equal(old_points2, points2) and np.array_equal(old_points3, points3):
            stop2 = True
            print("stop!!")

    return points1, points2, points3


def find_intersect(points1, points2, points3):
    print("taille :", len(points1), len(points2), len(points3))
    if(len(points1)*len(points2)*len(points3) <= 500000):
        print("this !!!")
        # Calcul des distances entre les points
        distances = np.zeros((len(points1), len(points2), len(points3)))
        for i, point1 in enumerate(points1):
            for j, point2 in enumerate(points2):
                for k, point3 in enumerate(points3):
                    distances[i, j, k] = np.sqrt(np.sum((point1 - point2)**2)) + np.sqrt(np.sum((point2 - point3)**2)) + np.sqrt(np.sum((point3 - point1)**2))

        # Trouver les points les plus proches
        i, j, k = np.unravel_index(np.argmin(distances), distances.shape)
        closest_points = (points1[i], points2[j], points3[k])

        return np.mean(closest_points, axis=0)
    else:
        x, y, z = np.mean(np.concatenate(
            [points1, points2, points3], axis=0), axis=0)
        return (x, y, z)


def WhereItIs(mic0, mic1, mic2, mic3, delta1, delta2, delta3):
    points1 = whereItCouldBe3D(mic0, mic1, delta1,res=100)
    points2 = whereItCouldBe3D(mic0, mic2, delta2,res=100)
    points3 = whereItCouldBe3D(mic0, mic3, delta3,res=100)
    points1, points2, points3 = reduce(points1, points2, points3)

    closest_point1 = points1[0, :]
    closest_point2 = points2[0, :]
    closest_point3 = points3[0, :]

    distmin1 = np.linalg.norm(closest_point1-mic0.get_pos())
    distmin2 = np.linalg.norm(closest_point2-mic0.get_pos())
    distmin3 = np.linalg.norm(closest_point3-mic0.get_pos())

    latest_points1 = points1[-1, :]
    latest_points2 = points2[-1, :]
    latest_points3 = points3[-1, :]

    distmax1 = np.linalg.norm(latest_points1-mic0.get_pos())
    distmax2 = np.linalg.norm(latest_points2-mic0.get_pos())
    distmax3 = np.linalg.norm(latest_points3-mic0.get_pos())

    print("distmin1 : ", distmin1)
    print("dismax:", distmax1)

    points1 = whereItCouldBe3D(
        mic0, mic1, delta1, res=1000, distmin=distmin1, distmax=distmax1)
    points2 = whereItCouldBe3D(
        mic0, mic2, delta2, res=1000, distmin=distmin2, distmax=distmax2)
    points3 = whereItCouldBe3D(
        mic0, mic3, delta3, res=1000, distmin=distmin3, distmax=distmax3)

    points1, points2, points3 = reduce(points1, points2, points3, 20)
    print("taille afeter:", len(points1), len(points2), len(points3))

    print("Coordonée estimé : ", find_intersect(points1, points2, points3))
