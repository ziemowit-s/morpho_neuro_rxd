from neuron import h


class Cell:
    def __init__(self, name, mechanism=None):
        """
        @param name:
            Name of the cell
        @param mechanism:
            Single MOD mechanism or a list of MOD mechanisms
        """
        if not hasattr(self, '_core_cell_builded'):
            self._name = name
            self.secs = {}
            if isinstance(mechanism, list):
                self.mechanisms = mechanism
            else:
                self.mechanisms = []
            self._core_cell_builded = True

    def add_cylindric_sec(self, name, diam=None, l=None, nseg=1):
        sec = h.Section(name=name, cell=self)
        sec.L = l
        sec.diam = diam
        sec.nseg = nseg

        for m in self.mechanisms:
            sec.insert(m)
        self.secs[name] = sec
        return sec

    def connect(self, fr, to, to_loc=1.0, fr_loc=0.0):
        """default: fr(0.0) -> to(1.0)"""
        fr_loc = float(fr_loc)
        to_loc = float(to_loc)
        fr = self.secs[fr]
        to = self.secs[to]
        fr.connect(to(to_loc), fr_loc)

    def __repr__(self):
        return "Cell[{}]".format(self._name)