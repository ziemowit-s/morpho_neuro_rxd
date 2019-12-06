import numpy as np
from neuron import h, gui
from neuron.units import mV, ms
import matplotlib.pyplot as plt
import time

from cells.cell_rxd_ca import CellRxDCa

RUNTIME = 5 * ms
STEPSIZE = 0.01 * ms
DELAY = 20 * ms  # between steps


def get_mol(sec, loc):
    return round(sec(loc).cai*1000, 2)  # in uM


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)

    cell = CellRxDCa(name="cell")
    cell.add_cylindric_sec(name="head", diam=1, l=1, nseg=50)
    cell.add_cylindric_sec(name="neck", diam=0.5, l=0.5, nseg=50)
    cell.add_cylindric_sec(name="dend", diam=0.5, l=5, nseg=100)
    cell.connect(fr='head', to='neck')
    cell.connect(fr='neck', to='dend', to_loc=0.5)
    cell.add_rxd()

    # init
    h.finitialize(-65*mV)
    head_last = cell.secs['head'].nseg+cell.secs['neck'].nseg+cell.secs['dend'].nseg - 1
    cell.ca.nodes[head_last].concentration = 0.5
    h.cvode.re_init()

    # plot shape
    ps = h.PlotShape(True)
    ps.variable('cai')
    ps.scale(0, 0.01)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot')
    h.PlotShape(False).plot(plt)

    # run
    sleep = 3
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
        neck_cai2 = get_mol(cell.secs['neck'], 0.2)
        neck_cai1 = get_mol(cell.secs['neck'], 0.1)

        dend_cai2 = get_mol(cell.secs['dend'], 0.5)  # left
        dend_cai1 = get_mol(cell.secs['dend'], 0.4)  # center
        dend_cai3 = get_mol(cell.secs['dend'], 0.6)  # right
        print('         ', round(i, 2), "ms")

        print('      |===========|')
        print('      |   ', neck_cai2, '  |')
        print('      |----%s----|' % round(neck_cai2-neck_cai1, 1))
        print('      |   ', neck_cai1, '  |')
        print('===========%s============' % round(neck_cai1-dend_cai2, 1))
        print('<-', dend_cai1, '|', dend_cai2, '|', dend_cai3, '->')
        print('==========================')
        print('comp_time_ms:', round(comp_time_ms*1000, 0))
        print()

