from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
import numpy as np

from .helpers import fov_from_K, plot_text


def plot_camera_fov(
    ax: Axes3D,
    K: np.ndarray,
    rt: np.ndarray,
    shape: tuple[int, int],
    scale: float = 0.05,
    color: str = "k",
    fill: bool = False,
    alpha: float = 0.15,
    name: str | None = None,
) -> Axes3D:
    """Draw camera field-of-view frustum.

    Plot a camera field-of-view (FOV) frustum in 3D.

    Parameters
    ----------
    ax : Axes3D
        Target Matplotlib 3D axes on which to draw the camera FOV.
    rt : (4,4) ndarray
        Pose of camera in world
    scale : float, optional
        Distance from the camera center to the far plane of the FOV pyramid, in world units.
        Default is 0.05
    color : str, optional
        Color for frustum edges and surface (default `'k'`).
    fill : bool, optional
        Whether to fill the far-plane polygon of the frustum (default True).
    alpha : float, optional
        Transparency of the filled frustum face (default 0.15).
    linewidth : float, optional
        Width of the frustum edge lines (default 1.0).
    name : str, optional
        Optional name or label for this camera. If provided and `show_legend=True`,
        the frustum will be included in the plot legend.
    """

    hfov, vfov = fov_from_K(K, shape)
    tx, ty = np.tan(hfov / 2), np.tan(vfov / 2)

    # Rays in camera coordinates (normalized)
    rays_c = np.array(
        [
            [-tx, -ty, 1.0],
            [tx, -ty, 1.0],
            [tx, ty, 1.0],
            [-tx, ty, 1.0],
        ]
    )
    rays_c /= np.linalg.norm(rays_c, axis=1, keepdims=True)
    corners_w = (rt[:3, :3] @ (rays_c.T * scale)).T + rt[:3, 3]

    # Lines from center and frustum edges
    segs = [[rt[:3, 3], p] for p in corners_w]
    segs += [[corners_w[i], corners_w[(i + 1) % 4]] for i in range(4)]
    lc = Line3DCollection(segs, colors=color, linewidths=1.0)
    ax.add_collection3d(lc)

    if fill:
        poly = Poly3DCollection([corners_w], alpha=alpha, facecolor=color)
        ax.add_collection3d(poly)

    plot_text(ax, rt[:3, 3], name)

    return ax


__all__ = ["plot_camera_fov"]
