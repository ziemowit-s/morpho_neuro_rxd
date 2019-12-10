from neuron import h
from nrn import Section

from cells.cell import Cell


class CellHOC(Cell):
    def __init__(self, name, mechanism=None, hoc_files=None):
        """
        @param name:
            Name of the cell
        @param mechanism:
            Single MOD mechanism or a list of MOD mechanisms
        @param hoc_files:
            list of string paths to hoc files or single string of single hoc file
        """
        Cell.__init__(self, name, mechanism)
        if hoc_files:
            if isinstance(hoc_files, str):
                hoc_files = [hoc_files]
            for f in hoc_files:
                h.load_file(f)

            for d in dir(h):
                try:
                    f = getattr(h, d)
                    if len(f) > 0 and isinstance(f[0], Section):
                        name = f[0].name().split('[')[0]
                        self.secs[name] = f
                except TypeError:
                    continue

            print('done')


