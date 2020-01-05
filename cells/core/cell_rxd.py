from neuron.rxd import rxd

from cells.core.cell import Cell
from cells.core.rxd_tools import RxDTool


class CellRxD(Cell):
    def __init__(self, name):
        """
        :param name:
            Name of the cell
        """
        Cell.__init__(self, name)
        self.rxds = {}

    def add_cylindric_sec(self, name, diam=None, l=None, nseg=1, mechanisms='all'):
        if hasattr(self, '_is_rxd_set') and self._is_rxd_set:
            raise MemoryError("RxD has been called earlier, after which you can't change morphology")

        return super().add_cylindric_sec(name, diam, l, nseg, mechanisms)

    def add_rxd(self, rxd_obj: RxDTool, sections, is_3d=False, threads=1, dx_3d_size=None):
        """
        :param is_3d:
        :param threads:
        :param dx_3d_size:
        :param sections:
            list of sections or string defining single section name or sections names separated by space
            param 'all' - takes all sections
        """
        self.rxds[rxd_obj.__class__.__name__] = rxd_obj

        if sections is 'all':
            sections = self.secs.values()
        else:
            sections = self.filter_secs(left=sections).values()

        if is_3d:
            rxd.set_solve_type(sections, dimension=3)
        rxd.nthread(threads)

        rxd_obj.load(sections, dx_3d_size=dx_3d_size, rxds=self.rxds)


