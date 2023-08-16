import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

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

# Circle parameters: center, radius, normal
circle_parameters = [
    (np.array([0, 0, 0]), 1.0, np.array([0, 0, 1])),
    (np.array([2, 2, 2]), 0.8, np.array([1, 0, 0])),
]

circle_data = [
    Circle(center, radius, normal) for center, radius, normal in circle_parameters
]

circle_points = [circle.draw(10) for circle in circle_data]

# Create a mesh connecting the outer points of the circles
mesh_points = np.vstack(circle_points)
mesh_triangles = []

num_circles = len(circle_points)
num_points_per_circle = len(circle_points[0])

for i in range(num_circles):
    for j in range(num_points_per_circle):
        p1 = i * num_points_per_circle + j
        p2 = ((i + 1) % num_circles) * num_points_per_circle + j
        p3 = i * num_points_per_circle + (j + 1) % num_points_per_circle
        p4 = ((i + 1) % num_circles) * num_points_per_circle + (j + 1) % num_points_per_circle
        
        mesh_triangles.append([p1, p2, p3])
        mesh_triangles.append([p2, p4, p3])

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Plot the mesh surface
mesh = Poly3DCollection(mesh_points[mesh_triangles])
ax.add_collection3d(mesh)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Surface through Outer Lines of Circles")

plt.show()
