import time
from struct import pack, unpack
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
                    temp = self.read_regs(0, 1, 'value')
                    if self.read_dict['basic_set'] == True:
                        basic_list = list(self.read_regs(8192, 13, 'value'))

                        self.signal.read_result.emit('basic_set', basic_list)

                    if self.read_dict['data'] == True:
                        data_list = []
                        data_list.append(self.read_regs(0, 5, 'value'))
                        data_list.append(self.read_regs(4096, 20, 'value'))
                        data_list.append(self.read_regs(4116, 40, 'value'))
                        data_list.append(self.read_regs(4156, 40, 'value'))
                        data_list.append(self.read_regs(4208, 3, 'value'))
                        data_list.append(self.read_regs(4211, 4, 'float'))
                        data_list.append(self.read_regs(4215, 2, 'value'))

                        self.signal.read_result.emit('data', data_list)

                    if self.read_dict['con_set'] == True:
                        connect_list = []
                        connect_list.append(self.read_regs(8205, 5, 'value'))
                        connect_list.append(self.read_regs(8224, 8, 'symbol'))
                        connect_list.append(self.read_regs(8232, 8, 'symbol'))
                        connect_list.append(self.read_regs(8240, 8, 'symbol'))
                        connect_list.append(self.read_regs(8248, 4, 'symbol'))
                        connect_list.append(self.read_regs(8252, 4, 'symbol'))
                        connect_list.append(self.read_regs(8256, 4, 'symbol'))
                        connect_list.append(self.read_regs(8260, 6, 'symbol'))
                        connect_list.append(self.read_regs(8266, 6, 'symbol'))
                        connect_list.append(self.read_regs(8272, 16, 'symbol'))
                        connect_list.append(self.read_regs(8288, 16, 'symbol'))
                        connect_list.append(self.read_regs(8304, 16, 'symbol'))
                        connect_list.append(self.read_regs(8320, 16, 'symbol'))
                        connect_list.append(self.read_regs(8336, 16, 'symbol'))
                        connect_list.append(self.read_regs(8352, 16, 'symbol'))

                        self.signal.read_result.emit('con_set', connect_list)

                    if self.read_dict['threshold'] == True:
                        threshold_list = []
                        threshold_list.append(self.read_regs(8384, 10, 'value'))
                        threshold_list.append(self.read_regs(8394, 20, 'value'))

                        self.signal.read_result.emit('threshold', threshold_list)

                    time.sleep(1)

            except Exception as e:
                self.signal.read_error.emit(str(e))
                txt = 'ERROR in main read thread'
                self.signal.read_error.emit(txt)

    def read_regs(self, adr_reg, num_reg, tag):
        try:
            print('Read {} register'.format(hex(adr_reg)))
            rr = self.client.read_holding_registers(adr_reg, num_reg, unit=1)
            if not rr.isError():
                print('Register {} read comlite!'.format(hex(adr_reg)))
                temp_list = []
                if tag == 'value':
                    for i in range(len(rr.registers)):
                        temp_list.append(self.dopCodeBinToDec(bin(rr.registers[i])[2:].zfill(16)))

                if tag == 'symbol':
                    temp_val = ''
                    for i in range(len(rr.registers)):
                        bytes = rr.registers[i].to_bytes(2, byteorder='big', signed=False)
                        temp_val = temp_val + chr(bytes[0]) + chr(bytes[1])
                    msg = ''
                    for i in range(len(temp_val)):
                        if temp_val[i] != '\00':
                            msg = msg + temp_val[i]
                        else:
                            break

                    temp_list.append(msg)

                if tag == 'float':
                    temp_list.append(round(unpack('f', pack('<HH', rr.registers[1], rr.registers[0]))[0], 2))
                    temp_list.append(round(unpack('f', pack('<HH', rr.registers[3], rr.registers[2]))[0], 2))

                return temp_list

            else:
                txt = 'ERROR read {} register'.format(hex(adr_reg))
                self.signal.read_error.emit(txt)

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

    def startRead(self, client, read_dict):
        self.client = client
        self.read_dict = read_dict
        self.is_run = True

    def stopRead(self):
        self.is_run = False

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
                print('Enter write thread')
                print('DATA, start_adr - {}, values - {}'.format(self.start_adr, self.values))
                rq = self.client.write_registers(self.start_adr, self.values, unit=1)
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
                    time.sleep(0.5)
            if not self.flag_write:
                txt = 'Ошибка в попытке записи регистра'
                self.signal.write_error.emit(txt)
                self.signal.write_error.emit(str(rq))

        except Exception as e:
            self.signal.read_error.emit(str(e))
            txt = 'ERROR in main write thread'
            self.signal.read_error.emit(txt)
