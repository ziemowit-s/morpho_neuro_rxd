from neuron import h

from cells.core.cell import Cell


class CellPointProcess(Cell):
    def __init__(self, name):
        """
        :param name:
            Name of the cell
        """
        Cell.__init__(self, name)
        self.stims = {}
        self.conns = {}
        self.syn_num = 0

    def filter_syns(self, synapse_type, synapses, as_list=False):
        return self._filter_obj_dict(synapse_type, synapses, as_list)

    def add_net_stim(self, synapse_type, weight, start, delay=0, number=1, interval=1, noise=0, synapses=None):
        """
        :param synapse_type:
        :param weight:
            netcon param
        :param delay:
            netcon param
        :param start:
            netstim param
        :param number:
            netstim param
        :param interval:
            netstim param
        :param noise:
            netstim param
        :param synapses:
        :return:
        """
        syns = self._filter_obj_dict(synapse_type, synapses)

        for name, syn in syns.items():
            name = "%s_%s[%s]" % (synapse_type, name, self.syn_num)
            self.syn_num += 1

            stim, con = self._connect_net_stim(syn, weight=weight, delay=delay, start=start, number=number, interval=interval, noise=noise)
            self.stims[name] = stim
            self.conns[name] = con

    @staticmethod
    def _connect_net_stim(syn, weight, delay, start, number, interval, noise):
        stim = h.NetStim()
        stim.start = start
        stim.number = number
        stim.interval = interval
        stim.noise = noise

        con = h.NetCon(stim, syn)
        con.delay = delay
        con.weight[0] = weight

        return stim, con