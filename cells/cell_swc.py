from os import path

from neuron import h, gui

from cells.cell import Cell

h.load_file('import3d.hoc')


class CellSWC(Cell):
    def add_swc(self, swc_file, seg_per_L_um=1.0, add_const_segs=11):
        """
        @param swc_file:
            swc file path
        @param seg_per_L_um:
            how many segments per single um of L, Length.  Can be < 1. None is 0.
        @param add_const_segs:
            how many segments have each section by default.
            With each um of L this number will be increased by seg_per_L_um
        """
        # SWC importing
        if not path.exists(swc_file):
            raise FileNotFoundError()
        morpho = h.Import3d_SWC_read()
        morpho.input(swc_file)
        h.Import3d_GUI(morpho, 0)
        i3d = h.Import3d_GUI(morpho, 0)
        i3d.instantiate(self)

        # add all SWC sections to self.secs; self.all is defined by SWC import
        for sec in self.all:
            name = sec.name().split('.')[-1]  # eg. name="dend[19]"
            self.secs[name] = sec

        # change segment number based on seg_per_L_um and add_const_segs
        for sec in self.secs.values():
            add = int(sec.L*seg_per_L_um) if seg_per_L_um is not None else 0
            sec.nseg = add_const_segs + add

