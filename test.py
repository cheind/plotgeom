import numpy as np
import matplotlib.pyplot as plt

import viewgeom as vg

fig = plt.figure(figsize=(10, 10))
ax = vg.make_ax(fig)

rx, ry, rz = np.deg2rad([25, 10, 30])
rt = (
    vg.translate([0.4, -0.2, 0.3]) @ vg.rotate_z(rz) @ vg.rotate_y(ry) @ vg.rotate_x(rx)
)

# Plot a 1.0 x 0.6 plane
vg.plot_plane(
    ax,
    rt,
    extent_xy=(1.0, 0.6),
    facecolor="C1",
    alpha=0.3,
    draw_axes=True,
    name="Testplane",
)


K = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]])
img_size = (480, 640)  # (H, W)

vg.plot_camera_fov(ax, K, np.eye(4), (480, 640), scale=0.1)
vg.plot_axes(ax, np.eye(4), scale=0.05, name="another name")


vg.set_axes_equal(ax)
plt.show()
