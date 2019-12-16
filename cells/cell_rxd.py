import abc

from neuron.rxd import rxd

from cells.cell import Cell


class CellRxD(Cell):
    def __init__(self, name):
        """
        @param name:
            Name of the cell
        """
        Cell.__init__(self, name)
        self.regs = {}
        self._is_rxd_set = False

    def add_cylindric_sec(self, name, diam=None, l=None, nseg=1, mechanisms='all'):
        if hasattr(self, '_is_rxd_set') and self._is_rxd_set:
            raise MemoryError("RxD has been called earlier, after which you can't change morphology")

        return super().add_cylindric_sec(name, diam, l, nseg, mechanisms)

    def add_rxd(self, is_3d=False, threads=1, dx_3d_size=None, sections=None):
        """
        @param is_3d:
        @param threads:
        @param dx_3d_size:
        @param sections:
            list of sections or string defining section name
        """
        if hasattr(self, '_is_rxd_set') and self._is_rxd_set:
            raise MemoryError("RxD has been called earlier, it can be called only once, after all morphology is set")
        self._is_rxd_set = True

        if sections is None:
            sections = self.secs.values()
        else:
            sections = self.filter_secs(left=sections)

        if is_3d:
            rxd.set_solve_type(sections, dimension=3)
        rxd.nthread(threads)

        self._add_rxd(sections, dx_3d_size=dx_3d_size)

    @abc.abstractmethod
    def _add_rxd(self, sections, dx_3d_size):
        raise NotImplementedError()


