import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def plot_text(
    ax: Axes3D,
    pos: np.ndarray,
    txt: str | None,
    offset_dir=(0, 0, 1),
    offset_scale=0.01,
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
        fontsize=10,
        color="k",
        ha="center",
        va="bottom",
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.7),
    )


__all__ = ["plot_text"]
