import time

from client import Client
from struct import pack, unpack
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
        self.adr_dev = 0
        self.num_dev = 0
        self.per_rstsyst = 0
        self.f_w = []
        self.t_w = []
        self.f_wl = []
        self.t_wl = []
        self.tp_wl = []
        self.u_wl = []
        self.t_vlagn = 0
        self.vlagn = 0
        self.napr_vetr = 0
        self.scor_vetr = 0.0
        self.napr_pit = 0.0
        self.t_ds18s20 = 0
        self.status_int = 0


class SetBasicContr:
    def __init__(self):
        self.time_msg = ''
        self.rz0 = 0
        self.rst_kontrol = 0
        self.sel_d_himid = 0
        self.sel_d_speed = 0
        self.sel_dw_forse = 0
        self.sel_dwl_forse = 0
        self.num_dw_forse = 0
        self.num_dwl_forse = 0
        self.adr_dw_forse = 0
        self.adr_dwl_forse = 0
        self.adr_ms = 0
        self.per_datch = 0
        self.per_obmen = 0


class SetConnectContr:
    def __init__(self):
        self.time_msg = ''
        self.sel_type_trans_a = 0
        self.sel_type_trans_b = 0
        self.num_modem = 0
        self.adr_ip_modem_a = 0
        self.adr_ip_modem_b = 0
        self.adr_ip_psd = 0
        self.num_port_modem_a = 0
        self.num_port_modem_b = 0
        self.num_port_psd = 0
        self.num_tel_a = 0
        self.num_tel_b = 0
        self.login_modem_a = 0
        self.login_modem_b = 0
        self.parole_modem_a = 0
        self.parole_modem_b = 0
        self.apn_modem_a = 0
        self.apn_modem_b = 0
        self.forse_en = 0
        self.gprs_per_norm = 0


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
        self.initWriter()
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

    def stopRead(self):
        self.signal.stopRead.emit()

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
            self.contr_setbasic.time_msg = datetime.now()[:-7]
            self.contr_setbasic.rz0 = data[0]
            self.contr_setbasic.rst_kontrol = data[1]
            self.contr_setbasic.sel_d_himid = data[2]
            self.contr_setbasic.sel_d_speed = data[3]
            self.contr_setbasic.sel_dw_forse = data[4]
            self.contr_setbasic.sel_dwl_forse = data[5]
            self.contr_setbasic.num_dw_forse = data[6]
            self.contr_setbasic.num_dwl_forse = data[7]
            self.contr_setbasic.adr_dw_forse = data[8]
            self.contr_setbasic.adr_dwl_forse = data[9]
            self.contr_setbasic.adr_ms = data[10]
            self.contr_setbasic.per_datch = data[11]
            self.contr_setbasic.per_obmen = data[12]

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

            self.contr_data.time_msg = datetime.now()[:-7]
            self.contr_data.adr_dev = data[0][0]
            self.contr_data.num_dev = data[0][1]
            self.contr_data.per_rstsyst = data[0][5]

            for i in range(0, 20, 2):
                self.contr_data.f_w.append(data[1][i])
                self.contr_data.t_w.append(data[1][i + 1])

            for i in range(2, 4):
                for j in range(0, 40, 4):
                    self.contr_data.f_wl.append(data[i][j])
                    self.contr_data.t_wl.append(data[i][j + 1])
                    self.contr_data.tp_wl.append(data[i][j + 2])
                    self.contr_data.u_wl.append(data[i][j + 3])

            self.contr_data.t_vlagn = data[4][0]
            self.contr_data.vlagn = data[4][1]
            self.contr_data.napr_vetr = data[4][2]
            self.contr_data.scor_vetr = round(unpack('f', pack('<HH', data[4][4], data[4][3]))[0], 2)
            self.contr_data.napr_pit = round(unpack('f', pack('<HH', data[4][6], data[4][5]))[0], 2)
            self.contr_data.t_ds18s20 = data[4][7]
            self.contr_data.status_int = data[4][8]

        except Exception as e:
            print('ERROR in parsData')
            print(str(e))

    def parsConSet(self, data):
        try:
            print(data)

        except Exception as e:
            print('ERROR in parsConSet')
            print(str(e))

    def parsThreshold(self, data):
        try:
            self.contr_setThresh.f_w_max = []
            self.contr_setThresh.f_wl_max = []
            for i in range(10):
                self.contr_setThresh.f_w_max.append(data[0][i])

            for i in range(20):
                self.contr_setThresh.f_wl_max.append(data[1][i])

        except Exception as e:
            print('ERROR in parsThreshold')
            print(str(e))
    def viewTable(self, tag):
        try:
            self.signal.finish_read.emit(tag)

        except Exception as e:
            print('ERROR in view table')
            print(str(e))

    def initWriter(self):
        self.writeVal = Writer()
        self.writeVal.signal.write_error.connect(self.writeError)
        self.writeVal.signal.write_finish.connect(self.writeFinish)
        self.signal.startWrite.connect(self.writeVal.startWrite)
        self.signal.stopWrite.connect(self.writeVal.stopWrite)
        self.signal.exitWrite.connect(self.writeVal.exitWrite)
        self.threadpool.start(self.writeVal)

    def startWrite(self, start_adr, values):
        self.signal.startWrite.emit(self.client.client, start_adr, values)

    def stopWrite(self):
        self.signal.stopWrite.emit()

    def exitWrite(self):
        self.signal.exitWrite.emit()

    def writeError(self, txt):
        print(txt)

    def writeFinish(self):
        print('Write OK')
        self.flag_write = True
        self.stopWrite()

    def writeValue(self, start_adr, value):
        try:
            self.start_adr = start_adr
            self.value = value

        except Exception as e:
            print(str(e))
            print('ERROR in startValue')
