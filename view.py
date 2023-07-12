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

        self.start_reg = 0
        self.type_reg = 'number'
        self.count_reg = 1
        self.read_dict = {'basic_set': False, 'data': False, 'threshold': False, 'con_set': False}

        self.model.signal.finish_read.connect(self.initTable)

    def closeEvent(self, event):
        self.model.exitRead()
        self.model.exitWrite()
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

    def winWriteShow(self, text_lbl, start_reg, type_reg='number', count_reg=1):
        try:
            self.model.flag_write = False
            self.start_reg = start_reg
            self.type_reg = type_reg
            self.count_reg = count_reg
            self.win_write.show()
            self.win_write.value_LE.clear()
            self.win_write.value_LE.setFocus()
            self.win_write.label.setText(text_lbl)

        except Exception as e:
            print(str(e))

    def initWriteVal(self):
        try:
            ascii_list = []
            msg_list = []
            temp = self.win_write.value_LE.text()
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
            if c == 1:
                comm_write = True
                if r == 1:
                    tag = 'SEL_D_HIMID'
                    start_reg = 8194
                elif r == 2:
                    tag = 'SEL_D_SPEED'
                    start_reg = 8195
                elif r == 3:
                    tag = 'SEL_DW_FORSE'
                    start_reg = 8196
                elif r == 4:
                    tag = 'SEL_DWL_FORSE'
                    start_reg = 8197
                elif r == 5:
                    tag = 'NUM_DW_FORSE'
                    start_reg = 8198
                elif r == 6:
                    tag = 'NUM_DWL_FORSE'
                    start_reg = 8199
                elif r == 7:
                    tag = 'ADR_DW_FORSE'
                    start_reg = 8200
                elif r == 8:
                    tag = 'ADR_DWL_FORSE'
                    start_reg = 8201
                elif r == 9:
                    tag = 'ADR_MS'
                    start_reg = 8202
                elif r == 10:
                    tag = 'PER_DATCH'
                    start_reg = 8203
                elif r == 11:
                    tag = 'PER_OBMEN'
                    start_reg = 8204

                else:
                    comm_write = False
            else:
                pass

            if comm_write:
                print('tag - {}, start_reg - {}'.format(tag, start_reg))
                self.winWriteShow(tag, start_reg)
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
            if c == 1:
                comm_write = True
                if r == 2:
                    tag = 'NUM_DEV'
                    start_reg = 1
                elif r == 3:
                    tag = 'PER_RSTSYST'
                    start_reg = 4
                else:
                    comm_write = False
            else:
                pass

            if comm_write:
                self.winWriteShow(tag, start_reg)
            else:
                pass

        except Exception as e:
            print('ERROR in clickedTableData')
            print(str(e))

    def clickedTableConSet(self, r, c):
        try:
            tag = ''
            start_reg = 0
            type_reg = 'number'
            count_reg = 1
            comm_write = False
            if c == 1:
                comm_write = True
                type_reg = 'number'
                if r == 1:
                    tag = 'SEL_TYPE_TRANS_A'
                    start_reg = 8205
                elif r == 2:
                    tag = 'SEL_TYPE_TRANS_B'
                    start_reg = 8206
                elif r == 3:
                    tag = 'NUM_MODEM'
                    start_reg = 8207
                elif r == 4:
                    tag = 'FORSE_EN'
                    start_reg = 8208
                elif r == 5:
                    tag = 'GPRS_PER_NORM'
                    start_reg = 8209
                elif r == 6:
                    tag = 'ADR_IP_MODEM_A'
                    start_reg = 8224
                    type_reg = 'symbol'
                    count_reg = 8
                elif r == 7:
                    tag = 'ADR_IP_MODEM_B'
                    start_reg = 8232
                    type_reg = 'symbol'
                    count_reg = 8
                elif r == 8:
                    tag = 'ADR_IP_PSD'
                    start_reg = 8240
                    type_reg = 'symbol'
                    count_reg = 8
                elif r == 9:
                    tag = 'NUM_PORT_MODEM_A'
                    start_reg = 8248
                    type_reg = 'symbol'
                    count_reg = 4
                elif r == 10:
                    tag = 'NUM_PORT_MODEM_B'
                    start_reg = 8252
                    type_reg = 'symbol'
                    count_reg = 4
                elif r == 11:
                    tag = 'NUM_PORT_PSD'
                    start_reg = 8256
                    type_reg = 'symbol'
                    count_reg = 4
                elif r == 12:
                    tag = 'NUM_TEL_A'
                    start_reg = 8260
                    type_reg = 'symbol'
                    count_reg = 6
                elif r == 13:
                    tag = 'NUM_TEL_B'
                    start_reg = 8266
                    type_reg = 'symbol'
                    count_reg = 6
                elif r == 14:
                    tag = 'LOGIN_MODEM_A'
                    start_reg = 8272
                    type_reg = 'symbol'
                    count_reg = 16
                elif r == 15:
                    tag = 'LOGIN_MODEM_B'
                    start_reg = 8288
                    type_reg = 'symbol'
                    count_reg = 16
                elif r == 16:
                    tag = 'PAROLE_MODEM_A'
                    start_reg = 8304
                    type_reg = 'symbol'
                    count_reg = 16
                elif r == 17:
                    tag = 'PAROLE_MODEM_B'
                    start_reg = 8320
                    type_reg = 'symbol'
                    count_reg = 16
                elif r == 18:
                    tag = 'APN_MODEM_A'
                    start_reg = 8336
                    type_reg = 'symbol'
                    count_reg = 16
                elif r == 19:
                    tag = 'APN_MODEM_B'
                    start_reg = 8352
                    type_reg = 'symbol'
                    count_reg = 16

                else:
                    comm_write = False

            if comm_write:
                self.winWriteShow(tag, start_reg, type_reg, count_reg)
            else:
                pass

        except Exception as e:
            print('ERROR in clickedTableConSet')
            print(str(e))

    def clickedTableThreshold(self, r, c):
        try:
            tag = ''
            start_reg = ''
            comm_write = False
            if c == 1:
                comm_write = True
                adr_dw = int(self.model.contr_setbasic.adr_dw_forse)
                num_dw = int(self.model.contr_setbasic.num_dw_forse)
                adr_dwl = int(self.model.contr_setbasic.adr_dwl_forse)
                num_dwl = int(self.model.contr_setbasic.num_dwl_forse)

                if 0 < r <= num_dw + num_dwl:
                    if r <= num_dw:
                        tag = 'F_{}_W_Max'.format(adr_dw + r - 1)
                        start_reg = 8384 + r - 1

                    if r > num_dw:
                        tag = 'F_{}_WL_Max'.format(adr_dwl + r - num_dw - 1)
                        start_reg = 8394 + r - num_dw - 1

                else:
                    comm_write = False
            else:
                pass

            if comm_write:
                self.winWriteShow(tag, start_reg)
            else:
                pass

        except Exception as e:
            print('ERROR in clickedTableThreshold')
            print(str(e))
