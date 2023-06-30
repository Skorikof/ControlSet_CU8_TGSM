import serial
from pymodbus.client.sync import ModbusSerialClient as ModBusClient


class Client:
    def __init__(self):
        self.client = None
        self.flag_connect = False

    def port_scan(self):
        try:
            result = []
            ports = ['COM{}'.format(i + i) for i in range(256)]
            for port in ports:
                try:
                    s = serial.Serial(port)
                    s.close()
                    result.append(port)

                except:
                    pass

            return result

        except Exception as e:
            print('ERROR in scan port')
            print(str(e))

    def connectClient(self, port):
        try:
            self.client = ModBusClient(method='ascii', port='COM4', parity='N', baudrate=9600,
                                       databits=8, stopbits=1, strict=False, retries=5, timeout=1000)

            self.flag_connect = self.client.connect()
            if self.flag_connect:
                print('Controller is connect')

            else:
                print('Controller is not connect')

        except Exception as e:
            print('ERROR in connect client')
            print(str(e))

    def closeClient(self):
        self.client.close()
        self.flag_connect = False
        print('Connect is stopped')
