from neuron import h, gui
import matplotlib.pyplot as plt

from cells.cell_hoc import CellHOC
from cells.cell_swc import CellSWC

h.load_file('import3d.hoc')

#cell = CellSWC(name='cell', swc_file='cells/morphology/swc/c91662.swc')
cell = CellHOC(name='cell', hoc_files="cells/morphology/hoc/Mig_geo5038804.hoc")
#ps = h.PlotShape(True).plot(plt)
ps = h.PlotShape(True)
ps.show(0)