import numpy as np
from neuron import h, rxd
import matplotlib.pyplot as plt
from neuron.rxd.node import Node3D


def plot_cai():
    # plot shape
    ps = h.PlotShape(True)
    ps.variable('cai')
    ps.scale(0, 0.01)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot')
    return ps


def plot_contours(species: rxd.Species):
    r = species.nodes[0].region
    if not hasattr(r, '_xs'):
        raise LookupError("For RxD ionic contour plot - you must use 3D RxD model.")
    xz = np.empty((max(r._xs)+1, max(r._zs)+1))
    xz.fill(np.nan)

    def replace_nans(a, b):
        if np.isnan(a):
            return b
        return max(a, b)

    for node in species.nodes:
        if isinstance(node, Node3D):
            xz[node._i, node._k] = replace_nans(xz[node._i, node._k], node.value)

    xs, ys = np.meshgrid(range(xz.shape[1]), range(xz.shape[0]))
    plt.contour(xs, ys, np.nan_to_num(xz), 0.5, colors='k', linewidths=0.5)
    plt.axis('equal')
    plt.axis('off')
