import time

from neuron import h
from neuron.units import mV

from cells.cell_ebner2019 import CellEbner2019
from cells.core.cell_rxd import CellRxD
from cells.core.cell_spine import CellSpine
from utils import connect_net_stim, run_sim, get_shape_plot


class CellEbnerRxDCaSpine(CellEbner2019, CellRxD, CellSpine):
    def __init__(self, name):
        CellRxD.__init__(self, name)
        CellSpine.__init__(self, name)
        CellEbner2019.__init__(self, name)


REPS = 3			# Number of postsynaptic spikes
DT = 0.025 			# ms, integration step
AMP = 5.5 			# nA, amplitude of current injection to trigger postsynaptic spikes
DUR = 2.0			# ms, duration of the current injection
COOL_DOWN = 100		# ms, silence phase after stimulation
FREQ = 200			# Hz, frequency of postsynaptic spikes
WEIGHT = 0.0035		# µS, conductance of (single) synaptic potentials

if __name__ == '__main__':
    h.load_file('stdrun.hoc')
    h.cvode.atol(1e-8)
    h.cvode.active(1)
    h.dt = .1

    cell = CellEbnerRxDCaSpine(name="cell")
    cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, add_const_segs=11)
    cell.add_spines(spine_number=10, head_nseg=10, neck_nseg=10, sections='dend')
    cell.add_soma_mechanisms()
    cell.add_apical_mechanisms(sections='dend head neck')
    cell.add_4p_synapse(sections="head", loc=0.99)

    stim, con = connect_net_stim(list(cell.synapses_4p.values())[0], weight=WEIGHT, delay=10)

    # init
    h.finitialize(-65 * mV)
    h.cvode.re_init()

    # plots
    ps_ca = get_shape_plot(variable='ica', min_val=-3, max_val=10)
    ps_v = get_shape_plot(variable='v')

    init_sleep = 3  # seconds
    print("sleep before run for: %s seconds" % init_sleep)
    time.sleep(init_sleep)

    run_sim(runtime=1000, stepsize=100, delay_between_steps=500, plot_shapes=[ps_ca, ps_v])