from neuron import h

from cells.core.netcon_cell import NetConnCell
from cells.hay2011_cell import Hay2011Cell


class Ebner2019AChDACellNet(Hay2011Cell, NetConnCell):
    def __init__(self, name):
        Hay2011Cell.__init__(self, name)
        NetConnCell.__init__(self, name)

        self.params_ach = {"tau": 1000}
        self.params_da = {"tau": 1000}

        self.params_4p_syn = {
            "tau_a": 0.2,  # time constant of EPSP rise
            "tau_b": 2,  # time constant of EPSP decay
            "e": 0,  # reversal potential
            "w_pre_init": 0.5,  # pre factor initial value
            "w_post_init": 2.0,  # post factor initial value
            "s_ampa": 0.5,  # contribution of AMPAR currents
            "s_nmda": 0.5,  # contribution of NMDAR currents
            "tau_G_a": 2,  # time constant of presynaptic event G (rise)
            "tau_G_b": 50,  # time constant of presynaptic event G (decay)
            "m_G": 10,  # slope of the saturation function for G
            "A_LTD_pre": 3e-3,  # amplitude of pre-LTD
            "A_LTP_pre": 33e-4,  # amplitude of pre-LTP
            "A_LTD_post": 36e-5,  # amplitude of post-LTD
            "A_LTP_post": 2e-1,  # amplitude of post-LTP
            "tau_u_T": 10,  # time constant for filtering u to calculate T
            "theta_u_T": -60,  # voltage threshold applied to u to calculate T
            "m_T": 1.7,  # slope of the saturation function for T
            "theta_u_N": -30,  # voltage threshold applied to u to calculate N
            "tau_Z_a": 1,  # time constant of presynaptic event Z (rise)
            "tau_Z_b": 15,  # time constant of presynaptic event Z (decay)
            "m_Z": 6,  # slope of the saturation function for Z
            "tau_N_alpha": 7.5,  # time constant for calculating N-alpha
            "tau_N_beta": 30,  # time constant for calculating N-beta
            "m_N_alpha": 2,  # slope of the saturation function for N_alpha
            "m_N_beta": 10,  # slope of the saturation function for N_beta
            "theta_N_X": 0.2,  # threshold for N to calculate X
            "theta_u_C": -68,  # voltage threshold applied to u to calculate C
            "theta_C_minus": 15,  # threshold applied to C for post-LTD (P activation)
            "theta_C_plus": 35,  # threshold applied to C for post-LTP (K-alpha activation)
            "tau_K_alpha": 15,  # time constant for filtering K_alpha to calculate K_alpha_bar
            "tau_K_gamma": 20,  # time constant for filtering K_beta to calculate K_gamma
            "m_K_alpha": 1.5,  # slope of the saturation function for K_alpha
            "m_K_beta": 1.7,  # slope of the saturation function for K_beta
            "s_K_beta": 100,  # scaling factor for calculation of K_beta
        }

    def add_4p_ach_da_synapse(self, sec_names, loc):
        syns_4p = self.add_point_processes(pp_type_name="Syn4PAChDa", sec_names=sec_names, loc=loc, **self.params_4p_syn)
        syns_ach = self.add_point_processes(pp_type_name="SynACh", sec_names=sec_names, loc=loc, **self.params_ach)
        syns_da = self.add_point_processes(pp_type_name="SynDa", sec_names=sec_names, loc=loc, **self.params_da)

        # Set pointers
        for s4p, ach, da in zip(syns_4p, syns_ach, syns_da):
            h.setpointer(ach._ref_w, 'ACh', s4p)
            h.setpointer(da._ref_w, 'Da', s4p)

            h.setpointer(ach._ref_flag_D, 'flag_D_ACh', s4p)
            h.setpointer(da._ref_flag_D, 'flag_D_Da', s4p)

            h.setpointer(ach._ref_last_max_w, 'last_max_w_ACh', s4p)
            h.setpointer(da._ref_last_max_w, 'last_max_w_Da', s4p)
