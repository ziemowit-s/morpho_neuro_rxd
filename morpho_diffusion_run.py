from neuron import h
from neuron.units import mV

from cells.core.hoc_cell import HOCCell
from cells.core.rxd_cell import RxDCell
from cells.core.spine_cell import SpineCell
from cells.core.rxd_tools import RxDCa, RxDpmca, RxDncx
from utils.Record import Record
from utils.utils import connect_net_stim, get_shape_plot, run_sim


class CellRxDCaSpineCellCellCell(RxDCell, SpineCell, HOCCell):
    def __init__(self, name):
        RxDCell.__init__(self, name)
        SpineCell.__init__(self, name)
        HOCCell.__init__(self, name)

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


def get_ampa(sec, weight, delay):
    ampa = h.ExpSyn(sec(0.5))
    ampa.tau = 0.5
    ampa.e = 0
    stim, con = connect_net_stim(ampa, weight, delay)
    return ampa, stim, con


def get_nmda(sec, weight, delay):
    nmda = h.NMDAca(sec(0.5))
    nmda.fCa = 0.1  # fraction of Ca current (Bloodgood & Sabatini)
    nmda.tcon = 3
    nmda.tcoff = 100
    nmda.mgconc = 1  # (mM) standard Mg concnmda.gamma = 0.08 Larkum Science 2009 (sharpens voltage curve)
    stim, con = connect_net_stim(nmda, weight, delay)
    return nmda, stim, con


if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)
    h.dt = .1  # We choose dt = 0.1 here because the ratio of d * dt / dx**2 must be less than 1

    # define cell
    cell = CellRxDCaSpineCellCellCell(name="cell")
    cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, add_const_segs=11)
    cell.add_spines(spine_number=10, head_nseg=10, neck_nseg=10, sections='dend')
    cell.add_rxd(rxd_obj=RxDCa(), sec_names="soma dend head neck")
    cell.add_rxd(rxd_obj=RxDpmca(), sec_names="soma dend head neck")
    cell.add_rxd(rxd_obj=RxDncx(), sec_names="head neck")

    # plots
    ps_cai = get_shape_plot(variable='cai', min_val=0, max_val=0.01)
    ps_v = get_shape_plot(variable='v', min_val=-70, max_val=40)
    rec = Record(cell.filter_secs("head[0]"), locs=1, variables='ica cai')

    # init and run
    h.finitialize(-65 * mV)
    # make_stim(cell)
    make_head_ca2_concentration(cell)
    h.cvode.re_init()
    run_sim(runtime=100, stepsize=0.1, init_sleep=3, delay_between_steps=50, plot_shapes=[ps_cai, ps_v])

    rec.plot()
