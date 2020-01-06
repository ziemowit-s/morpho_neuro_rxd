from neuron import h

from cells.cell_hay2011 import CellHay2011
from cells.core.cell_point_process import CellPointProcess


class CellEbner2019AChDA(CellHay2011, CellPointProcess):
    def __init__(self, name):
        CellHay2011.__init__(self, name)
        CellPointProcess.__init__(self, name)
        self.syns_4p = {}
        self.syns_ach = {}
        self.syns_da = {}

    def add_4p_ach_da_synapse(self, sections, loc):
        secs = self.filter_secs(left=sections)
        for name, s in secs.items():
            # Add 4p syn
            syn_4p = self._make_4p_syn(s, loc)
            self.syns_4p[name] = syn_4p

            # Add ACh syn
            syn_ach = h.SynACh(s(loc))
            self.syns_ach[name] = syn_ach
            syn_ach.tau = 2000

            # Add DA syn
            syn_da = h.SynDa(s(loc))
            self.syns_da[name] = syn_da
            syn_da.tau = 2000

            # set pointer
            #
            # Example in HOC:
            # objref syn
            # somedendrite syn = new GradSyn(0.8)
            # setpointer syn.cp, precell.bouton.cai(0.5)
            #
            # Python Example:
            # h.setpointer(sec['hSec'](.5)._ref_ecl, 'e', sec['synMechs'][0]['hSyn'])
            h.setpointer(syn_ach._ref_g, 'ACh', syn_4p)
            h.setpointer(syn_da._ref_g, 'Da', syn_4p)

            h.setpointer(syn_ach._ref_tau, 'tau_ACh', syn_4p)
            h.setpointer(syn_da._ref_tau, 'tau_Da', syn_4p)

    def _make_4p_syn(self, sec, loc):
        syn_4p = h.Syn4PAChDa(sec(loc))
        syn_4p.tau_a = 0.2  # time constant of EPSP rise
        syn_4p.tau_b = 2  # time constant of EPSP decay
        syn_4p.e = 0  # reversal potential
        syn_4p.w_pre_init = 0.5  # pre factor initial value
        syn_4p.w_post_init = 2.0  # post factor initial value
        syn_4p.s_ampa = 0.5  # contribution of AMPAR currents
        syn_4p.s_nmda = 0.5  # contribution of NMDAR currents
        syn_4p.tau_G_a = 2  # time constant of presynaptic event G (rise)
        syn_4p.tau_G_b = 50  # time constant of presynaptic event G (decay)
        syn_4p.m_G = 10  # slope of the saturation function for G
        syn_4p.A_LTD_pre = 3e-3  # amplitude of pre-LTD
        syn_4p.A_LTP_pre = 33e-4  # amplitude of pre-LTP
        syn_4p.A_LTD_post = 36e-5  # amplitude of post-LTD
        syn_4p.A_LTP_post = 2e-1  # amplitude of post-LTP
        syn_4p.tau_u_T = 10  # time constant for filtering u to calculate T
        syn_4p.theta_u_T = -60  # voltage threshold applied to u to calculate T
        syn_4p.m_T = 1.7  # slope of the saturation function for T
        syn_4p.theta_u_N = -30  # voltage threshold applied to u to calculate N
        syn_4p.tau_Z_a = 1  # time constant of presynaptic event Z (rise)
        syn_4p.tau_Z_b = 15  # time constant of presynaptic event Z (decay)
        syn_4p.m_Z = 6  # slope of the saturation function for Z
        syn_4p.tau_N_alpha = 7.5  # time constant for calculating N-alpha
        syn_4p.tau_N_beta = 30  # time constant for calculating N-beta
        syn_4p.m_N_alpha = 2  # slope of the saturation function for N_alpha
        syn_4p.m_N_beta = 10  # slope of the saturation function for N_beta
        syn_4p.theta_N_X = 0.2  # threshold for N to calculate X
        syn_4p.theta_u_C = -68  # voltage threshold applied to u to calculate C
        syn_4p.theta_C_minus = 15  # threshold applied to C for post-LTD (P activation)
        syn_4p.theta_C_plus = 35  # threshold applied to C for post-LTP (K-alpha activation)
        syn_4p.tau_K_alpha = 15  # time constant for filtering K_alpha to calculate K_alpha_bar
        syn_4p.tau_K_gamma = 20  # time constant for filtering K_beta to calculate K_gamma
        syn_4p.m_K_alpha = 1.5  # slope of the saturation function for K_alpha
        syn_4p.m_K_beta = 1.7  # slope of the saturation function for K_beta
        syn_4p.s_K_beta = 100  # scaling factor for calculation of K_beta
        return syn_4p