import abc
import numpy as np
from neuron import rxd
import matplotlib.pyplot as plt
from neuron.rxd.node import Node3D


class RxDTool:
    @abc.abstractmethod
    def load(self, sections, dx_3d_size):
        """
        Must be called after all secs are set.
        @param secs:
        @param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.
        """
        raise NotImplementedError


class RxDCa(RxDTool):

    def load(self, sections, dx_3d_size):
        """
        Must be called after all secs are set.
        @param secs:
        @param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.
        """

        reg = self.regs = rxd.Region(secs=sections, nrn_region='i', dx=dx_3d_size)
        self.ca = rxd.Species(regions=reg, initial=50e-6, name='ca', charge=2, d=0.6)
        self.cabuf = rxd.Species(regions=reg, initial=0.003, name='cabuf', charge=0)

        self.ca_cabuf = rxd.Species(regions=reg, initial=0, name='ca_cabuf', charge=0)
        self.reaction = rxd.Reaction(self.ca + self.cabuf, self.ca_cabuf, 100, 0.1)


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