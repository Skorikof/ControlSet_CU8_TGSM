import serial.tools.list_ports
from pymodbus.client import ModbusTcpClient, ModbusSerialClient
from pymodbus.framer import ModbusAsciiFramer, ModbusSocketFramer
from PyQt5.QtCore import QObject, pyqtSignal


class ClientSignals(QObject):
    client_msg = pyqtSignal(str)


class Client:
    def __init__(self):
        self.signal = ClientSignals()
        self.client = None
        self.server = None
        self.flag_connect = False

    def port_scan(self) -> list:
        """Сканирует систему на спользуемые СОМ-порты и возвращвет список"""
        try:
            result = []

            ports = serial.tools.list_ports.comports()
            for port in ports:
                result.append(port.device)

            return result

        except Exception as e:
            txt = 'ERROR in Client/port_scan - {}'.format(e)
            self.msg_client(txt)

    def connect_com(self, port) -> bool:
        """Подключение к контроллеру через СОМ-порт, возвращает состояние подключения"""
        try:
            self.client = ModbusSerialClient(port=port,
                                             framer=ModbusAsciiFramer,
                                             baudrate=9600,
                                             bytesize=8,
                                             parity='N',
                                             stopbits=1,
                                             strict=False,
                                             retries=4,
                                             timeout=1,
                                             retry_on_empty=True)

            self.flag_connect = self.client.connect()

        except Exception as e:
            txt = 'ERROR in Client/connect_com - {}'.format(e)
            self.msg_client(txt)

        finally:
            if self.flag_connect:
                txt = 'Соединение установлено'
            else:
                txt = 'Соединение не установлено'
            self.msg_client(txt)

            return self.flag_connect

    def connect_tcp(self, port, host='localhost') -> bool:
        """Подключение к контроллеру через ТСР, возвращает состояние подключения"""
        try:
            self.client = ModbusTcpClient(host=host,
                                          port=port,
                                          framer=ModbusSocketFramer,
                                          timeout=1,
                                          retries=4,
                                          retry_on_empty=True)

            self.flag_connect = self.client.connect()

        except Exception as e:
            txt = 'ERROR in Client/connect_tcp - {}'.format(e)
            self.msg_client(txt)

        finally:
            if self.flag_connect:
                txt = 'Соединение установлено'
            else:
                txt = 'Соединение не установлено'
            self.msg_client(txt)

            return self.flag_connect

    def close_client(self):
        """Закрывает клиент"""
        try:
            self.client.close()
            self.flag_connect = False
            print('Connect is stopped')

        except Exception as e:
            txt = 'ERROR in Client/close_client - {}'.format(e)
            self.msg_client(txt)

    def msg_client(self, txt_err):
        self.signal.client_msg.emit(txt_err)
