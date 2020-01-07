from neuron import h


def get_netstim(start, number, interval, noise):
    stim = h.NetStim()
    stim.start = start
    stim.number = number
    stim.interval = interval
    stim.noise = noise
    return stim


def get_conn(source, target, delay, weight):
    con = h.NetCon(source, target)
    con.delay = delay
    con.weight[0] = weight
    return con
