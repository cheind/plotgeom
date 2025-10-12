import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from .texts import plot_text


def plot_ray(
    ax: Axes3D,
    origin: np.ndarray,
    dir: np.ndarray,
    scale: float = 1.0,
    linewidth: float = 0.5,
    linestyle: str = "-",
    color: str = "C0",
    name: str | None = None,
):
    """Draw a single ray.

    Parameters
    ----------
    ax : Axes3D
        Target 3D axes.
    origin : (*,3) ndarray
        Ray origins.
    dir : (*,3) ndarray
        Ray directions.
    linewidth : float
        Ray line width.
    linestyle: str
        Line style to apply.
    scale : float
        Length of the drawn normal.
    draw_normal : bool
        Draw the plane normal (+z in local) from the origin.
    name: str
        Name to attach to plane


    """

    origin = np.asarray(origin)
    dir = np.asarray(dir)

    mid = (origin + (origin + dir * scale)) * 0.5
    l0 = ax.quiver(
        *origin,
        *(dir * scale),
        color=color,
        arrow_length_ratio=0.05,
        linewidth=linewidth,
        linestyle=linestyle,
    )

    plot_text(ax, mid, name)

    return l0


__all__ = ["plot_ray"]
