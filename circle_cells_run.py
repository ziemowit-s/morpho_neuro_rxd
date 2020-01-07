from neuron import h
from matplotlib import pyplot

from cells.core.basic_cell import BasicCell

h.load_file('stdrun.hoc')

n = 10
r = 50
cells = []
for i in range(n):
    cell = BasicCell(name=str(i))
    cell.add_sec('soma', diam=12, l=200, nseg=10)
    cell.add_sec('dend', diam=1, l=10, nseg=10)
    cell.connect_secs(source='soma', target='dend')

    theta = i * 2 * h.PI / n
    cell.set_cell_position(x=h.cos(theta) * r, y=h.sin(theta) * r, z=0)
    cell.rotate_cell_z(theta=theta)
    cells.append(cell)

ps = h.PlotShape(False)
ps.plot(pyplot)
pyplot.show()
