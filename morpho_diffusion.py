from neuron import h, gui, rxd
import matplotlib.pyplot as plt
from neuron.units import mV

from cells.cell_swc_rxd_ca_spine import CellSWCRxDCaSpine

if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)
    rxd.nthread(8)

    cell = CellSWCRxDCaSpine(name='cell', spine_number=10, swc_file='cells/morphology/c91662.swc')

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