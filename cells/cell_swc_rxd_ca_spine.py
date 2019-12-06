from random import randint

import numpy as np
from cells.cell_rxd_ca import CellRxDCa
from cells.cell_swc import CellSWC


class CellSWCRxDCaSpine(CellSWC, CellRxDCa):
    def __init__(self, name, swc_file, spine_number, mechanism=None, seg_per_L_um=1.0, add_const_segs=11,
                 is_3d=False, threads=1, dx_3d_size=0.1):
        """
        @param name:
            Name of the cell
        @param swc_file:
            swc file path
        @param spine_number:
            The number of spines to create
        @param mechanism:
            Single MOD mechanism or a list of MOD mechanisms
        @param seg_per_L_um:
            how many segments per single um of L, Length.  Can be < 1
        @param add_const_segs:
            how many segments have each section by default.
            With each um of L this number will be increased by seg_per_L_um
        @param seg_per_L_um:
            how many segments per single um of L, Length.  Can be < 1. None is 0.
        @param add_const_segs:
            how many segments have each section by default.
            With each um of L this number will be increased by seg_per_L_um
        @param is_3d:
            If 3D geometry - True. Default False
        @param threads:
            How many threads to use for RxD. Default 1
        @param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.

        """
        CellSWC.__init__(self, name=name, swc_file=swc_file, mechanism=mechanism,
                         seg_per_L_um=seg_per_L_um, add_const_segs=add_const_segs)
        self.heads = []
        self.necks = []

        max_l = int(sum([s.L for s in self.secs.values()]))
        added = dict([(k, []) for k in self.secs.keys()])
        for i in range(spine_number):
            head = self.add_cylindric_sec(name="head_%s" % i, diam=1, l=1, nseg=50)
            neck = self.add_cylindric_sec(name="neck_%s" % i, diam=0.5, l=0.5, nseg=50)
            self.heads.append(head)
            self.necks.append(neck)
            self.connect(fr='head_%s' % i, to='neck_%s' % i)
            self._con_random_neck_to_neurite(neck, max_l, added)

        CellRxDCa.__init__(self, name=name, mechanism=mechanism, is_3d=is_3d, threads=threads, dx_3d_size=dx_3d_size)

    def _con_random_neck_to_neurite(self, neck, max_l, added):
        l = 0
        r = randint(0, max_l)
        for key, seg in self.secs.items():
            l += seg.L
            if l > r:
                loc = (r - l + seg.L) / seg.L
                if loc in added[key]:
                    break
                neck.connect(seg(loc), 0.0)
                added[key].append(loc)
                break