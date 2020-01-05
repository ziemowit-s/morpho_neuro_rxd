from random import randint

from cells.core.cell import Cell


class CellSpine(Cell):
    def __init__(self, name):
        Cell.__init__(self, name)
        self.heads = []
        self.necks = []

    def add_spines(self, spine_number, sections, head_nseg=2, neck_nseg=2):
        """
        Single spine is 2 x cylinder:
          * head: L=1um diam=1um
          * neck: L=0.5um diam=0.5um

        @param spine_number:
            The number of spines to create
        @param sections:
            list of sections or string defining single section name or sections names separated by space
            param 'all' - takes all sections
        @param head_nseg
        @param neck_nseg
        """
        if sections == 'all':
            sections = self.secs
        else:
            sections = self.filter_secs(sections)
        sections = sections.values()

        for i in range(spine_number):
            head = self.add_cylindric_sec(name="head[%s]" % i, diam=1, l=1, nseg=head_nseg)
            neck = self.add_cylindric_sec(name="neck[%s]" % i, diam=0.5, l=0.5, nseg=neck_nseg)
            self.heads.append(head)
            self.necks.append(neck)
            self.connect(fr='head[%s]' % i, to='neck[%s]' % i)
            self._connect_necks_rand_uniform(neck, sections)

    def _connect_necks_rand_uniform(self, necks, sections):
        """
        Connect necks list to sections list with uniform random distribution
        @param necks:
        @param sections:
        """
        max_l = int(sum([s.L for s in sections]))
        added = dict([(s.name(), []) for s in sections])

        l = 0
        r = randint(0, max_l)
        for s in sections:
            l += s.L
            if l > r:
                loc = (r - l + s.L) / s.L
                if loc in added[s.name()]:
                    break
                necks.connect(s(loc), 0.0)
                added[s.name()].append(loc)
                break