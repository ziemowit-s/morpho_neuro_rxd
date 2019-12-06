from neuron import h, rxd

from cells.cell import Cell

h.load_file('import3d.hoc')


class CellSWC(Cell):
    def __init__(self, name, swc_file, mechanism=None, seg_per_L_um=1.0, add_const_segs=11):
        """
        @param name:
            Name of the cell
        @param swc_file:
            swc file path
        @param mechanism:
            Single MOD mechanism or a list of MOD mechanisms
        @param seg_per_L_um:
            how many segments per single um of L, Length.  Can be < 1. None is 0.
        @param add_const_segs:
            how many segments have each section by default.
            With each um of L this number will be increased by seg_per_L_um
        """
        Cell.__init__(self, name, mechanism)
        if swc_file is None:
            raise FileNotFoundError("swc file need to be specified, found NONE.")
        morpho = h.Import3d_SWC_read()
        morpho.input(swc_file)
        h.Import3d_GUI(morpho, 0)
        i3d = h.Import3d_GUI(morpho, 0)
        i3d.instantiate(self)

        for sec in self.all:
            name = sec.name().split('.')[-1]  # eg. name="dend[19]"
            self.secs[name] = sec

        add = int(sec.L*seg_per_L_um) if seg_per_L_um is not None else 0
        for sec in self.secs.values():
            sec.nseg = add_const_segs + add

