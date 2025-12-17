import numpy as np
from mpl_toolkits.mplot3d import Axes3D

from .texts import plot_text, FONT_SIZE_SMALL


def plot_axes(
    ax: Axes3D,
    rt: np.ndarray,
    scale=0.05,
    name: str | None = None,
    axis_labels: tuple[str, str, str] | None = None,
):
    """Draw a set of xyz-axes"""

    t = rt[:3, 3]
    dirs = rt[:3, :3]

    l0 = ax.quiver(*t, *dirs[:, 0] * scale, color="r", arrow_length_ratio=0.25)  # +x
    l1 = ax.quiver(*t, *dirs[:, 1] * scale, color="g", arrow_length_ratio=0.25)  # +y
    l2 = ax.quiver(*t, *dirs[:, 2] * scale, color="b", arrow_length_ratio=0.25)  # +z

    # Plot name at origin
    if name is not None:
        plot_text(ax, t, name)

    # Plot axis labels near tips
    if axis_labels is not None:
        for i, (label, color) in enumerate(zip(axis_labels, ("r", "g", "b"))):
            tip = t + dirs[:, i] * scale
            plot_text(
                ax,
                tip,
                label,
                offset_scale=0.005,
                color=color,
                font_size=FONT_SIZE_SMALL,
            )

    return l0, l1, l2


__all__ = ["plot_axes"]
