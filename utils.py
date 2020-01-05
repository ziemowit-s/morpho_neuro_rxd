import time
import numpy as np

from neuron import h
from neuron.units import ms


def get_shape_plot(variable, min_val=-70, max_val=40):
    # plot shape
    ps = h.PlotShape(True)
    ps.variable(variable)
    ps.scale(min_val, max_val)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot')
    return ps


def connect_net_stim(syn, weight, delay):
    stim = h.NetStim()
    con = h.NetCon(stim, syn)
    con.delay = delay
    con.weight[0] = weight
    return stim, con


def run_sim(runtime, stepsize=1, delay_between_steps=1, plot_shapes=()):
    """

    :param runtime:
        in ms
    :param stepsize:
        in ms
    :param delay_between_steps:
        in ms
    :param plot_shapes:
        list of plotshapes to flush
    """
    runtime = runtime * ms
    stepsize = stepsize * ms
    delay_between_steps = delay_between_steps * 1e-3  # between steps

    # run main loop
    before = time.time()  # compute time before
    for i in np.arange(0, runtime, stepsize):

        # step till i-th ms
        h.continuerun(i * ms)
        current = time.time()
        computation_time = current - before

        # adjust delay
        delay = delay_between_steps - computation_time
        if delay < 0:
            delay = 0
        time.sleep(delay)
        before = time.time()  # compute time before

        # flush shape and console log
        for ps in plot_shapes:
            ps.fastflush()
        print(round(i, 2), "ms", '// comp_time_ms:', round(computation_time * 1000, 0))

