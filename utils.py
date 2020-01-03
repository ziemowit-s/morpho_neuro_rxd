from neuron import h


def plot_cai():
    # plot shape
    ps = h.PlotShape(True)
    ps.variable('cai')
    ps.scale(0, 0.01)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot CAI')
    return ps


def plot_ica():
    # plot shape
    ps = h.PlotShape(True)
    ps.variable('ica')
    ps.scale(-10, 10)
    ps.show(0)
    h.fast_flush_list.append(ps)
    ps.exec_menu('Shape Plot ICA')
    return ps

