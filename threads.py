import time
import socket
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot


class Signals(QObject):
    connect_result = pyqtSignal(str)
    connect_error = pyqtSignal(str)
    connect_client = pyqtSignal(tuple)
    connect_restart = pyqtSignal()
    read_result = pyqtSignal(str, list)
    read_flag = pyqtSignal(bool)
    read_error = pyqtSignal(str)
    write_finish = pyqtSignal()
    write_error = pyqtSignal(str)


class ConnectTCP(QRunnable):
    signal = Signals()

    def __init__(self):
        super(ConnectTCP, self).__init__()
        self.cycle = True
        self.flag_connect = False

    @pyqtSlot()
    def run(self):
        while self.cycle:
            while not self.flag_connect:
                time.sleep(0.5)

            while self.flag_connect:
                try:
                    conn, addr = self.sock.accept()
                    txt = 'New connection from - {}'.format(addr)
                    self.signal.connect_result.emit(txt)
                    data = conn.recv(1024)
                    txt = 'MSG - {}'.format(data.decode())
                    self.signal.connect_result.emit(txt)
                    if data.decode() == 'CONNECT OK':
                        # self.signal.connect_client.emit(addr)
                        while True:
                            msg = '3A30313033303030303030303146420D0A'
                            conn.send(bytearray.fromhex(msg))
                            data = conn.recv(1024)
                            txt = 'MSG - {}'.format(data.decode())
                            self.signal.connect_result.emit(txt)
                            time.sleep(10)

                        # self.signal.connect_restart.emit()

                except Exception as e:
                    txt = 'ERROR in thread connect GPRS - {}'.format(e)
                    self.signal.read_error.emit(txt)

    def startConnect(self, port):
        try:
            self.count_msg = 0
            self.port = port
            self.flag_connect = False
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('', self.port))
            self.sock.listen(1)
            txt = 'Port {} is connect'.format(self.port)
            self.signal.connect_result.emit(txt)
            self.cycle = True
            self.flag_connect = True

        except Exception as e:
            txt = 'ERROR in thread start connect GPRS - {}'.format(e)
            self.flag_connect = False
            self.sock.close()
            self.signal.connect_error.emit(txt)

    def exitConnect(self):
        self.sock.close()
        self.cycle = False


class Reader(QRunnable):
    signal = Signals()

    def __init__(self):
        super(Reader, self).__init__()
        self.cycle = True
        self.is_run = False
        self.flag_read = False

    @pyqtSlot()
    def run(self):
        while self.cycle:
            try:
                if not self.is_run:
                    time.sleep(0.01)
                else:
                    temp = self.read_regs(0, 1)
                    if self.read_dict['basic_set'] == True:
                        self.flag_read = True
                        basic_list = list(self.read_regs(8192, 13))

                        self.signal.read_result.emit('basic_set', basic_list)
                        self.flag_read = False

                    if self.read_dict['data'] == True:
                        self.flag_read = True
                        data_list = []
                        data_list.append(self.read_regs(0, 5))
                        data_list.append(self.read_regs(4096, 20))
                        data_list.append(self.read_regs(4116, 40))
                        data_list.append(self.read_regs(4156, 40))
                        data_list.append(self.read_regs(4208, 9))

                        self.signal.read_result.emit('data', data_list)
                        self.flag_read = False

                    if self.read_dict['con_set'] == True:
                        self.flag_read = True
                        connect_list = []
                        connect_list.append(self.read_regs(8205, 5))
                        connect_list.append(self.read_regs(8224, 8))
                        connect_list.append(self.read_regs(8232, 8))
                        connect_list.append(self.read_regs(8240, 8))
                        connect_list.append(self.read_regs(8248, 4))
                        connect_list.append(self.read_regs(8252, 4))
                        connect_list.append(self.read_regs(8256, 4))
                        connect_list.append(self.read_regs(8260, 6))
                        connect_list.append(self.read_regs(8266, 6))
                        connect_list.append(self.read_regs(8272, 16))
                        connect_list.append(self.read_regs(8288, 16))
                        connect_list.append(self.read_regs(8304, 16))
                        connect_list.append(self.read_regs(8320, 16))
                        connect_list.append(self.read_regs(8336, 16))
                        connect_list.append(self.read_regs(8352, 16))

                        self.signal.read_result.emit('con_set', connect_list)
                        self.flag_read = False

                    if self.read_dict['threshold'] == True:
                        self.flag_read = True
                        threshold_list = []
                        threshold_list.append(self.read_regs(8384, 10))
                        threshold_list.append(self.read_regs(8394, 20))

                        self.signal.read_result.emit('threshold', threshold_list)
                        self.flag_read = False

                    self.signal.read_flag.emit(self.flag_read)
                    time.sleep(5)

            except Exception as e:
                txt = 'ERROR in thread Reader - {}'.format(e)
                self.signal.read_error.emit(txt)

    def read_regs(self, adr_reg, num_reg):
        try:
            print('Read {} register'.format(hex(adr_reg)))
            rr = self.client.read_holding_registers(adr_reg, num_reg, unit=1)
            if not rr.isError():
                print('Register {} read comlite!'.format(hex(adr_reg)))
                temp_list = []
                for i in range(len(rr.registers)):
                    temp_list.append(bin(rr.registers[i])[2:].zfill(16))

                return temp_list

            else:
                txt = 'ERROR read {} register'.format(hex(adr_reg))
                self.signal.read_error.emit(txt)

        except Exception as e:
            txt = 'ERROR in thread read regs - {}'.format(e)
            self.signal.read_error.emit(txt)

    def startRead(self, client, read_dict):
        self.client = client
        self.read_dict = read_dict
        self.is_run = True

    def stopRead(self):
        if not self.flag_read:
            self.is_run = False
        else:
            time.sleep(0.1)
            self.stopRead()

    def exitRead(self):
        self.cycle = False


class Writer(QRunnable):
    signal = Signals()

    def __init__(self, client, start_adr, values):
        super(Writer, self).__init__()
        self.client = client
        self.values = values
        self.start_adr = start_adr
        self.number_attempts = 0
        self.max_attempts = 5

    @pyqtSlot()
    def run(self):
        try:
            while self.number_attempts <= self.max_attempts:
                txt = 'Writer, start_adr - {}, value - {}'.format(self.start_adr, self.values)
                self.signal.write_error.emit(txt)
                rq = self.client.write_registers(self.start_adr, self.values, unit=1)
                time.sleep(0.1)
                if not rq.isError():
                    txt = 'Complite write value {} in reg - {}'.format(self.values, self.start_adr)
                    self.signal.write_error.emit(txt)
                    self.flag_write = True
                    self.number_attempts = self.max_attempts + 1
                    if not self.flag_ok:
                        self.signal.write_finish.emit()
                        self.flag_ok = True

                else:
                    txt = 'Attempts write: {}, value {} in reg - {}'.format(self.number_attempts, self.values,
                                                                             self.start_adr)
                    self.signal.write_error.emit(txt)
                    self.number_attempts += 1
                    time.sleep(0.5)
            if not self.flag_write:
                txt = 'Unsuccessful write attempt value {} in reg - {}'.format(self.values, self.start_adr)
                self.signal.write_error.emit(txt)
                txt = 'ERROR format - {}'.format(rq)
                self.signal.write_error.emit(txt)

        except Exception as e:
            txt = 'ERROR in thread Writer - {}'.format(e)
            self.signal.read_error.emit(txt)
