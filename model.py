import time

from client import Client
from struct import pack, unpack
from datetime import datetime
from PyQt5.QtCore import QObject, QThreadPool, pyqtSignal
from threads import Reader, Writer


class WinSignals(QObject):
    startRead = pyqtSignal(object, str)
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

    def startRead(self, tag):
        self.signal.startRead.emit(self.client.client, tag)

    def stopRead(self):
        self.signal.stopRead.emit()

    def exitRead(self):
        self.signal.exitRead.emit()

    def readError(self, txt):
        print(txt)

    def readResult(self, tag, data):
        try:
            temp = 0
            if tag == 'basic':
                print(data)

            if tag == 'connect':
                print(data)

            if tag == 'threshold':
                print(data)

        except Exception as e:
            print('ERROR in read result in {}'.format(temp))
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
