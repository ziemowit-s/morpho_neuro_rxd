from os import path

from neuron import h

h.load_file('stdlib.hoc')
h.load_file('import3d.hoc')


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

    def load_morpho(self, filepath, seg_per_L_um=1.0, add_const_segs=11):
        """
        @param filepath:
            swc file path
        @param seg_per_L_um:
            how many segments per single um of L, Length.  Can be < 1. None is 0.
        @param add_const_segs:
            how many segments have each section by default.
            With each um of L this number will be increased by seg_per_L_um
        """
        if not path.exists(filepath):
            raise FileNotFoundError()

        # SWC
        fileformat = filepath.split('.')[-1]
        if fileformat == 'swc':
            morpho = h.Import3d_SWC_read()
        # Neurolucida
        elif fileformat == 'asc':
            morpho = h.Import3d_Neurolucida3()
        else:
            raise Exception('file format `%s` not recognized' % filepath)

        morpho.input(filepath)
        h.Import3d_GUI(morpho, 0)
        i3d = h.Import3d_GUI(morpho, 0)
        i3d.instantiate(self)

        # add all SWC sections to self.secs; self.all is defined by SWC import
        new_secs = {}
        for sec in self.all:
            name = sec.name().split('.')[-1]  # eg. name="dend[19]"
            new_secs[name] = sec

        # change segment number based on seg_per_L_um and add_const_segs
        for sec in new_secs.values():
            add = int(sec.L * seg_per_L_um) if seg_per_L_um is not None else 0
            sec.nseg = add_const_segs + add

        self.secs.update(new_secs)
        del self.all

    def set_position(self, x, y, z):
        h.define_shape()
        for sec in self.secs.values():
            for i in range(sec.n3d()):
                sec.pt3dchange(i,
                               x - sec.x3d(i),
                               y - sec.y3d(i),
                               z - sec.z3d(i),
                              sec.diam3d(i))
        
    def rotate_z(self, theta):
        h.define_shape()
        """Rotate the cell about the Z axis."""
        for sec in self.secs.values():
            for i in range(sec.n3d()):
                x = sec.x3d(i)
                y = sec.y3d(i)
                c = h.cos(theta)
                s = h.sin(theta)
                xprime = x * c - y * s
                yprime = x * s + y * c
                sec.pt3dchange(i, xprime, yprime, sec.z3d(i), sec.diam3d(i))

    @staticmethod
    def _is_array_name(name):
        return "[" in name

    def __repr__(self):
        return "Cell[{}]".format(self._name)
