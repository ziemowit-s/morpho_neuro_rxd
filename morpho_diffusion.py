import time

import numpy as np
from neuron import h, gui
from neuron.units import mV, ms

from cells.cell_swc_rxd_ca_spine import CellSWCRxDCaSpine
from utils import plot_cai

RUNTIME = 50 * ms
STEPSIZE = 0.01 * ms
DELAY = 20 * ms  # between steps
THREADS = 32
INIT_SLEEP = 3  # seconds

max_delay = DELAY / 1000  # in seconds


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
        if 'Cell[cell].head' in str(n.segment) and n.segment.x > .9:
            n.concentration = 0.1
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