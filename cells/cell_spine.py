from random import randint

from cells.cell import Cell


class CellSpine(Cell):
    def __init__(self, name, mechanism=None):
        """
        @param name:
            Name of the cell
        @param mechanism:
            Single MOD mechanism or a list of MOD mechanisms
        """
        Cell.__init__(self, name, mechanism)
        self.heads = []
        self.necks = []

    def add_spines(self, spine_number, head_nseg=2, neck_nseg=2, sections=None):
        """
        Single spine is 2 x cylinder:
          * head: L=1um diam=1um
          * neck: L=0.5um diam=0.5um

        @param spine_number:
            The number of spines to create
        @param head_nseg
        @param neck_nseg
        @param sections:
            list of sections or string defining section name
        """
        if isinstance(sections, str):
            sections = [sections]
        sections = self.filter_sections(sections)

        for i in range(spine_number):
            head = self.add_cylindric_sec(name="head_%s" % i, diam=1, l=1, nseg=head_nseg)
            neck = self.add_cylindric_sec(name="neck_%s" % i, diam=0.5, l=0.5, nseg=neck_nseg)
            self.heads.append(head)
            self.necks.append(neck)
            self.connect(fr='head_%s' % i, to='neck_%s' % i)
            self._con_random_neck_to_neurite(neck, sections)

    def _con_random_neck_to_neurite(self, neck, sections):
        max_l = int(sum([v.L for k, v in sections]))
        added = dict([(k, []) for k, v in sections])

        l = 0
        r = randint(0, max_l)
        for key, seg in sections:
            l += seg.L
            if l > r:
                loc = (r - l + seg.L) / seg.L
                if loc in added[key]:
                    break
                neck.connect(seg(loc), 0.0)
                added[key].append(loc)
                break