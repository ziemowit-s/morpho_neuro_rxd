from neuron import h
from neuron.units import mV
import matplotlib.pyplot as plt

from cells.ebner2019_ach_da_cell import Ebner2019AChDACellNet
from cells.core.netstim_cell import NetStimCell
from cells.core.spine_cell import SpineCell
from utils.Record import Record
from utils.utils import run_sim


class EbnerRxDCaSpineCell(Ebner2019AChDACellNet, SpineCell):
    def __init__(self, name):
        SpineCell.__init__(self, name)
        Ebner2019AChDACellNet.__init__(self, name)


WEIGHT = 0.0035		# µS, conductance of (single) synaptic potentials
WARMUP = 200


if __name__ == '__main__':
    h.load_file('stdrun.hoc')

    # define cell
    cell = EbnerRxDCaSpineCell(name="cell")
    cell.load_morpho(filepath='morphologies/swc/my.swc', seg_per_L_um=1, add_const_segs=11)
    cell.add_spines(spine_number=10, head_nseg=10, neck_nseg=10, sections='dend')
    cell.add_soma_mechanisms()
    cell.add_apical_mechanisms(sections='dend head neck')
    cell.add_4p_ach_da_synapse(sec_names="head", loc=1)  # add synapse at the top of each spine's head

    # Create stims
    s1 = NetStimCell("stim_cell")
    stim1 = s1.add_netstim("stim1", start=WARMUP + 1)
    stim2 = s1.add_netstim("stim2", start=WARMUP + 100)

    # stimulation
    cell.add_netcons(source=stim1, weight=WEIGHT, delay=1, pp_type_name="SynACh", sec_names="head[0][0]")
    cell.add_netcons(source=stim1, weight=WEIGHT, delay=1, pp_type_name="SynDa", sec_names="head[0][0]")

    # create plots
    rec_4psyn = Record(cell.filter_point_processes(pp_type_name="Syn4PAChDa", sec_names="head[0][0]"), variables="LTD_pre w")

    # init and run
    h.finitialize(-70 * mV)
    run_sim(runtime=500, warmup=WARMUP)

    # plot
    rec_4psyn.plot()
    plt.show()
