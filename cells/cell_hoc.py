from neuron import h
from nrn import Section

from cells.cell import Cell


class CellHOC(Cell):
    def __init__(self, name, mechanism=None, hoc_files=None, seg_per_L_um=1.0, add_const_segs=11):
        """
        @param name:
            Name of the cell
        @param mechanism:
            Single MOD mechanism or a list of MOD mechanisms
        @param hoc_files:
            list of string paths to hoc files or single string of single hoc file
        @param seg_per_L_um:
            how many segments per single um of L, Length.  Can be < 1. None is 0.
        @param add_const_segs:
            how many segments have each section by default.
            With each um of L this number will be increased by seg_per_L_um
        """
        Cell.__init__(self, name, mechanism)
        if hoc_files:
            if isinstance(hoc_files, str):
                hoc_files = [hoc_files]
            for f in hoc_files:
                h.load_file(f)

            # add each Section or Section list from h object to self.secs dictionary
            for d in dir(h):
                try:
                    f = getattr(h, d)
                    if isinstance(f, Section):
                        self.secs[name] = f
                    elif len(f) > 0 and isinstance(f[0], Section):
                        for ff in f:
                            self.secs[ff.name()] = ff
                except TypeError:
                    continue

            for sec in self.secs.values():
                add = int(sec.L * seg_per_L_um) if seg_per_L_um is not None else 0
                sec.nseg = add_const_segs + add

