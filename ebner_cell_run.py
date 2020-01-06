from neuron import h
from neuron.units import mV

from cells.cell_ebner2019 import CellEbner2019
from cells.core.cell_spine import CellSpine
from utils.Record import Record
from utils.utils import connect_net_stim, run_sim


class CellEbnerRxDCaSpine(CellEbner2019, CellSpine):
    def __init__(self, name):
        CellSpine.__init__(self, name)
        CellEbner2019.__init__(self, name)


REPS = 3			# Number of postsynaptic spikes
DT = 0.025 			# ms, integration step
AMP = 5.5 			# nA, amplitude of current injection to trigger postsynaptic spikes
DUR = 2.0			# ms, duration of the current injection
COOL_DOWN = 100		# ms, silence phase after stimulation
FREQ = 200			# Hz, frequency of postsynaptic spikes
WEIGHT = 0.0035		# µS, conductance of (single) synaptic potentials
WARMUP = 200

if __name__ == '__main__':
    h.load_file('stdrun.hoc')

    # define cell
    cell = CellEbnerRxDCaSpine(name="cell")
    cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, add_const_segs=11)
    cell.add_spines(spine_number=10, head_nseg=10, neck_nseg=10, sections='dend')
    cell.add_soma_mechanisms()
    cell.add_apical_mechanisms(sections='dend head neck')
    cell.add_4p_synapse(sections="head", loc=0.99)

    # stimulation
    for syn in cell.syns_4p.values():
        stim, con = connect_net_stim(syn, weight=WEIGHT, delay=WARMUP+1)

    # create plots
    rec = Record(cell.filter_secs("soma head[0]"), locs=0.5, variables="v")

    # init and run
    h.finitialize(-70 * mV)
    run_sim(runtime=100, warmup=WARMUP)

    # plot
    rec.plot()