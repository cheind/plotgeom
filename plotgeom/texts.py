import numpy as np
from mpl_toolkits.mplot3d import Axes3D


FONT_SIZE_DEFAULT = 10
FONT_SIZE_LARGE = FONT_SIZE_DEFAULT * 1.2
FONT_SIZE_SMALL = FONT_SIZE_DEFAULT * 0.8


def plot_text(
    ax: Axes3D,
    pos: np.ndarray,
    txt: str | None,
    offset_dir=(0, 0, 1),
    offset_scale=0.01,
    color: str = "k",
    font_size: float | int = FONT_SIZE_DEFAULT,
):
    """Plot text anchored at `pos` oriented towards the viewer."""
    if txt is None:
        return
    pos = np.array(pos)
    offset = offset_scale * np.array(offset_dir)
    pos_off = pos + offset
    ax.text(
        *pos_off,
        txt,
        fontsize=font_size,
        color=color,
        ha="center",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7),
    )


__all__ = ["plot_text", "BASE_FONT_SIZE"]
