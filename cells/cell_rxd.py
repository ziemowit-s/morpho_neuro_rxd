import abc

from neuron.rxd import rxd

from cells.cell import Cell


class CellRxD(Cell):
    def __init__(self, name, mechanism=None, is_3d=False, threads=1):
        Cell.__init__(self, name, mechanism)

        self.regs = {}
        self.is_3d = is_3d
        self.threads = threads
        self._is_rxd_set = False

    def add_sec(self, name, diam=None, l=None, nseg=1):
        if self._is_rxd_set:
            raise MemoryError("RxD has been called earlier, after which you can't change morphology")
        super().add_sec(name, diam, l, nseg)

    def add_rxd(self):
        if self._is_rxd_set:
            raise MemoryError("RxD has been called earlier, it can be called only once, after all morphology is set")
        self._is_rxd_set = True

        if self.is_3d:
            rxd.set_solve_type(self.secs.values(), dimension=3)
        rxd.nthread(self.threads)

        self._add_rxd(self.secs)

    @abc.abstractmethod
    def _add_rxd(self, regs):
        raise NotImplementedError()


