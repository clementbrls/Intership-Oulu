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
    if distmin is None:
        distmin = (mic0.dist(mic1) - delta) / 2

    if distmax is None:
        distmax = mic0.dist(mic1)*10

    i = np.logspace(np.log10(distmin + (1 / res)), np.log10(distmax), res)
    circle = np.vectorize(find3D)(mic0, mic1, delta, i)
    res_circle = (i/distmax)*(res)
    u = np.concatenate([c.draw(int(r)) for c, r in zip(circle, res_circle)])
    surface = u.reshape(-1, 3)

    return surface


def reduce(points1, points2, points3, lim=100):
    #this function reduce the number of points to lim
    stop = False
    stop1=False
    stop2=False
    stop3=False
    perc=0.6
    while not stop:
        limits1 = np.array([np.min(points1, axis=0), np.max(points1, axis=0)])
        limits2 = np.array([np.min(points2, axis=0), np.max(points2, axis=0)])
        limits3 = np.array([np.min(points3, axis=0), np.max(points3, axis=0)])        
        # agrandir la limite de perc%
        limits1[0] = limits1[0] - perc*np.abs(limits1[0])
        limits1[1] = limits1[1] + perc*np.abs(limits1[1])
        limits2[0] = limits2[0] - perc*np.abs(limits2[0])
        limits2[1] = limits2[1] + perc*np.abs(limits2[1])
        limits3[0] = limits3[0] - perc*np.abs(limits3[0])
        limits3[1] = limits3[1] + perc*np.abs(limits3[1])

        #create a mask to filter out the points that are outside the limits
        mask1 = np.logical_and(
            points1 >= limits2[0], points1 <= limits2[1]).all(axis=1)
        mask2 = np.logical_and(
            points2 >= limits1[0], points2 <= limits1[1]).all(axis=1)
        mask3 = np.logical_and(
            points3 >= limits1[0], points3 <= limits1[1]).all(axis=1)
        mask4 = np.logical_and(
            points1 >= limits3[0], points1 <= limits3[1]).all(axis=1)
        mask5 = np.logical_and(
            points3 >= limits1[0], points3 <= limits1[1]).all(axis=1)
        mask6 = np.logical_and(
            points2 >= limits3[0], points2 <= limits3[1]).all(axis=1)
        
        old_len1=len(points1)
        old_len2=len(points2)
        old_len3=len(points3)

        mask1=np.logical_and(mask1,mask4)
        mask2=np.logical_and(mask2,mask6)
        mask3=np.logical_and(mask3,mask5)

        if len(points1[mask1]) > lim: points1 = points1[mask1]
        else : stop1=True
        if len(points2[mask2]) > lim: points2 = points2[mask2]
        else : stop2=True
        if len(points3[mask3]) > lim: points3 = points3[mask3] 
        else : stop3=True

        if old_len1==len(points1) and old_len2==len(points2) and old_len3==len(points3):
            perc=perc/1.8
      
        if (stop1 and stop2) or (stop1 and stop3) or (stop2 and stop3) or perc ==0:
            stop=True

    return points1, points2, points3


def find_intersect(points1, points2, points3):
    if(len(points1)*len(points2)*len(points3) <= 100000):
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

def compute_distance(point1, point2, point3):
    distance = np.sqrt(np.sum((point1 - point2)**2)) + np.sqrt(np.sum((point2 - point3)**2)) + np.sqrt(np.sum((point3 - point1)**2))
    i, j, k = np.argmin([point1, point2, point3], axis=0)
    return i, j, k, distance


def WhereItIs(mic0, mic1, mic2, mic3, delta1, delta2, delta3):
    points1 = whereItCouldBe3D(mic0, mic1, delta1)
    points2 = whereItCouldBe3D(mic0, mic2, delta2)
    points3 = whereItCouldBe3D(mic0, mic3, delta3)
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

    points1 = whereItCouldBe3D(
        mic0, mic1, delta1, res=700, distmin=distmin1, distmax=distmax1)
    points2 = whereItCouldBe3D(
        mic0, mic2, delta2, res=700, distmin=distmin2, distmax=distmax2)
    points3 = whereItCouldBe3D(
        mic0, mic3, delta3, res=700, distmin=distmin3, distmax=distmax3)
    
    points1, points2, points3 = reduce(points1, points2, points3, 50)

    return find_intersect(points1, points2, points3)
