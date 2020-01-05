import time

import numpy as np
from neuron import h
from neuron.units import mV, ms

from cells.cell_ebner2019 import CellEbner2019
from cells.core.cell_rxd import CellRxD
from cells.core.cell_spine import CellSpine
from cells.core.rxd_tools import RxDCa, RxDpmca, RxDncx
from utils import plot_cai, plot_v

RUNTIME = 1000 * ms
STEPSIZE = 0.01 * ms
DELAY = 1 * ms  # between steps
INIT_SLEEP = 3  # seconds

max_delay = DELAY / 1000  # in seconds


class CellEbnerRxDCaSpine(CellEbner2019, CellRxD, CellSpine):
    def __init__(self, name):
        CellRxD.__init__(self, name)
        CellSpine.__init__(self, name)
        CellEbner2019.__init__(self, name)


def get_con(syn, weight, delay):
    stim = h.NetStim()
    con = h.NetCon(stim, syn)
    con.delay = delay
    con.weight[0] = weight
    return stim, con


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)
    h.dt = .1  # We choose dt = 0.1 here because the ratio of d * dt / dx**2 must be less than 1

    cell = CellEbnerRxDCaSpine(name="cell")
    #cell.load_morpho(filepath='morphologies/asc/cell1.asc', seg_per_L_um=1, add_const_segs=11)
    cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, add_const_segs=11)
    cell.add_spines(spine_number=10, head_nseg=10, neck_nseg=10, sections='dend')
    cell.add_soma_mechanisms()
    cell.add_apical_mechanisms(sections='dend')
    cell.add_4p_synapse(sections="head", loc=0.99)
    cell.add_rxd(rxd_obj=RxDCa(), sections="soma dend head neck")
    cell.add_rxd(rxd_obj=RxDpmca(), sections="soma dend head neck")
    cell.add_rxd(rxd_obj=RxDncx(), sections="head neck")

    # init
    h.finitialize(-65 * mV)
    h.cvode.re_init()

    # plots
    ps_cai = plot_cai()
    ps_v = plot_v()

    print("sleep before run for: %s seconds" % INIT_SLEEP)
    time.sleep(INIT_SLEEP)

    # run main loop
    before = time.time()  # compute time before
    for i in np.arange(0, RUNTIME, STEPSIZE):

        # step till i-th ms
        h.continuerun(i * ms)
        current = time.time()
        computation_time = current - before

        # adjust delay
        delay = max_delay - computation_time
        if delay < 0:
            delay = 0
        time.sleep(delay)
        before = time.time()  # compute time before

        # flush shape and console log
        ps_cai.fastflush()
        ps_v.fastflush()
        print(round(i, 2), "ms", '// comp_time_ms:', round(computation_time * 1000, 0))
