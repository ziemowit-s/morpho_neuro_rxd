import time

import numpy as np
from neuron import h
from neuron.units import mV, ms

from cells.cell_hoc import CellHOC
from cells.cell_rxd import CellRxD
from cells.cell_spine import CellSpine
from cells.rxd_tools import RxDCa, RxDpmca, RxDncx
from utils import plot_cai, plot_v

RUNTIME = 1000 * ms
STEPSIZE = 0.01 * ms
DELAY = 1 * ms  # between steps
INIT_SLEEP = 3  # seconds

max_delay = DELAY / 1000  # in seconds


class CellSWCRxDCaSpine(CellRxD, CellSpine, CellHOC):
    def __init__(self, name):
        CellRxD.__init__(self, name)
        CellSpine.__init__(self, name)
        CellHOC.__init__(self, name)

"""
    if ($1 == 1) {	// AMPA
      soma syn = new Exp2Syn(0.5) pre_list.append(syn)
      syn.tau1 = 0.5
      syn.tau2 = 3
      syn.e = 0
      syn_list.append(syn)
    } else if ($1 == 2) {	// AMPA/NMDA
      soma syn = new Exp2Syn(0.5) pre_list.append(syn)
      syn.tau1 = 0.5	// Spruston JPhysiol 1995
      syn.tau2 = 3	// Spruston JPhysiol 1995
      syn.e = 0
      syn_list.append(syn)
      soma syn = new NMDAca(0.5) pre_list.append(syn)
      syn.fCa = 0.1	// fraction of Ca current (Bloodgood & Sabatini)
      syn.tcon = 3	
      syn.tcoff = 100
      syn.mgconc = 1	// (mM) standard Mg conc
      syn.gamma = 0.08	// Larkum Science 2009 (sharpens voltage curve)
      syn_list.append(syn)
    } else if ($1 == 3) {	// GABAA
      soma syn = new Exp2Syn(0.5) pre_list.append(syn)
      syn.tau1 = 1
      syn.tau2 = 8
      syn.e = -75
      syn_list.append(syn)
    } else if ($1 == 4) {	// GABAB
      soma syn = new Exp2Syn(0.5) pre_list.append(syn)
      syn.tau1 = 35
      syn.tau2 = 100
      syn.e = -75
      syn_list.append(syn)
"""

"""
$o2.sec connect $o3.sec(0), 1
      for i=0,$o1.count()-1 {
        $o3.sec $o1.o(i).loc(0.5)
"""


def make_stim(cell):
    for name, sec in cell.secs.items():
        sec.insert('hh')
        sec.insert('pas')
        if 'head' in name:
            ampa, ampa_stim, ampa_con = get_ampa(sec, weight=0.0, delay=0)
            nmda, nmda_stim, nmda_con = get_nmda(sec, weight=0.1, delay=0)
            ampa_stim.start = 0
            ampa_stim.number = 1

            nmda_stim.start = 0
            nmda_stim.number = 1


def make_head_ca2_concentration(cell):
    for n in cell.rxds['RxDCa'].ca.nodes:
        if 'Cell[cell].head' in str(n.segment) and n.segment.x > .9:
            n.concentration = 1.0


def get_con(syn, weight, delay):
    stim = h.NetStim()
    con = h.NetCon(stim, syn)
    con.delay = delay
    con.weight[0] = weight
    return stim, con


def get_ampa(sec, weight, delay):
    ampa = h.ExpSyn(sec(0.5))
    ampa.tau = 0.5
    ampa.e = 0
    stim, con = get_con(ampa, weight, delay)
    return ampa, stim, con


def get_nmda(sec, weight, delay):
    nmda = h.NMDAca(sec(0.5))
    nmda.fCa = 0.1  # fraction of Ca current (Bloodgood & Sabatini)
    nmda.tcon = 3
    nmda.tcoff = 100
    nmda.mgconc = 1  # (mM) standard Mg concnmda.gamma = 0.08 Larkum Science 2009 (sharpens voltage curve)
    stim, con = get_con(nmda, weight, delay)
    return nmda, stim, con


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)
    h.dt = .1  # We choose dt = 0.1 here because the ratio of d * dt / dx**2 must be less than 1

    cell = CellSWCRxDCaSpine(name="cell")
    cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, add_const_segs=11)
    cell.add_spines(spine_number=10, head_nseg=10, neck_nseg=10, sections='dend')
    cell.add_rxd(rxd_obj=RxDCa(), sections="soma dend head neck")
    cell.add_rxd(rxd_obj=RxDpmca(), sections="soma dend head neck")
    cell.add_rxd(rxd_obj=RxDncx(), sections="head neck")

    # init
    h.finitialize(-65 * mV)

    #make_stim(cell)
    make_head_ca2_concentration(cell)

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
