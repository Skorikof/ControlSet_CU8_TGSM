class Settings:
    def __init__(self):
        self.type_connect = ''
        self.port = ''
        self.host = 'localhost'
        self.available_ports = []
        self.flag_connect = False
        self.flag_read = False
        self.flag_write = False
        self.read_dict = {'basic_set': False, 'data': False, 'threshold': False, 'con_set': False}


class DataContr:
    def __init__(self):
        self.time_msg = ''
        self.adr_dev = ''
        self.num_dev = ''
        self.per_rstsyst = ''
        self.f_w = []
        self.t_w = []
        self.f_wl = []
        self.t_wl = []
        self.tp_wl = []
        self.u_wl = []
        self.t_vlagn = ''
        self.vlagn = ''
        self.napr_vetr = ''
        self.scor_vetr = ''
        self.napr_pit = ''
        self.t_ds18s20 = ''
        self.status_int = ''


class SetBasicContr:
    def __init__(self):
        self.time_msg = ''
        self.rz0 = ''
        self.rst_kontrol = ''
        self.sel_d_himid = ''
        self.sel_d_speed = ''
        self.sel_dw_forse = ''
        self.sel_dwl_forse = ''
        self.num_dw_forse = 0
        self.num_dwl_forse = 0
        self.adr_dw_forse = 0
        self.adr_dwl_forse = 0
        self.adr_ms = ''
        self.per_datch = ''
        self.per_obmen = ''


class SetConnectContr:
    def __init__(self):
        self.time_msg = ''
        self.sel_type_trans_a = ''
        self.sel_type_trans_b = ''
        self.num_modem = ''
        self.forse_en = ''
        self.gprs_per_norm = ''
        self.adr_ip_modem_a = ''
        self.adr_ip_modem_b = ''
        self.adr_ip_psd = ''
        self.num_port_modem_a = ''
        self.num_port_modem_b = ''
        self.num_port_psd = ''
        self.num_tel_a = ''
        self.num_tel_b = ''
        self.login_modem_a = ''
        self.login_modem_b = ''
        self.parole_modem_a = ''
        self.parole_modem_b = ''
        self.apn_modem_a = ''
        self.apn_modem_b = ''


class SetThresholdContr:
    def __init__(self):
        self.time_msg = ''
        self.f_w_max = []
        self.f_wl_max = []
