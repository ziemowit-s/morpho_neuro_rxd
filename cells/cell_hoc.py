from neuron import h
from nrn import Section

from cells.cell import Cell


class CellHOC(Cell):
    def add_hoc(self, hoc_file, seg_per_L_um=1.0, add_const_segs=11):
        """
        @param hoc_file:
            paths to hoc file
        @param seg_per_L_um:
            how many segments per single um of L, Length.  Can be < 1. None is 0.
        @param add_const_segs:
            how many segments have each section by default.
            With each um of L this number will be increased by seg_per_L_um
        """
        h.load_file(hoc_file)

        # add potential new Sections from hoc file to self.secs dictionary
        for d in dir(h):
            try:
                f = getattr(h, d)
                if isinstance(f, Section):
                    self.secs[f.name()] = f
                elif len(f) > 0 and isinstance(f[0], Section):
                    for ff in f:
                        self.secs[ff.name()] = ff
            except TypeError:
                continue

        # change segment number based on seg_per_L_um and add_const_segs
        for sec in self.secs.values():
            add = int(sec.L * seg_per_L_um) if seg_per_L_um is not None else 0
            sec.nseg = add_const_segs + add

