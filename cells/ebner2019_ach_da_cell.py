from neuron import h

from cells.ebner2019_cell import Ebner2019Cell
from cells.core.conn_cell import ConnCell


class Ebner2019AChDACell(Ebner2019Cell, ConnCell):
    def __init__(self, name):
        Ebner2019Cell.__init__(self, name)
        ConnCell.__init__(self, name)
        self.params_ach = {"tau": 1000}
        self.params_da = {"tau": 1000}

    def add_4p_ach_da_synapse(self, sec_names, loc):
        self.add_4p_synapse(sec_names=sec_names, loc=loc)
        syns_4p = self.add_pprocs(name="Syn4PAChDa", sec_names=sec_names, loc=loc, **self.params_4p_syn)
        syns_ach = self.add_pprocs(name="SynACh", sec_names=sec_names, loc=loc, **self.params_ach)
        syns_da = self.add_pprocs(name="SynDa", sec_names=sec_names, loc=loc, **self.params_da)

        # Set pointers
        for s4p, ach, da in zip(syns_4p, syns_ach, syns_da):
            h.setpointer(ach._ref_w, 'ACh', s4p)
            h.setpointer(da._ref_w, 'Da', s4p)

            h.setpointer(ach._ref_flag_D, 'flag_D_ACh', s4p)
            h.setpointer(da._ref_flag_D, 'flag_D_Da', s4p)

            h.setpointer(ach._ref_last_max_w, 'last_max_w_ACh', s4p)
            h.setpointer(da._ref_last_max_w, 'last_max_w_Da', s4p)
