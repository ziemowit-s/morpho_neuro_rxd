from neuron import h, gui

from cells.cell_hoc_rxd_ca_spine import CellHOCRxDCaSpine

h.load_file('import3d.hoc')

cell = CellHOCRxDCaSpine(name='cell', hoc_files="cells/morphology/hoc/Mig_geo5038804.hoc",
                         spine_number=2000, spine_nseg=20)
ps = h.PlotShape(True)
ps.show(0)