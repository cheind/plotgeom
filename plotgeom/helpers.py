import numpy as np
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D


def make_ax(
    fig: Figure, pos: int = 111, elev: float = 30, azim: float = -37.5, proj="persp"
) -> Axes3D:
    """Create a new 3D matplot axis at desired subplot position"""
    ax = fig.add_subplot(pos, projection="3d")
    ax.set_box_aspect((1, 1, 1))
    ax.set_proj_type(proj)
    ax.view_init(elev=elev, azim=azim)
    return ax


def set_axes_equal(ax: Axes3D):
    """Make 3D plot axes have equal scale (aspect-correct)."""
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    plot_radius = 0.5 * max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])
    ax.set_zlim3d([z_middle - plot_radius, z_middle + plot_radius])


def plot_text(ax: Axes3D, pos: np.ndarray, txt: str | None):
    if txt is not None:
        ax.text(*pos, txt, fontsize=10)


def rotate_x(rx: float):
    R = np.array(
        [
            [1, 0, 0, 0],
            [0, np.cos(rx), -np.sin(rx), 0],
            [0, np.sin(rx), np.cos(rx), 0],
            [0, 0, 0, 1],
        ]
    )
    return R


def rotate_y(ry: float):
    R = np.array(
        [
            [np.cos(ry), 0, np.sin(ry), 0],
            [0, 1, 0, 0],
            [-np.sin(ry), 0, np.cos(ry), 0],
            [0, 0, 0, 1],
        ]
    )
    return R


def rotate_z(rz: float):
    R = np.array(
        [
            [np.cos(rz), -np.sin(rz), 0, 0],
            [np.sin(rz), np.cos(rz), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ]
    )
    return R


def translate(xyz: np.ndarray):
    T = np.eye(4)
    T[:3, 3] = np.asarray(xyz)
    return T


def random_pose():
    r = np.random.rand(6) * 2 - 1.0

    return (
        translate(r[3:] * 0.1)
        @ rotate_z(r[2] * np.pi / 2)
        @ rotate_y(r[1] * np.pi / 2)
        @ rotate_x(r[0] * np.pi / 2)
    )


def fov_from_K(K: np.ndarray, shape: tuple[int, int]):
    """Extract field of view from intrinsics and image shape"""
    h, w = shape
    fx, fy = K[0, 0], K[1, 1]
    hfov = 2 * np.arctan(w / (2 * fx))
    vfov = 2 * np.arctan(h / (2 * fy))
    return hfov, vfov


__all__ = [
    "make_ax",
    "set_axes_equal",
    "rotate_x",
    "rotate_y",
    "rotate_z",
    "translate",
    "plot_text",
    "random_pose",
]
