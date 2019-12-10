from random import randint

import numpy as np

from cells.cell import Cell
from cells.cell_rxd_ca import CellRxDCa
from cells.cell_swc import CellSWC


class CellSpine(Cell):
    def __init__(self, name, spine_number, mechanism=None, spine_nseg=2, spine_not_in_by_name=None):
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
        @param spine_not_in_by_name
            list of segments which contains name from this list will not be populated by spines.
            it can also be a single string (for a single name)
        """
        Cell.__init__(self, name, mechanism)
        if isinstance(spine_not_in_by_name, str):
            spine_not_in_by_name = [spine_not_in_by_name]
        self.spine_not_in_by_name = spine_not_in_by_name
        self.spine_number = spine_number
        self.spine_nseg = spine_nseg
        self.heads = []
        self.necks = []

    def add_spines(self):
        nseg = int(self.spine_nseg/2)
        for i in range(self.spine_number):
            head = self.add_cylindric_sec(name="head_%s" % i, diam=1, l=1, nseg=nseg)
            neck = self.add_cylindric_sec(name="neck_%s" % i, diam=0.5, l=0.5, nseg=nseg)
            self.heads.append(head)
            self.necks.append(neck)
            self.connect(fr='head_%s' % i, to='neck_%s' % i)
            self._con_random_neck_to_neurite(neck)

    def _con_random_neck_to_neurite(self, neck):
        filtered_secs = []
        for k, v in self.secs.items():
            is_add = True
            for f in self.spine_not_in_by_name:
                if f.lower() in k.lower():
                    is_add = False
                    break
            if is_add:
                filtered_secs.append((k, v))

        max_l = int(sum([v.L for k, v in filtered_secs]))
        added = dict([(k, []) for k, v in filtered_secs])

        l = 0
        r = randint(0, max_l)
        for key, seg in filtered_secs:
            l += seg.L
            if l > r:
                loc = (r - l + seg.L) / seg.L
                if loc in added[key]:
                    break
                neck.connect(seg(loc), 0.0)
                added[key].append(loc)
                break