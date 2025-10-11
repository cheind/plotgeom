from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
import numpy as np

from .texts import plot_text


def far_plane_corners(hfov: float, vfov: float, rt: np.ndarray, scale: float = 0.05):
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
    corners = (rt[:3, :3] @ (rays_c.T * scale)).T + rt[:3, 3]
    return corners


def fov_from_K(K: np.ndarray, shape: tuple[int, int]):
    """Extract field of view from intrinsics and image shape"""
    h, w = shape
    fx, fy = K[0, 0], K[1, 1]
    hfov = 2 * np.arctan(w / (2 * fx))
    vfov = 2 * np.arctan(h / (2 * fy))
    return hfov, vfov


def plot_camera_fov(
    ax: Axes3D,
    rt: np.ndarray,
    hfov: float,
    vfov: float,
    *,
    scale: float = 0.05,
    color: str = "k",
    fill: bool = False,
    alpha: float = 0.15,
    linewidth: float = 1.0,
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
    hfov: float
        Horizontal field of view
    vfov: float
        Vertical field of view
    scale : float, optional
        Distance from the camera center to the far plane of the FOV pyramid, in world units.
        Default is 0.05
    color : str, optional
        Color for frustum edges and surface (default `'k'`).
    fill : bool, optional
        Whether to fill the far-plane polygon of the frustum.
    alpha : float, optional
        Transparency of the filled frustum face (default 0.15).
    linewidth : float, optional
        Width of the frustum edge lines (default 1.0).
    name : str, optional
        Optional name or label for this camera. If provided and `show_legend=True`,
        the frustum will be included in the plot legend.
    """

    corners = far_plane_corners(hfov, vfov, rt, scale=scale)

    # Lines from center and frustum edges
    segs = [[rt[:3, 3], p] for p in corners]
    segs += [[corners[i], corners[(i + 1) % 4]] for i in range(4)]
    lc = Line3DCollection(segs, colors=color, linewidths=linewidth)
    ax.add_collection3d(lc)

    if fill:
        poly = Poly3DCollection([corners], alpha=alpha, facecolor=color)
        ax.add_collection3d(poly)

    plot_text(ax, rt[:3, 3], name)

    return ax


def plot_camera_image(
    ax: Axes3D,
    rt: np.ndarray,
    image: np.ndarray,
    hfov: float,
    vfov: float,
    *,
    scale: float = 0.05,
    origin: str = "upper",
    tex_res: tuple[int, int] = (64, 64),
    alpha: float = 0.8,
    name: str | None = None,
):
    corners = far_plane_corners(hfov, vfov, rt, scale=scale)

    img = np.asarray(image)
    if img.ndim == 2:
        img = np.stack([img] * 3, axis=-1)  # grayscale -> RGB
    if img.dtype != np.float32 and img.dtype != np.float64:
        img = img.astype(np.float32) / 255.0  # normalize to 0..1 for facecolors

    if origin.lower() == "lower":
        img = img[::-1, :, :]

    # Resample image
    tr, tc = tex_res
    H, W = img.shape[:2]
    rs = np.linspace(0, H - 1, tr).round().astype(int)
    cs = np.linspace(0, W - 1, tc).round().astype(int)
    img_resampled = img[rs][:, cs]  # (tr, tc, C)

    # Build bilinear surface over the quad: P(u,v) with u in [0,1] left -> right, v in [0,1] top -> # bottom, corners order: TL=c0, TR=c1, BR=c2, BL=c3
    c0, c1, c2, c3 = corners
    us = np.linspace(0.0, 1.0, tc)
    vs = np.linspace(0.0, 1.0, tr)
    U, V = np.meshgrid(us, vs)
    # Bilinear interpolation
    P = (
        (1 - U)[:, :, None] * (1 - V)[:, :, None] * c0
        + U[:, :, None] * (1 - V)[:, :, None] * c1
        + U[:, :, None] * V[:, :, None] * c2
        + (1 - U)[:, :, None] * V[:, :, None] * c3
    )  # (tr, tc, 3)

    X, Y, Z = P[..., 0], P[..., 1], P[..., 2]

    if img_resampled.shape[-1] == 4:
        # Matplotlib expects facecolors as MxNx4; use given alpha but also respect global alpha
        fc = img_resampled.copy()
        fc[..., 3] *= alpha
        surface = ax.plot_surface(
            X,
            Y,
            Z,
            rstride=1,
            cstride=1,
            facecolors=fc,
            linewidth=0,
            antialiased=False,
            shade=False,
        )
    else:
        surface = ax.plot_surface(
            X,
            Y,
            Z,
            rstride=1,
            cstride=1,
            facecolors=img_resampled,
            linewidth=0,
            antialiased=False,
            shade=False,
            alpha=alpha,
        )

    plot_text(ax, corners[0], name)

    return surface


__all__ = ["plot_camera_fov", "plot_camera_image", "fov_from_K"]
