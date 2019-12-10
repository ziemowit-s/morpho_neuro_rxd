from cells.cell_hoc import CellHOC
from cells.cell_rxd_ca import CellRxDCa
from cells.cell_spine import CellSpine
from cells.cell_swc import CellSWC


class CellHOCRxDCaSpine(CellHOC, CellSpine, CellRxDCa):
    def __init__(self, name, spine_number, spine_nseg=2, hoc_files=None, mechanism=None, seg_per_L_um=1.0, add_const_segs=11,
                 is_3d=False, threads=1, dx_3d_size=0.1):
        """
        @param name:
            Name of the cell
        @param swc_file:
            swc file path
        @param spine_number:
            The number of spines to create
        @param spine_nseg:
            number of segments in the whole spine (1/2 will go to the head and 1/2 to the neck)
        @param hoc_files:
            list of string paths to hoc files or single string of single hoc file
        @param mechanism:
            Single MOD mechanism or a list of MOD mechanisms
        @param seg_per_L_um:
            how many segments per single um of L, Length.  Can be < 1
        @param add_const_segs:
            how many segments have each section by default.
            With each um of L this number will be increased by seg_per_L_um
        @param seg_per_L_um:
            how many segments per single um of L, Length.  Can be < 1. None is 0.
        @param add_const_segs:
            how many segments have each section by default.
            With each um of L this number will be increased by seg_per_L_um
        @param is_3d:
            If 3D geometry - True. Default False
        @param threads:
            How many threads to use for RxD. Default 1
        @param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.

        """
        CellHOC.__init__(self, name=name, hoc_files=hoc_files, mechanism=mechanism)

        CellSpine.__init__(self, name=name, spine_number=spine_number, mechanism=mechanism, spine_nseg=spine_nseg)

        CellRxDCa.__init__(self, name=name, mechanism=mechanism, is_3d=is_3d, threads=threads, dx_3d_size=dx_3d_size)