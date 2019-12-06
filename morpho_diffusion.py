import numpy as np
from neuron import h, gui, rxd
import matplotlib.pyplot as plt
from neuron.rxd.node import Node3D
from neuron.units import mV

from cells.cell_swc_rxd_ca_spine import CellSWCRxDCaSpine

THREADS = 8


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)
    h.dt = .1  # We choose dt = 0.1 here because the ratio of d * dt / dx**2 must be less than 1

    cell = CellSWCRxDCaSpine(name='cell', spine_number=500, threads=THREADS, seg_per_L_um=0.1,
                             is_3d=False, swc_file='cells/morphology/c91662.swc')
    cell.add_rxd()

    # init
    h.finitialize(-65 * mV)
    h.cvode.re_init()

    # plot shape
    ps = h.PlotShape(True)
    ps.variable('cai')
    ps.scale(0, 0.01)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot')

    print('done')