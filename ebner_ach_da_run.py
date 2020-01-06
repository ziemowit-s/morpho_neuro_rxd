from neuron import h
from neuron.units import mV

from cells.cell_ebner2019_ach_da import CellEbner2019AChDA
from cells.core.cell_spine import CellSpine
from utils.Record import Record
from utils.utils import run_sim


class CellEbnerRxDCaSpine(CellEbner2019AChDA, CellSpine):
    def __init__(self, name):
        CellSpine.__init__(self, name)
        CellEbner2019AChDA.__init__(self, name)


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
    cell.add_4p_ach_da_synapse(sections="head", loc=1)  # add synapse at the top of each spine's head

    # stimulation
    cell.add_net_stim("syns_4p", weight=WEIGHT, start=WARMUP+1, delay=1)

    # create plots
    rec = Record(cell.filter_secs("soma head[0]"), locs=0.5, variables="v")

    # init and run
    h.finitialize(-70 * mV)
    run_sim(runtime=100, warmup=0)

    # plot
    rec.plot()