from neuron import h, rxd

from cells.cell_rxd_ca import CellRxDCa
from cells.cell_swc import CellSWC


class CellSWCRxDCaSpine(CellRxDCa, CellSWC):
    def __init__(self, name, swc_file, spine_number, mechanism=None):
        CellRxDCa.__init__(self, name, mechanism)
        CellSWC.__init__(self, name, swc_file, mechanism)
        for i in range(spine_number):
            self.add_sec(name="head_%s" % i, diam=1, l=1, nseg=50)
            self.add_sec(name="neck_%s" % i, diam=0.5, l=0.5, nseg=50)
            self.connect(fr='head_%s' % i, to='neck_%s' % i)

        self.add_rxd()


