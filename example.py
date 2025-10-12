import numpy as np
import matplotlib.pyplot as plt

# Main import
import plotgeom as pg


np.random.seed(112)

# Create figure
fig = plt.figure(figsize=(10, 10))

# Helper to create 3d axis
ax = pg.make_ax(fig=fig, proj="persp")

# Plot world axes
pg.plot_axes(
    ax=ax,
    rt=np.eye(4),
    scale=0.05,
    name="world",
)

# Plot a plane with limits
pg.plot_plane(
    ax=ax,
    rt=pg.random_pose(),
    extent_xy=(0.2, 0.1),
    name="pi",
    draw_normal=True,
    normal_scale=0.05,
)

# Plot a ray
pg.plot_ray(
    ax=ax,
    origin=[0, 0, 0],
    dir=[0.1, 0.1, 0],
    linestyle="--",
    linewidth=1.0,
    name="ray",
)


# Helper function to produce camera params
def random_camera_params():
    pose = pg.random_pose()
    K = np.array([[800, 0, 320], [0, 800, 240], [0, 0, 1]])
    shape = (480, 640)
    hfov, vfov = pg.fov_from_K(K, shape)
    image = pg.generate_chessboard_image((8, 6), square_size=80)
    image[:80, :80] = (0, 1, 1)
    return pose, (hfov, vfov), image


# Plot camera field of view
pose, (hfov, vfov), image = random_camera_params()
pg.plot_camera_fov(
    ax=ax,
    rt=pose,
    hfov=hfov,
    vfov=vfov,
    scale=0.1,
)

# Add an image to far plane
pg.plot_camera_image(
    ax=ax,
    rt=pose,
    hfov=hfov,
    vfov=vfov,
    image=image,
    scale=0.1,
    tex_res=(32, 32),
)

# Mark camera origin
pg.plot_axes(ax, pose, scale=0.05, name="a camera")

# Final preps
pg.set_axes_equal(ax)
pg.style_ax(ax)

# Show
plt.show()
