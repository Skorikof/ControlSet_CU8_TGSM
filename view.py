from tableui import TableView
from struct import pack, unpack
from mainui import Ui_MainWindow, WinWrite
from PyQt5.QtWidgets import QMainWindow


class AppWindow(QMainWindow):
    def __init__(self, model):
        super(AppWindow, self).__init__()
        self.model = model
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.win_write = WinWrite()
        self.table = TableView()
        self.com_port()
        self.buttons()
        self.initCheckBox()
        self.initTableClicked()

        self.type_ui = 'LineEdit'
        self.start_reg = 0
        self.type_reg = 'number'
        self.count_reg = 1
        self.write_value = ''
        self.read_dict = {'basic_set': False, 'data': False, 'threshold': False, 'con_set': False}

        self.model.signal.finish_read.connect(self.initTable)

    def closeEvent(self, event):
        self.model.exitRead()
        self.model.closeContr()
        self.close()

    def com_port(self):
        try:
            for i in range(len(self.model.available_ports)):
                self.ui.com_port_cb.addItem(self.model.available_ports[i])

            self.model.com_port = self.ui.com_port_cb.currentText()
            self.ui.com_port_cb.activated[str].connect(self.select_port)

        except Exception as e:
            print(str(e))

    def select_port(self, port):
        try:
            self.model.com_port = port

        except Exception as e:
            print(str(e))

    def buttons(self):
        try:
            self.ui.connect_btn.clicked.connect(self.model.connectContr)
            self.ui.read_btn.clicked.connect(self.readDataContr)
            self.ui.stop_btn.clicked.connect(self.model.stopRead)

            self.win_write.value_LE.returnPressed.connect(self.initWriteVal)
            self.win_write.write_value_btn.clicked.connect(self.initWriteVal)
            self.win_write.cancel_value_btn.clicked.connect(self.winWriteClose)

        except Exception as e:
            print(str(e))

    def initCheckBox(self):
        try:
            self.ui.basic_set_chb.setChecked(False)
            self.ui.data_chb.setChecked(False)
            self.ui.threshold_chb.setChecked(False)
            self.ui.con_set_chb.setChecked(False)
            self.ui.basic_set_chb.stateChanged.connect(lambda: self.initReadDict(self.ui.basic_set_chb, 'basic_set'))
            self.ui.data_chb.stateChanged.connect(lambda: self.initReadDict(self.ui.data_chb, 'data'))
            self.ui.threshold_chb.stateChanged.connect(lambda: self.initReadDict(self.ui.threshold_chb, 'threshold'))
            self.ui.con_set_chb.stateChanged.connect(lambda: self.initReadDict(self.ui.con_set_chb, 'con_set'))

        except Exception as e:
            print('ERROR in init combobox')
            print(str(e))

    def initReadDict(self, chb, tag):
        try:
            if chb.isChecked():
                self.read_dict[tag] = True
            else:
                self.read_dict[tag] = False

        except Exception as e:
            print('ERROR init dict read')
            print(str(e))

    def initTable(self, tag):
        try:
            num_dw = int(self.model.contr_setbasic.num_dw_forse)
            adr_dw = int(self.model.contr_setbasic.adr_dw_forse)
            num_dwl = int(self.model.contr_setbasic.num_dwl_forse)
            adr_dwl = int(self.model.contr_setbasic.adr_dwl_forse)
            if tag == 'basic_set':
                self.ui.basic_set_table.clear()
                self.table.initTableBasic(self.ui.basic_set_table, self.model.contr_setbasic)
            if tag == 'data':
                self.ui.data_table.clear()
                self.table.initTableData(self.ui.data_table, num_dw, adr_dw, num_dwl, adr_dwl, self.model.contr_data)
            if tag == 'con_set':
                self.ui.con_set_table.clear()
                self.table.initTableConnect(self.ui.con_set_table, self.model.contr_setConnect)
            if tag == 'threshold':
                self.ui.threshold_table.clear()
                self.table.initTableThreshold(self.ui.threshold_table, num_dw, adr_dw, num_dwl, adr_dwl,
                                              self.model.contr_setThresh)

        except Exception as e:
            print('ERROR in init table')
            print(str(e))

    def initTableClicked(self):
        self.ui.basic_set_table.cellClicked[int, int].connect(self.clickedTableBasic)
        self.ui.data_table.cellClicked[int, int].connect(self.clickedTableData)
        self.ui.con_set_table.cellClicked[int, int].connect(self.clickedTableConSet)
        self.ui.threshold_table.cellClicked[int, int].connect(self.clickedTableThreshold)

    def readDataContr(self):
        self.model.startRead(self.read_dict)

    def winWriteShow(self, text_lbl, type_ui, start_reg, type_reg='number', count_reg=1):
        try:
            self.model.flag_write = False
            self.type_ui = type_ui
            self.start_reg = start_reg
            self.type_reg = type_reg
            self.count_reg = count_reg
            self.win_write.show()
            self.win_write.label.setText(text_lbl)
            if self.type_ui == 'LineEdit':
                self.win_write.comboBox.setVisible(False)
                self.win_write.value_LE.setVisible(True)
                self.win_write.value_LE.clear()
                self.win_write.value_LE.setFocus()

            elif self.type_ui == 'ComboBox':
                self.win_write.value_LE.setVisible(False)
                self.win_write.comboBox.setVisible(True)
                self.win_write.comboBox.clear()
                self.initComboBox()

        except Exception as e:
            print(str(e))

    def initComboBox(self):
        try:
            self.selectComboBox(0)
            if self.start_reg == 8194:
                self.win_write.comboBox.addItems(['SHT75', 'SHT85', 'HIH6000-HIH9000', 'Метеостанция'])

            elif self.start_reg == 8195:
                self.win_write.comboBox.addItems(['DEVIS', 'Метеостанция'])

            elif self.start_reg == 8196:
                self.win_write.comboBox.addItems(['Протокол обмена ASCII', 'Протокол обмена MODBUS-RTU'])

            elif self.start_reg == 8197:
                self.win_write.comboBox.addItems(['Датчики Селезнёва', 'Датчики Седышева'])

            elif self.start_reg == 8205 or self.start_reg == 8206:
                self.win_write.comboBox.addItems(['DATA-modem', 'GPRS, динамический IP', 'GPRS, статический IP'])

            elif self.start_reg == 8207:
                self.win_write.comboBox.addItems(['Один модем', 'Два модема'])

            elif self.start_reg == 8208:
                self.win_write.comboBox.addItems(['Не отслеживается', 'Отслеживается'])

            self.win_write.comboBox.activated[int].connect(self.selectComboBox)

        except Exception as e:
            print('ERROR in initComboBox')
            print(str(e))

    def selectComboBox(self, value):
        try:
            self.write_value = str(value)

        except Exception as e:
            print('ERROR in selectComboBox')
            print(str(e))

    def winWriteClose(self):
        try:
            self.win_write.close()

        except Exception as e:
            print('ERROR in winWriteClose')
            print(str(e))

    def initWriteVal(self):
        try:
            ascii_list = []
            msg_list = []
            if self.type_ui == 'LineEdit':
                temp = self.win_write.value_LE.text()
            else:
                temp = self.write_value
            if len(temp) > 0:
                if self.type_reg == 'number':
                    msg_list.append(int(temp))

                elif self.type_reg == 'symbol':
                    for i in range(len(temp)):
                        ascii_list.append(ord(temp[i]))

                    ascii_list.append(0)

                    while len(ascii_list) < self.count_reg * 2:
                        ascii_list.append(35)

                    for i in range(0, len(ascii_list), 2):
                        temp_u = []
                        temp_u.append(ascii_list[i])
                        temp_u.append(ascii_list[i + 1])
                        bytes_arr = bytes(temp_u)
                        val_int = int.from_bytes(bytes_arr, byteorder='big', signed=False)
                        msg_list.append(val_int)

                self.win_write.close()
                self.model.initWriter(self.start_reg, msg_list)

            else:
                pass

        except Exception as e:
            print(str(e))
            print('ERROR in initWriteVal')

    def clickedTableBasic(self, r, c):
        try:
            tag = ''
            start_reg = 0
            comm_write = False
            type_ui = 'LineEdit'
            if c == 1:
                comm_write = True
                if r == 1:
                    tag = 'Тип датчика влажности'
                    start_reg = 8194
                    type_ui = 'ComboBox'
                elif r == 2:
                    tag = 'Тип датчика направления и скорости ветра'
                    start_reg = 8195
                    type_ui = 'ComboBox'
                elif r == 3:
                    tag = 'Тип проводных датчиков усилия'
                    start_reg = 8196
                    type_ui = 'ComboBox'
                elif r == 4:
                    tag = 'Тип беспроводных датчиков усилия'
                    start_reg = 8197
                    type_ui = 'ComboBox'
                elif r == 5:
                    tag = 'Количество проводных датчиков усилия'
                    start_reg = 8198
                    type_ui = 'LineEdit'
                elif r == 6:
                    tag = 'Количество беспроводных датчиков усилия'
                    start_reg = 8199
                    type_ui = 'LineEdit'
                elif r == 7:
                    tag = 'Начальный адрес проводных датчиков'
                    start_reg = 8200
                    type_ui = 'LineEdit'
                elif r == 8:
                    tag = 'Начальный адрес беспроводных датчиков'
                    start_reg = 8201
                    type_ui = 'LineEdit'
                elif r == 9:
                    tag = 'Адрес контроллера метеостанции'
                    start_reg = 8202
                    type_ui = 'LineEdit'
                elif r == 10:
                    tag = 'Период опроса датчиков, сек'
                    start_reg = 8203
                    type_ui = 'LineEdit'
                elif r == 11:
                    tag = 'Период сеанса связи пункта наблюдения, сек'
                    start_reg = 8204
                    type_ui = 'LineEdit'

                else:
                    comm_write = False
            else:
                pass

            if comm_write:
                print('tag - {}, start_reg - {}'.format(tag, start_reg))
                self.winWriteShow(tag, type_ui, start_reg)
            else:
                pass

        except Exception as e:
            print('ERROR in clickedTableBasic')
            print(str(e))

    def clickedTableData(self, r, c):
        try:
            tag = ''
            start_reg = 0
            comm_write = False
            type_ui = 'LineEdit'
            if c == 1:
                comm_write = True
                if r == 1:
                    tag = 'Номер контроллера'
                    start_reg = 1
                elif r == 2:
                    tag = 'Период программного сброса, мин'
                    start_reg = 4
                else:
                    comm_write = False
            else:
                pass

            if comm_write:
                self.winWriteShow(tag, type_ui, start_reg)
            else:
                pass

        except Exception as e:
            print('ERROR in clickedTableData')
            print(str(e))

    def clickedTableConSet(self, r, c):
        try:
            tag = ''
            type_ui = 'LineEdit'
            start_reg = 0
            type_reg = 'number'
            count_reg = 1
            comm_write = False
            if c == 1:
                comm_write = True
                type_reg = 'number'
                if r == 1:
                    tag = 'Тип передачи первого модема'
                    start_reg = 8205
                    type_ui = 'ComboBox'
                elif r == 2:
                    tag = 'Тип передачи второго модема'
                    start_reg = 8206
                    type_ui = 'ComboBox'
                elif r == 3:
                    tag = 'Количество модемов'
                    start_reg = 8207
                    type_ui = 'ComboBox'
                elif r == 4:
                    tag = 'Отслеживание превышения усилия'
                    start_reg = 8208
                    type_ui = 'ComboBox'
                elif r == 5:
                    tag = 'Период передачи через GPRS\nри нормальных условиях, мин'
                    start_reg = 8209
                    type_ui = 'LineEdit'
                elif r == 6:
                    tag = 'Статический IP адрес первого модема'
                    start_reg = 8224
                    type_reg = 'symbol'
                    count_reg = 8
                    type_ui = 'LineEdit'
                elif r == 7:
                    tag = 'Статический IP адрес второго модема'
                    start_reg = 8232
                    type_reg = 'symbol'
                    count_reg = 8
                    type_ui = 'LineEdit'
                elif r == 8:
                    tag = 'Статический IP адрес ПСД'
                    start_reg = 8240
                    type_reg = 'symbol'
                    count_reg = 8
                    type_ui = 'LineEdit'
                elif r == 9:
                    tag = 'Номер порта первого модема'
                    start_reg = 8248
                    type_reg = 'symbol'
                    count_reg = 4
                    type_ui = 'LineEdit'
                elif r == 10:
                    tag = 'Номер порта второго модема'
                    start_reg = 8252
                    type_reg = 'symbol'
                    count_reg = 4
                    type_ui = 'LineEdit'
                elif r == 11:
                    tag = 'Номер порта для GPRS связи'
                    start_reg = 8256
                    type_reg = 'symbol'
                    count_reg = 4
                    type_ui = 'LineEdit'
                elif r == 12:
                    tag = 'Основной номер телефона ПСД'
                    start_reg = 8260
                    type_reg = 'symbol'
                    count_reg = 6
                    type_ui = 'LineEdit'
                elif r == 13:
                    tag = 'Резервный номер телефона ПСД'
                    start_reg = 8266
                    type_reg = 'symbol'
                    count_reg = 6
                    type_ui = 'LineEdit'
                elif r == 14:
                    tag = 'Логин первого модема'
                    start_reg = 8272
                    type_reg = 'symbol'
                    count_reg = 16
                    type_ui = 'LineEdit'
                elif r == 15:
                    tag = 'Логин второго модема'
                    start_reg = 8288
                    type_reg = 'symbol'
                    count_reg = 16
                    type_ui = 'LineEdit'
                elif r == 16:
                    tag = 'Пароль первого модема'
                    start_reg = 8304
                    type_reg = 'symbol'
                    count_reg = 16
                    type_ui = 'LineEdit'
                elif r == 17:
                    tag = 'Пароль второго модема'
                    start_reg = 8320
                    type_reg = 'symbol'
                    count_reg = 16
                    type_ui = 'LineEdit'
                elif r == 18:
                    tag = 'APN первого модема'
                    start_reg = 8336
                    type_reg = 'symbol'
                    count_reg = 16
                    type_ui = 'LineEdit'
                elif r == 19:
                    tag = 'APN второго модема'
                    start_reg = 8352
                    type_reg = 'symbol'
                    count_reg = 16
                    type_ui = 'LineEdit'

                else:
                    comm_write = False

            if comm_write:
                self.winWriteShow(tag, type_ui, start_reg, type_reg, count_reg)
            else:
                pass

        except Exception as e:
            print('ERROR in clickedTableConSet')
            print(str(e))

    def clickedTableThreshold(self, r, c):
        try:
            tag = ''
            type_ui = 'LineEdit'
            start_reg = ''
            comm_write = False
            if c == 1:
                comm_write = True
                adr_dw = int(self.model.contr_setbasic.adr_dw_forse)
                num_dw = int(self.model.contr_setbasic.num_dw_forse)
                adr_dwl = int(self.model.contr_setbasic.adr_dwl_forse)
                num_dwl = int(self.model.contr_setbasic.num_dwl_forse)

                if 1 < r <= num_dw + num_dwl + 2:
                    if r <= num_dw + 1:
                        tag = 'Порог проводного датчика №{}, кг'.format(adr_dw + r - 2)
                        start_reg = 8384 + r - 2

                    if r > num_dw + 2:
                        tag = 'Порог беспроводного датчика №{}, кг'.format(adr_dwl + r - num_dw - 3)
                        start_reg = 8394 + r - num_dw - 3

                else:
                    comm_write = False
            else:
                pass

            if comm_write:
                self.winWriteShow(tag, type_ui, start_reg)
            else:
                pass

        except Exception as e:
            print('ERROR in clickedTableThreshold')
            print(str(e))
