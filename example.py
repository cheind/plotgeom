import numpy as np
import matplotlib.pyplot as plt

import plotgeom as pg

np.random.seed(456)

# Create figure
fig = plt.figure(figsize=(10, 10))

# Helper to create 3d axis
ax = pg.make_ax(fig, proj="ortho")

# Plot world
pg.plot_axes(ax, rt=np.eye(4), scale=0.05, name="world")

# Plot a plane with limits
pose = pg.random_pose()
pg.plot_plane(
    ax,
    pose,
    extent_xy=(0.2, 0.1),
    name="plane 1",
    draw_normal=True,
    scale=0.05,
)

# Plot a camera with axes and FOV
pose = pg.random_pose()
K = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]])
img_size = (480, 640)  # (H, W)
pg.plot_camera_fov(ax, K, pose, (480, 640), scale=0.1)
pg.plot_axes(ax, pose, scale=0.05, name="camera")

# Ensure equal aspect
pg.set_axes_equal(ax)

# Show
plt.show()
