import time

from client import Client
from struct import pack, unpack
from datetime import datetime
from PyQt5.QtCore import QObject, QThreadPool, pyqtSignal
from threads import Reader, Writer


class WinSignals(QObject):
    startRead = pyqtSignal(object)
    stopRead = pyqtSignal()
    exitRead = pyqtSignal()
    startWrite = pyqtSignal(object, int, list)
    stopWrite = pyqtSignal()
    exitWrite = pyqtSignal()
    finish_read = pyqtSignal(str)


class DataController:
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


class SettingController:
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
        self.f_w_max = []
        self.f_wl_max = []


class Model:
    def __init__(self):
        self.signal = WinSignals()
        self.client = Client()
        self.data_cont = DataController()
        self.set_cont = SettingController()
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

    def startRead(self):
        self.signal.startRead.emit(self.client.client)

    def stopRead(self):
        self.signal.stopRead.emit()

    def exitRead(self):
        self.signal.exitRead.emit()

    def readError(self, txt):
        print(txt)

    def readResult(self, tag, data):
        try:
            if tag == 'block_1':
                temp = 1
                self.data_cont.time_msg = str(datetime.now())[11:-7]

                self.data_cont.adr_dev = data[0]
                self.data_cont.num_dev = data[1]
                self.data_cont.per_rstsyst = data[4]

            if tag == 'block_dw':
                temp = 2
                self.data_cont.f_w = []
                self.data_cont.t_w = []
                for i in range(0, self.set_cont.num_dw_forse * 2, 2):
                    self.data_cont.f_w.append(data[i])
                    self.data_cont.t_w.append(data[i + 1])

            if tag == 'block_dwl_1':
                temp = 3
                self.data_cont.f_wl = []
                self.data_cont.t_wl = []
                self.data_cont.tp_wl = []
                self.data_cont.u_wl = []
                for i in range(0, len(data), 4):
                    self.data_cont.f_wl.append(data[i])
                    self.data_cont.t_wl.append(data[i + 1])
                    self.data_cont.tp_wl.append(data[i + 2])
                    self.data_cont.u_wl.append(data[i + 3])

            if tag == 'block_dwl_2':
                temp = 4
                for i in range(0, len(data), 4):
                    self.data_cont.f_wl.append(data[i])
                    self.data_cont.t_wl.append(data[i + 1])
                    self.data_cont.tp_wl.append(data[i + 2])
                    self.data_cont.u_wl.append(data[i + 3])

            if tag == 'block_end':
                temp = 5
                self.data_cont.t_vlagn = data[0]
                self.data_cont.vlagn = data[1]
                self.data_cont.napr_vetr = data[2]
                self.data_cont.scor_vetr = round(unpack('f', pack('<HH', data[4], data[3]))[0], 2)
                self.data_cont.napr_pit = round(unpack('f', pack('<HH', data[6], data[5]))[0], 2)
                self.data_cont.t_ds18s20 = data[7]
                self.data_cont.status_int = data[8]
                self.viewTable('data')

            if tag == 'block_nastr':
                temp = 6
                self.set_cont.sel_d_himid = data[0]
                self.set_cont.sel_d_speed = data[1]
                self.set_cont.sel_dw_forse = data[2]
                self.set_cont.sel_dwl_forse = data[3]
                self.set_cont.num_dw_forse = data[4]
                self.set_cont.num_dwl_forse = data[5]
                self.set_cont.adr_dw_forse = data[6]
                self.set_cont.adr_dwl_forse = data[7]
                self.set_cont.adr_ms = data[8]
                self.set_cont.per_datch = data[9]
                self.set_cont.per_obmen = data[10]
                self.set_cont.sel_type_trans_a = data[11]
                self.set_cont.sel_type_trans_b = data[12]
                self.set_cont.num_modem = data[13]
                self.viewTable('nastr')

        except Exception as e:
            print('ERROR in read result in {}'.format(temp))
            print(str(e))

    def viewTable(self, tag):
        try:
            self.signal.finish_read.emit(tag)

        except Exception as e:
            print('ERROR in view table')
            print(str(e))

    def dopCodeBinToDec(self, value, bits=16):
        try:
            if value[:1] == '1':
                val_temp = -(2 ** bits - int(value, 2))
            else:
                val_temp = int(value, 2)

            return val_temp

        except Exception as e:
            print(str(e))
            txt = 'ERROR in dopCodeBinToDec'
            print(txt)

    def initWriter(self):
        self.writeVel = Writer()
        self.writeVel.signal.write_error.connect(self.writeError)
        self.writeVel.signal.write_finish.connect(self.writeFinish)
        self.signal.startWrite.connect(self.writeVel.startWrite)
        self.signal.stopWrite.connect(self.writeVel.stopWrite)
        self.signal.exitWrite.connect(self.writeVel.exitWrite)
        self.threadpool.start(self.writeVel)

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
