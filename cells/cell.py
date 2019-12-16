from neuron import h


class Cell:
    def __init__(self, name):
        """
        @param name:
            Name of the cell
        """
        # if Cell (named core_cell) have been built before on the stack of super() objects
        if not hasattr(self, '_core_cell_builded'):
            self._name = name
            self.mechanisms = []
            self.secs = {}
            self._core_cell_builded = True

    def add_mechanism(self, mechanism=None):
        """
        @param mechanism:
            Single MOD mechanism or a list of MOD mechanisms
        """
        if not isinstance(mechanism, list):
            mechanism = [mechanism]
        self.mechanisms.extend(mechanism)

    def add_cylindric_sec(self, name, diam=None, l=None, nseg=1, mechanisms='all'):
        """

        @param name:
        @param diam:
        @param l:
        @param nseg:
        @param mechanisms:
            string of mechanisms or list of strings of selected mechanisms.
        @return:
        """
        sec = h.Section(name=name, cell=self)
        sec.L = l
        sec.diam = diam
        sec.nseg = nseg
        if isinstance(mechanisms, str):
            mechanisms = [mechanisms]

        for m in self.mechanisms:
            if 'all' in mechanisms or m in mechanisms:
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

    def filter_secs(self, left):
        """
        @param left:
            list of sections or string defining section name. Only sections specified here will remain
        """
        result = []
        for k, v in self.secs.items():
            for s in left:
                sec_name = ''.join(k.split("[")[:-1])
                if s.lower() == sec_name.lower():
                    result.append(v)
                    break
        return result

    def __repr__(self):
        return "Cell[{}]".format(self._name)