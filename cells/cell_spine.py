from random import randint

import numpy as np

from cells.cell import Cell
from cells.cell_rxd_ca import CellRxDCa
from cells.cell_swc import CellSWC


class CellSpine(Cell):
    def __init__(self, name, spine_number, mechanism=None, spine_nseg=2):
        """
        Single spine is 2 x cylinder:
          * head: L=1um diam=1um
          * neck: L=0.5um diam=0.5um

        @param name:
            Name of the cell
        @param spine_number:
            The number of spines to create
        @param mechanism:
            Single MOD mechanism or a list of MOD mechanisms
        @param spine_nseg:
            number of segments in the whole spine (1/2 will go to the head and 1/2 to the neck)
        """
        Cell.__init__(self, name, mechanism)

        self.heads = []
        self.necks = []
        max_l = int(sum([s.L for s in self.secs.values()]))
        added = dict([(k, []) for k in self.secs.keys()])
        for i in range(spine_number):
            head = self.add_cylindric_sec(name="head_%s" % i, diam=1, l=1, nseg=int(spine_nseg/2))
            neck = self.add_cylindric_sec(name="neck_%s" % i, diam=0.5, l=0.5, nseg=int(spine_nseg/2))
            self.heads.append(head)
            self.necks.append(neck)
            self.connect(fr='head_%s' % i, to='neck_%s' % i)
            self._con_random_neck_to_neurite(neck, max_l, added)

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