import time

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


def run_sim(runtime, start_from=0, stepsize=None, delay_between_steps=1, warmup=0, dt=0.025, plot_shapes=()):
    """

    :param runtime:
        in ms
    :param start_from:
        in ms
    :param stepsize:
        in ms. Default None -> stepsize is the size of runtime
    :param delay_between_steps:
        in ms
    :param warmup:
        in ms, for warmup with dt=10*ms
    :param plot_shapes:
        list of plotshapes to flush
    """
    if stepsize is None:
        stepsize = runtime
    if warmup > 0:
        h.dt = 10
        h.continuerun(warmup * ms)
        h.dt = dt

    delay_between_steps = delay_between_steps * 1e-3  # between steps

    # prepare run array
    max_runtime = runtime+warmup+start_from
    run_array = [i for i in range(0+warmup+start_from+stepsize, max_runtime+1, stepsize)]
    left_run = max_runtime - max(run_array)
    if left_run > 0:
        run_array = run_array + [max_runtime]

    # run main loop
    before = time.time()  # compute time before
    for r in run_array:

        # step till i-th ms
        h.continuerun(r * ms)
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
        print(stepsize, "ms", '// comp_time_ms:', round(computation_time * 1000, 0))

