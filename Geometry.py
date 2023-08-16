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
        t = np.linspace(0, 2*np.pi, 100)
        x = radius * np.cos(t)
        y = radius * np.sin(t)

        # Rotate the points to account for the orientation of the circle in 3D space
        points = np.column_stack((x, y, np.zeros_like(t)))
        points = np.dot(points, np.array([x_axis, y_axis, z_axis]))

        # Translate the points to the origin of the circle
        points += center

        return points


def angle_between(v1, v2):
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    return np.arccos(cos_theta)



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

    circle = Circle((x_mid,y_mid,z_mid), h, vector_orthogonal)
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


def whereItCouldBe3D(mic0, mic1, delta):
    surface = np.empty((0, 3))  # Initialize with an empty 2D array
    distmin = (mic0.dist(mic1) - delta) / 2
    distmax = 50
    res = 100
    for i in np.logspace(np.log10(distmin + (1 / res)), np.log10(distmax), res):
        circle = find3D(mic0, mic1, delta, i)
        u = circle.draw(100)
        surface = np.append(surface, u, axis=0)
    return surface



mic1=Mic(0, 0, 0)
mic2=Mic(10,10, 5)
mic3=Mic(-20, 20, 10)

points = whereItCouldBe3D(mic1, mic2, 14)
points2 = whereItCouldBe3D(mic1, mic3, 10)


fig = plt.figure()
ax = fig.add_subplot(projection='3d')
# Show mic
ax.scatter(mic1.x, mic1.y, mic1.z, color='red')
ax.scatter(mic2.x, mic2.y, mic2.z, color='green')
ax.scatter(mic3.x, mic3.y, mic3.z, color='orange')

#transform all the circle into one surface
ax.plot(points[:,0], points[:,1], points[:,2])
#ax.plot(points2[:,0], points2[:,1], points2[:,2])

intersection = np.intersect1d(points, points2)

print(intersection)

plt.xlim(-10, 10)
plt.ylim(-10, 10)
ax.set_zlim(-10, 10)
plt.xlabel('X')
plt.ylabel('Y')
ax.set_zlabel('Z')
plt.show()