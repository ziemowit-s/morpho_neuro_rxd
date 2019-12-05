from neuron import h, rxd

from cells.cell import Cell

h.load_file('import3d.hoc')


class CellSWC(Cell):
    def __init__(self, name, swc_file, mechanism=None):
        Cell.__init__(self, name, mechanism)
        if swc_file is None:
            raise FileNotFoundError("swc file need to be specified, found NONE.")
        morpho = h.Import3d_SWC_read()
        morpho.input(swc_file)
        h.Import3d_GUI(morpho, 0)
        i3d = h.Import3d_GUI(morpho, 0)
        i3d.instantiate(self)

        self.segs = self.all
        for sec in self.segs:
            sec.nseg = 1 + 10 + int(sec.L/5)


