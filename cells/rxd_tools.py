import abc

from neuron import rxd


class RxDTool:
    @abc.abstractmethod
    def load(self, sections, dx_3d_size):
        """
        Must be called after all secs are set.
        @param secs:
        @param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.
        """
        raise NotImplementedError


class RxDCa(RxDTool):

    def load(self, sections, dx_3d_size):
        """
        Must be called after all secs are set.
        @param secs:
        @param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.
        """

        reg = self.regs = rxd.Region(secs=sections, nrn_region='i', dx=dx_3d_size)
        self.ca = rxd.Species(regions=reg, initial=50e-6, name='ca', charge=2, d=0.6)
        self.cabuf = rxd.Species(regions=reg, initial=0.003, name='cabuf', charge=0)

        self.ca_cabuf = rxd.Species(regions=reg, initial=0, name='ca_cabuf', charge=0)
        self.reaction = rxd.Reaction(self.ca + self.cabuf, self.ca_cabuf, 100, 0.1)