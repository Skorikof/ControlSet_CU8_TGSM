import time
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot


class Signals(QObject):
    read_result = pyqtSignal(str, list)
    read_error = pyqtSignal(str)
    write_finish = pyqtSignal()
    write_error = pyqtSignal(str)


class Reader(QRunnable):
    signal = Signals()

    def __init__(self):
        super(Reader, self).__init__()
        self.cycle = True
        self.is_run = False

    @pyqtSlot()
    def run(self):
        while self.cycle:
            try:
                if not self.is_run:
                    time.sleep(0.01)
                else:
                    block_nastr = self.read_int(8194, 14)
                    self.signal.read_result.emit('block_nastr', block_nastr)
                    block_1 = self.read_int(0, 5)
                    block_dw = self.read_int(4096, 20)
                    block_dwl_1 = self.read_int(4116, 40)
                    block_dwl_2 = self.read_int(4156, 40)
                    block_end = self.read_int(4208, 9)

                    self.signal.read_result.emit('block_1', block_1)
                    self.signal.read_result.emit('block_dw', block_dw)
                    self.signal.read_result.emit('block_dwl_1', block_dwl_1)
                    self.signal.read_result.emit('block_dwl_2', block_dwl_2)
                    self.signal.read_result.emit('block_end', block_end)
                    time.sleep(10)

            except Exception as e:
                self.signal.read_error.emit(str(e))
                txt = 'ERROR in main read thread'
                self.signal.read_error.emit(txt)

    def read_int(self, adr_reg, num_reg):
        try:
            print('Read {} register'.format(hex(adr_reg)))
            rr = self.client.read_holding_registers(adr_reg, num_reg, unit=1)
            if not rr.isError():
                print('Register {} read comlite!'.format(hex(adr_reg)))
                temp_list = []
                for i in range(len(rr.registers)):
                    temp_list.append(self.dopCodeBinToDec(bin(rr.registers[i])[2:].zfill(16)))
                return temp_list

            else:
                txt = 'ERROR read {} register'.format(hex(adr_reg))
                self.signal.read_error.emit(txt)
                self.read_int(adr_reg, num_reg)

        except Exception as e:
            self.signal.read_error.emit(str(e))

    def dopCodeBinToDec(self, value, bits=16):
        try:
            if value[:1] == '1':
                val_temp = -(2 ** bits - int(value, 2))
            else:
                val_temp = int(value, 2)

            return val_temp

        except Exception as e:
            self.signal.read_error.emit(str(e))

    def startRead(self, client):
        self.client = client
        self.is_run = True

    def stopRead(self):
        self.is_run = False

    def exitRead(self):
        self.cycle = False


class Writer(QRunnable):
    signal = Signals()

    def __init__(self):
        super(Writer, self).__init__()
        self.cycle = True
        self.is_run = False
        self.number_attempts = 0
        self.max_attempts = 5

    @pyqtSlot()
    def run(self):
        while self.cycle:
            try:
                if not self.is_run:
                    time.sleep(0.01)
                else:
                    while self.number_attempts <= self.max_attempts:
                        temp_list = []
                        temp_list.append(self.values)
                        print('Enter write thread')
                        print('DATA, start_adr - {}, values - {}'.format(self.start_adr, temp_list))
                        rq = self.client.write_registers(self.start_adr, temp_list, unit=1)
                        time.sleep(0.1)
                        if not rq.isError():
                            print('Complite write reg')
                            self.flag_write = True
                            self.number_attempts = self.max_attempts + 1
                            if not self.flag_ok:
                                self.signal.write_finish.emit()
                                self.flag_ok = True

                        else:
                            print('Attempts {}'.format(self.number_attempts))
                            self.number_attempts += 1
                            time.sleep(0.2)
                    if not self.flag_write:
                        txt = 'Ошибка в попытке записи регистра'
                        self.signal.write_error.emit(txt)
                        self.signal.write_error.emit(str(rq))

            except Exception as e:
                self.signal.read_error.emit(str(e))
                txt = 'ERROR in main write thread'
                self.signal.read_error.emit(txt)

    def startWrite(self, client, start_adr, values):
        self.is_run = True
        self.start_adr = start_adr
        self.values = values
        self.client = client
        self.flag_write = False
        self.flag_ok = False

    def stopWrite(self):
        self.is_run = False

    def exitWrite(self):
        self.cycle = False
