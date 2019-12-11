from cells.cell_rxd import CellRxD
from cells.cell_spine import CellSpine


class CellRxDSpine(CellSpine, CellRxD):
    def __init__(self, name, spine_number, spine_nseg=2, mechanism=None,
                 is_3d=False, threads=1, dx_3d_size=0.1, spine_not_in_by_name=None):
        """
        @param name:
            Name of the cell
        @param spine_number:
            The number of spines to create
        @param spine_nseg:
            number of segments in the whole spine (1/2 will go to the head and 1/2 to the neck)
        @param mechanism:
            Single MOD mechanism or a list of MOD mechanisms
        @param is_3d:
            If 3D geometry - True. Default False
        @param threads:
            How many threads to use for RxD. Default 1
        @param dx_3d_size:
            If 3D geometry is True, define the size of the single compartment size.
        @param spine_not_in_by_name
            list of segments which contains name from this list will not be populated by spines.
            it can also be a single string (for a single name)

        """
        CellSpine.__init__(self, name=name, spine_number=spine_number, mechanism=mechanism, spine_nseg=spine_nseg,
                           spine_not_in_by_name=spine_not_in_by_name)

        CellRxD.__init__(self, name=name, mechanism=mechanism, is_3d=is_3d, threads=threads, dx_3d_size=dx_3d_size)