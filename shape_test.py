from neuron import h, gui
import matplotlib.pyplot as plt
import numpy as np

from cells.cell_swc import CellSWC

h.load_file('import3d.hoc')

cell = CellSWC(name='cell', swc_file='cells/morphology/4-14-2016-sl2-c3-basal-dendrite.CNG.swc')

ps = h.PlotShape(True).plot(plt)