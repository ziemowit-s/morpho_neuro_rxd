import time

import numpy as np
from neuron import h
from neuron.units import mV, ms

from cells.cell_rxd import CellRxD
from cells.cell_spine import CellSpine
from cells.cell_swc import CellSWC
from cells.rxd_tools import RxDCa
from utils import plot_cai

RUNTIME = 5000 * ms
STEPSIZE = 0.01 * ms
DELAY = 1 * ms  # between steps
THREADS = 32
INIT_SLEEP = 6  # seconds

max_delay = DELAY / 1000  # in seconds


class CellSWCRxDCaSpine(CellSWC, CellSpine):
    def __init__(self, name):
        CellSWC.__init__(self, name)
        #CellRxD.__init__(self, name)
        CellSpine.__init__(self, name)


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)
    h.dt = .1  # We choose dt = 0.1 here because the ratio of d * dt / dx**2 must be less than 1

    cell = CellSWCRxDCaSpine(name="cell")
    cell.add_swc(swc_file='morphology/swc/my.swc', seg_per_L_um=1, add_const_segs=11)
    cell.add_spines(spine_number=10, head_nseg=10, neck_nseg=10, sections='dend')
    #cell.add_rxd(rxd_obj=RxDCa(), sections="dend head neck")

    # init
    h.finitialize(-65 * mV)
    #for n in cell.rxd.ca.nodes:
    #    if 'Cell[cell].head' in str(n.segment) and n.segment.x > .9:
    #        n.concentration = 1.0
    h.cvode.re_init()

    # plots
    ps = plot_cai()

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
        ps.fastflush()
        print(round(i, 2), "ms", '// comp_time_ms:', round(computation_time * 1000, 0))
