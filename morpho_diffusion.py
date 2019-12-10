import time

import numpy as np
from neuron import h, gui, rxd
from neuron.units import mV, ms
import matplotlib.pyplot as plt

from cells.cell_hoc_rxd_ca_spine import CellHOCRxDCaSpine
from cells.cell_rxd_ca import CellRxDCa
from cells.cell_rxd_spine import CellRxDSpine
from cells.cell_swc_rxd_ca_spine import CellSWCRxDCaSpine
from utils import plot_cai

RUNTIME = 5000 * ms
STEPSIZE = 0.01 * ms
DELAY = 1 * ms  # between steps
THREADS = 32
INIT_SLEEP = 6  # seconds

max_delay = DELAY / 1000  # in seconds


class CellRxDSpineCa(CellRxDSpine):
    def _add_rxd(self, secs, dx_3d_size):
        """
        Must be called after all secs are set.
        @param secs:
        @param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.
        """

        reg = self.regs = rxd.Region(secs=secs, nrn_region='i', dx=dx_3d_size)
        self.ca = rxd.Species(regions=reg, initial=50e-6, name='ca', charge=2, d=0.6)
        self.cabuf = rxd.Species(regions=reg, initial=0.003, name='cabuf', charge=0)

        self.ca_cabuf = rxd.Species(regions=reg, initial=0, name='ca_cabuf', charge=0)
        self.reaction = rxd.Reaction(self.ca + self.cabuf, self.ca_cabuf, 100, 0.1)


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)
    h.dt = .1  # We choose dt = 0.1 here because the ratio of d * dt / dx**2 must be less than 1

    cell = CellRxDSpineCa(name="cell", spine_number=10, spine_nseg=20, threads=8, spine_not_in_by_name=['soma', 'axon'])

    cell.add_cylindric_sec(name="dend", diam=1, l=50, nseg=100)
    #cell.add_cylindric_sec(name="soma", diam=10, l=10, nseg=100)
    #cell.connect(fr='soma', to='dend')
    cell.add_spines()

    #cell = CellSWCRxDCaSpine(name='cell', spine_number=10, spine_nseg=20, threads=THREADS, seg_per_L_um=1,
    #                         swc_file='cells/morphology/swc/my.swc', spine_not_in_by_name=['soma', 'axon'])
    #cell = CellHOCRxDCaSpine(name='cell', hoc_files="cells/morphology/hoc/Mig_geo5038804.hoc",
    #                         spine_number=200, spine_nseg=40, threads=THREADS, seg_per_L_um=1)
    cell.add_rxd()

    # init
    h.finitialize(-65 * mV)
    for n in cell.ca.nodes:
        if 'Cell[cell].head' in str(n.segment) and n.segment.x > .9:
            n.concentration = 1.0
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