from typing import Tuple

import numpy as np
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
from mpl_toolkits.mplot3d.axes3d import Axes3D

from .helpers import plot_text


def plot_plane(
    ax: Axes3D,
    rt: np.ndarray,  # 4x4 local plane frame -> world
    extent_xy: Tuple[float, float],  # (size_x, size_y) in plane-local units
    *,
    facecolor: str = "C0",
    edgecolor: str = "k",
    alpha: float = 0.25,
    linewidth: float = 0.5,
    scale: float = 0.05,
    draw_normal: bool = True,
    name: str | None = None,
) -> np.ndarray:
    """
    Plot a rectangular plane z=0 in its *local* frame, placed in the world by (R_wc, t_wc).

    Local frame convention:
      - Plane lies on local z=0
      - Local +x and +y span the rectangle
      - Local +z is the plane normal (right-handed)

    Parameters
    ----------
    ax : Axes3D
        Target 3D axes.
    rt : (4,4) ndarray
        Transformation from plane-local to world coordinates.
    extent_xy : (sx, sy)
        Side lengths of the rectangle along local x and y.
    facecolor, edgecolor : str
        Matplotlib colors for the plane.
    alpha : float
        Plane transparency.
    linewidth : float
        Edge line width.
    scale : float
        Length of the drawn normal.
    draw_normal : bool
        Draw the plane normal (+z in local) from the origin.
    name: str
        Name to attach to plane

    Returns
    -------
    corners_w : (4,3) ndarray
        World-space coordinates of the rectangle corners in CCW order.
    """
    sx, sy = extent_xy
    hx, hy = sx * 0.5, sy * 0.5

    # Local corners on z=0, CCW order
    corners_local = np.array(
        [
            [-hx, -hy, 0.0],
            [+hx, -hy, 0.0],
            [+hx, +hy, 0.0],
            [-hx, +hy, 0.0],
        ]
    )

    R = rt[:3, :3]
    t = rt[:3, 3]

    # To world: X_w = R_wc * X_local + t_wc
    corners_w = (R @ corners_local.T).T + t

    # Filled face
    poly = Poly3DCollection(
        [corners_w],
        facecolor=facecolor,
        edgecolor=edgecolor,
        alpha=alpha,
        linewidths=linewidth,
    )
    ax.add_collection3d(poly)

    # Perimeter edges (optional but looks nicer/sharper)
    edges = [[corners_w[i], corners_w[(i + 1) % 4]] for i in range(4)]
    ax.add_collection3d(Line3DCollection(edges, colors=edgecolor, linewidths=linewidth))

    if draw_normal:
        n = R[:, 2]
        ax.quiver(*t, *n * scale, color="b")

    plot_text(ax, t * 1.05, name)

    return corners_w


__all__ = ["plot_plane"]
