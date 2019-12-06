import time

import numpy as np
from neuron import h, gui, rxd
import matplotlib.pyplot as plt
from neuron.rxd.node import Node3D
from neuron.units import mV, ms

from cells.cell_swc_rxd_ca_spine import CellSWCRxDCaSpine

RUNTIME = 50 * ms
STEPSIZE = 0.01 * ms
DELAY = 20 * ms  # between steps
THREADS = 32


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


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)
    h.dt = .1  # We choose dt = 0.1 here because the ratio of d * dt / dx**2 must be less than 1

    cell = CellSWCRxDCaSpine(name='cell', spine_number=50, threads=THREADS, seg_per_L_um=1,
                             swc_file='cells/morphology/4-14-2016-sl2-c3-basal-dendrite.CNG.swc')
    cell.add_rxd()

    # init
    h.finitialize(-65 * mV)
    for n in cell.ca.nodes:
        if 'Cell[cell].head' in str(n.segment) and n.segment.x >.9:
            n.concentration = 0.1
    h.cvode.re_init()

    # plot shape
    ps = h.PlotShape(True)
    ps.variable('cai')
    ps.scale(0, 0.01)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot')

    #play
    sleep = 10
    print("sleep before run for: %s seconds" % sleep)
    time.sleep(sleep)
    before = time.time()
    const_delay = DELAY / 1000  # in seconds
    for i in np.arange(0, RUNTIME, STEPSIZE):
        h.continuerun(i * ms)
        current = time.time()
        comp_time_ms = current - before

        delay = const_delay - comp_time_ms
        if delay < 0:
            delay = 0

        time.sleep(delay)
        before = time.time()
        ps.fastflush()
        print(round(i, 2), "ms", '// comp_time_ms:', round(comp_time_ms * 1000, 0))