from client import Client
from datetime import datetime
from PyQt5.QtCore import QObject, QThreadPool, pyqtSignal
from threads import Reader, Writer


class WinSignals(QObject):
    startRead = pyqtSignal(object, dict)
    stopRead = pyqtSignal()
    exitRead = pyqtSignal()
    startWrite = pyqtSignal(object, int, int)
    stopWrite = pyqtSignal()
    exitWrite = pyqtSignal()
    finish_read = pyqtSignal(str)


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
        self.num_dw_forse = ''
        self.num_dwl_forse = ''
        self.adr_dw_forse = ''
        self.adr_dwl_forse = ''
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


class Model:
    def __init__(self):
        self.signal = WinSignals()
        self.client = Client()
        self.contr_data = DataContr()
        self.contr_setbasic = SetBasicContr()
        self.contr_setConnect = SetConnectContr()
        self.contr_setThresh = SetThresholdContr()
        self.threadpool = QThreadPool()

        self.com_port = ''
        self.available_ports = Client.port_scan(Client())
        self.initReader()
        self.flag_read = False
        self.flag_write = False

    def connectContr(self):
        try:
            self.client.connectClient(self.com_port)

        except Exception as e:
            print(str(e))

    def closeContr(self):
        try:
            self.client.closeClient()

        except Exception as e:
            print(str(e))

    def initReader(self):
        self.reader = Reader()
        self.reader.signal.read_result.connect(self.readResult)
        self.reader.signal.read_error.connect(self.readError)
        self.signal.startRead.connect(self.reader.startRead)
        self.signal.stopRead.connect(self.reader.stopRead)
        self.signal.exitRead.connect(self.reader.exitRead)
        self.threadpool.start(self.reader)

    def startRead(self, read_dict):
        self.signal.startRead.emit(self.client.client, read_dict)
        self.flag_read = True

    def stopRead(self):
        self.signal.stopRead.emit()
        self.flag_read = False

    def exitRead(self):
        self.signal.exitRead.emit()

    def readError(self, txt):
        print(txt)

    def readResult(self, tag, data):
        temp = 0
        try:
            if tag == 'basic_set':
                self.parsBasicSet(data)

            if tag == 'data':
                self.parsData(data)

            if tag == 'con_set':
                self.parsConSet(data)

            if tag == 'threshold':
                self.parsThreshold(data)

        except Exception as e:
            print('ERROR in read result in {}'.format(temp))
            print(str(e))

    def parsBasicSet(self, data):
        try:
            self.contr_setbasic.time_msg = str(datetime.now())[11:-7]
            self.contr_setbasic.rz0 = str(data[0])
            self.contr_setbasic.rst_kontrol = str(data[1])
            self.contr_setbasic.sel_d_himid = str(data[2])
            self.contr_setbasic.sel_d_speed = str(data[3])
            self.contr_setbasic.sel_dw_forse = str(data[4])
            self.contr_setbasic.sel_dwl_forse = str(data[5])
            self.contr_setbasic.num_dw_forse = str(data[6])
            self.contr_setbasic.num_dwl_forse = str(data[7])
            self.contr_setbasic.adr_dw_forse = str(data[8])
            self.contr_setbasic.adr_dwl_forse = str(data[9])
            self.contr_setbasic.adr_ms = str(data[10])
            self.contr_setbasic.per_datch = str(data[11])
            self.contr_setbasic.per_obmen = str(data[12])

            print(data)

            self.signal.finish_read.emit('basic_set')

        except Exception as e:
            print('ERROR in parsBasicSet')
            print(str(e))

    def parsData(self, data):
        try:
            self.contr_data.f_w = []
            self.contr_data.t_w = []
            self.contr_data.f_wl = []
            self.contr_data.t_wl = []
            self.contr_data.tp_wl = []
            self.contr_data.u_wl = []

            self.contr_data.time_msg = str(datetime.now())[11:-7]
            self.contr_data.adr_dev = str(data[0][0])
            self.contr_data.num_dev = str(data[0][1])
            self.contr_data.per_rstsyst = str(data[0][4])

            for i in range(0, 20, 2):
                self.contr_data.f_w.append(str(data[1][i]))
                self.contr_data.t_w.append(str(data[1][i + 1]))

            for i in range(2, 4):
                for j in range(0, 40, 4):
                    self.contr_data.f_wl.append(str(data[i][j]))
                    self.contr_data.t_wl.append(str(data[i][j + 1]))
                    self.contr_data.tp_wl.append(str(data[i][j + 2]))
                    self.contr_data.u_wl.append(str(data[i][j + 3]))

            self.contr_data.t_vlagn = str(data[4][0])
            self.contr_data.vlagn = str(data[4][1])
            self.contr_data.napr_vetr = str(data[4][2])
            self.contr_data.scor_vetr = str(data[5][0])
            self.contr_data.napr_pit = str(data[5][1])
            self.contr_data.t_ds18s20 = str(data[6][0])
            self.contr_data.status_int = str(data[6][1])

            print(data)

            self.signal.finish_read.emit('data')

        except Exception as e:
            print('ERROR in parsData')
            print(str(e))

    def parsConSet(self, data):
        try:
            self.contr_setConnect.time_msg = str(datetime.now())[11:-7]
            self.contr_setConnect.sel_type_trans_a = str(data[0][0])
            self.contr_setConnect.sel_type_trans_b = str(data[0][1])
            self.contr_setConnect.num_modem = str(data[0][2])
            self.contr_setConnect.forse_en = str(data[0][3])
            self.contr_setConnect.gprs_per_norm = str(data[0][4])

            self.contr_setConnect.adr_ip_modem_a = str(data[1][0])
            self.contr_setConnect.adr_ip_modem_b = str(data[2][0])
            self.contr_setConnect.adr_ip_psd = str(data[3][0])
            self.contr_setConnect.num_port_modem_a = str(data[4][0])
            self.contr_setConnect.num_port_modem_b = str(data[5][0])
            self.contr_setConnect.num_port_psd = str(data[6][0])
            self.contr_setConnect.num_tel_a = str(data[7][0])
            self.contr_setConnect.num_tel_b = str(data[8][0])
            self.contr_setConnect.login_modem_a = str(data[9][0])
            self.contr_setConnect.login_modem_b = str(data[10][0])
            self.contr_setConnect.parole_modem_a = str(data[11][0])
            self.contr_setConnect.parole_modem_b = str(data[12][0])
            self.contr_setConnect.apn_modem_a = str(data[13][0])
            self.contr_setConnect.apn_modem_b = str(data[14][0])

            print(data)

            self.signal.finish_read.emit('con_set')

        except Exception as e:
            print('ERROR in parsConSet')
            print(str(e))

    def parsThreshold(self, data):
        try:
            self.contr_setThresh.time_msg = str(datetime.now())[11:-7]
            self.contr_setThresh.f_w_max = []
            self.contr_setThresh.f_wl_max = []
            for i in range(10):
                self.contr_setThresh.f_w_max.append(str(data[0][i]))

            for i in range(20):
                self.contr_setThresh.f_wl_max.append(str(data[1][i]))

            print(data)

            self.signal.finish_read.emit('threshold')

        except Exception as e:
            print('ERROR in parsThreshold')
            print(str(e))

    def initWriter(self, start_adr, values):
        self.writeVal = Writer(self.client.client, start_adr, values)
        self.writeVal.signal.write_error.connect(self.writeError)
        self.writeVal.signal.write_finish.connect(self.writeFinish)
        self.threadpool.start(self.writeVal)

    def writeError(self, txt):
        print(txt)

    def writeFinish(self):
        print('Write OK')
        self.flag_write = True

    def writeValue(self, start_adr, value):
        try:
            self.start_adr = start_adr
            self.value = value

        except Exception as e:
            print(str(e))
            print('ERROR in startValue')
