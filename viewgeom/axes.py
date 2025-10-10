import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from .helpers import plot_text


def plot_axes(ax: Axes3D, rt: np.ndarray, scale=0.05, name: str | None = None):
    """Draw a set of xyz-axes"""

    t = rt[:3, 3]
    dirs = rt[:3, :3]

    l0 = ax.quiver(*t, *dirs[:, 0] * scale, color="r", arrow_length_ratio=0.25)  # +x
    l1 = ax.quiver(*t, *dirs[:, 1] * scale, color="g", arrow_length_ratio=0.25)  # +y
    l2 = ax.quiver(*t, *dirs[:, 2] * scale, color="b", arrow_length_ratio=0.25)  # +z

    plot_text(ax, t * 1.05, name)

    return l0, l1, l2


__all__ = ["plot_axes"]
