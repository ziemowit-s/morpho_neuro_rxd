from neuron import h
from cells.cell_hay2011 import CellHay2011
from cells.core.cell_point_process import CellPointProcess


class CellEbner2019(CellHay2011, CellPointProcess):
    def __init__(self, name):
        CellHay2011.__init__(self, name)
        CellPointProcess.__init__(self, name)
        self.syns_4p = {}

    def add_4p_synapse(self, sections, loc):
        secs = self.filter_secs(left=sections)
        for name, s in secs.items():
            syn = h.Syn4P(s(loc))
            self.syns_4p[name] = syn

            syn.tau_a = 0.2  # time constant of EPSP rise
            syn.tau_b = 2  # time constant of EPSP decay
            syn.e = 0  # reversal potential
            syn.w_pre_init = 0.5  # pre factor initial value
            syn.w_post_init = 2.0  # post factor initial value
            syn.s_ampa = 0.5  # contribution of AMPAR currents
            syn.s_nmda = 0.5  # contribution of NMDAR currents
            syn.tau_G_a = 2  # time constant of presynaptic event G (rise)
            syn.tau_G_b = 50  # time constant of presynaptic event G (decay)
            syn.m_G = 10  # slope of the saturation function for G
            syn.A_LTD_pre = 3e-3  # amplitude of pre-LTD
            syn.A_LTP_pre = 33e-4  # amplitude of pre-LTP
            syn.A_LTD_post = 36e-5  # amplitude of post-LTD
            syn.A_LTP_post = 2e-1  # amplitude of post-LTP
            syn.tau_u_T = 10  # time constant for filtering u to calculate T
            syn.theta_u_T = -60  # voltage threshold applied to u to calculate T
            syn.m_T = 1.7  # slope of the saturation function for T
            syn.theta_u_N = -30  # voltage threshold applied to u to calculate N
            syn.tau_Z_a = 1  # time constant of presynaptic event Z (rise)
            syn.tau_Z_b = 15  # time constant of presynaptic event Z (decay)
            syn.m_Z = 6  # slope of the saturation function for Z
            syn.tau_N_alpha = 7.5  # time constant for calculating N-alpha
            syn.tau_N_beta = 30  # time constant for calculating N-beta
            syn.m_N_alpha = 2  # slope of the saturation function for N_alpha
            syn.m_N_beta = 10  # slope of the saturation function for N_beta
            syn.theta_N_X = 0.2  # threshold for N to calculate X
            syn.theta_u_C = -68  # voltage threshold applied to u to calculate C
            syn.theta_C_minus = 15  # threshold applied to C for post-LTD (P activation)
            syn.theta_C_plus = 35  # threshold applied to C for post-LTP (K-alpha activation)
            syn.tau_K_alpha = 15  # time constant for filtering K_alpha to calculate K_alpha_bar
            syn.tau_K_gamma = 20  # time constant for filtering K_beta to calculate K_gamma
            syn.m_K_alpha = 1.5  # slope of the saturation function for K_alpha
            syn.m_K_beta = 1.7  # slope of the saturation function for K_beta
            syn.s_K_beta = 100  # scaling factor for calculation of K_beta