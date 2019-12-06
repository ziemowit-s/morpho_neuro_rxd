import abc

from neuron.rxd import rxd

from cells.cell import Cell


class CellRxD(Cell):
    def __init__(self, name, mechanism=None, is_3d=False, threads=1, dx_3d_size=0.1):
        """
        @param name:
            Name of the cell
        @param mechanism:
            Single MOD mechanism or a list of MOD mechanisms
        @param is_3d:
            If 3D geometry - True. Default False
        @param threads:
            How many threads to use for RxD. Default 1
        @param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.
        """
        Cell.__init__(self, name, mechanism)

        self.regs = {}
        self.is_3d = is_3d
        self.threads = threads
        self._is_rxd_set = False
        self._dx_3d_size = dx_3d_size

    def add_cylindric_sec(self, name, diam=None, l=None, nseg=1):
        if self._is_rxd_set:
            raise MemoryError("RxD has been called earlier, after which you can't change morphology")
        super().add_cylindric_sec(name, diam, l, nseg)

    def add_rxd(self):
        if self._is_rxd_set:
            raise MemoryError("RxD has been called earlier, it can be called only once, after all morphology is set")
        self._is_rxd_set = True

        if self.is_3d:
            rxd.set_solve_type(self.secs.values(), dimension=3)
        rxd.nthread(self.threads)

        self._add_rxd(self.secs, dx_3d_size=self._dx_3d_size)

    @abc.abstractmethod
    def _add_rxd(self, regs, dx_3d_size):
        raise NotImplementedError()


