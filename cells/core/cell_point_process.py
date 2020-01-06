from neuron import h

from cells.core.cell import Cell


class CellPointProcess(Cell):
    def __init__(self, name):
        """
        :param name:
            Name of the cell
        """
        Cell.__init__(self, name)
        self.stimulations = {}
        self.connections = {}

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
            stim, con = self._connect_net_stim(syn, weight=weight, delay=delay, start=start, number=number, interval=interval, noise=noise)
            self.stimulations[name] = stim
            self.connections[name] = con

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