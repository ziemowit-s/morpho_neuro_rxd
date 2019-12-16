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
        fr = self.filter_secs(fr)[0]
        to = self.filter_secs(to)[0]
        fr.connect(to(to_loc), fr_loc)

    def filter_secs(self, left):
        """
        @param left:
            list of sections or string defining single section name or sections names separated by space
        """
        if isinstance(left, str):
            left = left.split(' ')
        result = []
        for k, v in self.secs.items():
            if 'head' in k:
                pass
            for s in left:
                # section names (especially created by NEURON or hoc) frequently have array-like string name
                # eg. soma[0]. User can specify exact name eg. dend[12]
                # or group of names eg. dend (if apply to array-like naming convention)
                # or single name without array-like brackets (mostly this case works for user-defined compartments)
                if self._is_array_name(k) and not self._is_array_name(s):
                    sec_name = ''.join(k.split("[")[:-1])
                else:
                    sec_name = k
                if s.lower() == sec_name.lower():
                    result.append(v)
                    break
        if len(result) == 0:
            raise LookupError("Cannot found sections:", left)
        return result

    @staticmethod
    def _is_array_name(name):
        return "[" in name

    def __repr__(self):
        return "Cell[{}]".format(self._name)
