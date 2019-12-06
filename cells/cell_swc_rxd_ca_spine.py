from cells.cell_rxd_ca import CellRxDCa
from cells.cell_swc import CellSWC


class CellSWCRxDCaSpine(CellRxDCa, CellSWC):
    def __init__(self, name, swc_file, spine_number, mechanism=None, is_3d=False, threads=1):
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
        """
        CellRxDCa.__init__(self, name, mechanism, is_3d, threads)
        CellSWC.__init__(self, name, swc_file, mechanism)
        for i in range(spine_number):
            self.add_cylindric_sec(name="head_%s" % i, diam=1, l=1, nseg=50)
            self.add_cylindric_sec(name="neck_%s" % i, diam=0.5, l=0.5, nseg=50)
            self.connect(fr='head_%s' % i, to='neck_%s' % i)

        self.add_rxd()


