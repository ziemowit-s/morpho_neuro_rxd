import matplotlib.pyplot as plt
from neuron import h, rxd
from neuron.units import mV, ms
h.load_file('stdrun.hoc')

soma = h.Section(name='soma')
soma.diam = soma.L = 10

ecs = rxd.Extracellular(-20, -20, -20, 20, 20, 20, dx=10)
cyt = rxd.Region([soma], name='cyt', nrn_region='i')
mem = rxd.Region([soma], name='mem', geometry=rxd.membrane())

ca = rxd.Species([cyt, ecs],
                 d=1,  # with single section and nseg=1 only affects extracellular
                 name='ca',
                 charge=2,
                 initial=lambda node: 1e-3 if node.region==cyt else 0)

e = 1.60217662e-19
scale = 1e-14 / e

# rate constant is in terms of molecules/um2 ms
ca_pump = rxd.MultiCompartmentReaction(ca[cyt], ca[ecs], ca[cyt] * scale,
                                       custom_dynamics=True,
                                       membrane_flux=True,
                                       membrane=mem)

t = h.Vector().record(h._ref_t)
ca_vec = h.Vector().record(soma(0.5)._ref_cai)
ca_vec2 = h.Vector().record(ca[ecs].node_by_location(5, 0, 0)._ref_value)
v = h.Vector().record(soma(0.5)._ref_v)

h.finitialize(-65 * mV)
h.continuerun(100 * ms)

plt.subplot(2, 1, 1)
plt.plot(t, ca_vec * 1000, label='inside')
plt.plot(t, ca_vec2 * 1000, label='outside')
plt.ylabel('[Ca] (uM)')
plt.legend()
plt.subplot(2, 1, 2)
plt.plot(t, v)
plt.ylabel('v (mV)')
plt.xlabel('t (ms)')
plt.show()
