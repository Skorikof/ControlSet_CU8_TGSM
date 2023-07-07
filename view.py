from tableui import TableView
from mainui import Ui_MainWindow, WinWrite
from PyQt5.QtWidgets import QMainWindow


class AppWindow(QMainWindow):
    def __init__(self, model):
        super(AppWindow, self).__init__()
        self.model = model
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.win_write = WinWrite()
        self.win_write.setVisible(False)
        self.table = TableView()
        self.com_port()
        self.buttons()
        self.initCheckBox()
        self.initTable()

        self.start_reg = 0
        self.read_dict = {'basic_set': False, 'data': False, 'threshold': False, 'con_set': False}

        self.model.signal.finish_read.connect(self.viewTable)

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
            self.win_write.cancel_value_btn.clicked.connect(self.winWriteCancel)
            self.win_write.write_value_btn.clicked.connect(self.initWriteVal)

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

            self.readDataContr()

        except Exception as e:
            print('ERROR init dict read')
            print(str(e))

    def initTable(self):
        try:
            num_dw = self.model.contr_setbasic.num_dw_forse
            adr_dw = self.model.contr_setbasic.adr_dw_forse
            num_dwl = self.model.contr_setbasic.num_dwl_forse
            adr_dwl = self.model.contr_setbasic.adr_dwl_forse
            self.ui.basic_set_table = self.table.initTableBasic(self.ui.basic_set_table)
            self.ui.data_table = self.table.initTableData(self.ui.data_table, num_dw, adr_dw, num_dwl, adr_dwl)
            self.ui.con_set_table = self.table.initTableConnect(self.ui.con_set_table)
            self.ui.threshold_table = self.table.initTableThreshold(self.ui.threshold_table,
                                                                    num_dw, adr_dw, num_dwl, adr_dwl)

        except Exception as e:
            print('ERROR in init table')
            print(str(e))

    def readDataContr(self):
        self.model.startRead(self.read_dict)

    def winWriteShow(self, text_lbl, start_reg):
        try:
            self.model.flag_write = False
            self.start_reg = start_reg
            self.win_write.setVisible(True)
            self.win_write.value_LE.clear()
            self.win_write.label.setText(text_lbl)
            self.win_write.value_LE.returnPressed.connect(self.initWriteVal)

        except Exception as e:
            print(str(e))

    def winWriteCancel(self):
        try:
            self.win_write.close()

        except Exception as e:
            print(str(e))

    def initWriteVal(self):
        try:
            print('\nInside function initWriteVal')
            if not self.model.flag_write:
                print('self.model.flag_write = False')
                temp = self.win_write.value_LE.text()
                print('Value for write - {}'.format(temp))
                if len(temp) > 0:
                    temp_u = int(temp)
                    print('Command write, start_reg - {}, value - {}'.format(self.start_reg, temp_u))
                    self.model.startWrite(self.start_reg, temp_u)
                    self.win_write.setVisible(False)

                else:
                    pass
            else:
                print('self.model.flag_write = True')

        except Exception as e:
            print(str(e))
            print('ERROR in initWriteVal')

    def viewTable(self, tag):
        print(tag)
        # try:
        #     self.ui.tableWidget.blockSignals(True)
        #     if tag == 'nastr':
        #         temp = self.model.set_cont.adr_dw_forse
        #         num_row = 25
        #         for i in range(0, self.model.set_cont.num_dw_forse * 2, 2):
        #             self.ui.tableWidget.setItem(num_row + i, 0, QTableWidgetItem('F_{}_W'.format(temp)))
        #             self.ui.tableWidget.setItem(num_row + 1 + i, 0, QTableWidgetItem('T_{}_W'.format(temp)))
        #             temp += 1
        #
        #         num_row = self.model.set_cont.num_dw_forse * 2 + 25
        #         temp = self.model.set_cont.adr_dwl_forse
        #         for i in range(0, self.model.set_cont.num_dwl_forse * 4, 4):
        #             self.ui.tableWidget.setItem(num_row + i, 0, QTableWidgetItem('F_{}_WL'.format(temp)))
        #             self.ui.tableWidget.setItem(num_row + 1 + i, 0, QTableWidgetItem('T_{}_WL'.format(temp)))
        #             self.ui.tableWidget.setItem(num_row + 2 + i, 0, QTableWidgetItem('TP_{}_WL'.format(temp)))
        #             self.ui.tableWidget.setItem(num_row + 3 + i, 0, QTableWidgetItem('U_{}_WL'.format(temp)))
        #             temp += 1
        #         er_cod = 1
        #         self.ui.tableWidget.setItem(0, 1, QTableWidgetItem(str(self.model.data_cont.time_msg)))
        #         self.ui.tableWidget.setItem(1, 1, QTableWidgetItem(str(self.model.set_cont.sel_d_himid)))
        #         self.ui.tableWidget.setItem(2, 1, QTableWidgetItem(str(self.model.set_cont.sel_d_speed)))
        #         self.ui.tableWidget.setItem(3, 1, QTableWidgetItem(str(self.model.set_cont.sel_dw_forse)))
        #         self.ui.tableWidget.setItem(4, 1, QTableWidgetItem(str(self.model.set_cont.sel_dwl_forse)))
        #         er_cod = 2
        #         self.ui.tableWidget.setItem(5, 1, QTableWidgetItem(str(self.model.set_cont.num_dw_forse)))
        #         self.ui.tableWidget.setItem(6, 1, QTableWidgetItem(str(self.model.set_cont.num_dwl_forse)))
        #         self.ui.tableWidget.setItem(7, 1, QTableWidgetItem(str(self.model.set_cont.adr_dw_forse)))
        #         self.ui.tableWidget.setItem(8, 1, QTableWidgetItem(str(self.model.set_cont.adr_dwl_forse)))
        #         self.ui.tableWidget.setItem(9, 1, QTableWidgetItem(str(self.model.set_cont.adr_ms)))
        #         er_cod = 3
        #         self.ui.tableWidget.setItem(10, 1, QTableWidgetItem(str(self.model.set_cont.per_datch)))
        #         self.ui.tableWidget.setItem(11, 1, QTableWidgetItem(str(self.model.set_cont.per_obmen)))
        #         self.ui.tableWidget.setItem(12, 1, QTableWidgetItem(str(self.model.set_cont.sel_type_trans_a)))
        #         self.ui.tableWidget.setItem(13, 1, QTableWidgetItem(str(self.model.set_cont.sel_type_trans_b)))
        #         self.ui.tableWidget.setItem(14, 1, QTableWidgetItem(str(self.model.set_cont.num_modem)))
        #         er_cod = 4
        #
        #     if tag == 'data':
        #         self.ui.tableWidget.setItem(15, 1, QTableWidgetItem(str(self.model.data_cont.adr_dev)))
        #         self.ui.tableWidget.setItem(16, 1, QTableWidgetItem(str(self.model.data_cont.num_dev)))
        #         self.ui.tableWidget.setItem(17, 1, QTableWidgetItem(str(self.model.data_cont.per_rstsyst)))
        #         er_cod = 5
        #         self.ui.tableWidget.setItem(18, 1, QTableWidgetItem(str(self.model.data_cont.t_vlagn)))
        #         self.ui.tableWidget.setItem(19, 1, QTableWidgetItem(str(self.model.data_cont.vlagn)))
        #         self.ui.tableWidget.setItem(20, 1, QTableWidgetItem(str(self.model.data_cont.napr_vetr)))
        #         self.ui.tableWidget.setItem(21, 1, QTableWidgetItem(str(self.model.data_cont.scor_vetr)))
        #         er_cod = 8
        #         self.ui.tableWidget.setItem(22, 1, QTableWidgetItem(str(self.model.data_cont.napr_pit)))
        #         self.ui.tableWidget.setItem(23, 1, QTableWidgetItem(str(self.model.data_cont.t_ds18s20)))
        #         self.ui.tableWidget.setItem(24, 1, QTableWidgetItem(str(self.model.data_cont.status_int)))
        #         er_cod = 9
        #
        #         temp = 0
        #         num_row = 25
        #         for i in range(0, self.model.set_cont.num_dw_forse * 2, 2):
        #             self.ui.tableWidget.setItem(num_row + i, 1, QTableWidgetItem(str(self.model.data_cont.f_w[temp])))
        #             self.ui.tableWidget.setItem(num_row + 1 + i, 1, QTableWidgetItem(str(self.model.data_cont.t_w[temp])))
        #             temp += 1
        #         er_cod = 6
        #
        #         num_row = self.model.set_cont.num_dw_forse * 2 + 25
        #         temp = 1
        #         for i in range(0, self.model.set_cont.num_dwl_forse * 4, 4):
        #             self.ui.tableWidget.setItem(num_row + i, 1, QTableWidgetItem(str(self.model.data_cont.f_wl[temp - 1])))
        #             self.ui.tableWidget.setItem(num_row + 1 + i, 1, QTableWidgetItem(str(self.model.data_cont.t_wl[temp - 1])))
        #             self.ui.tableWidget.setItem(num_row + 2 + i, 1, QTableWidgetItem(str(self.model.data_cont.tp_wl[temp - 1])))
        #             self.ui.tableWidget.setItem(num_row + 3 + i, 1, QTableWidgetItem(str(self.model.data_cont.u_wl[temp - 1])))
        #             temp += 1
        #         er_cod = 7
        #
        #     self.ui.tableWidget.blockSignals(False)
        #
        # except Exception as e:
        #     print('ERROR in view table in er_code = {}'.format(er_cod))
        #     print(str(e))

    def clickedRowColumn(self, r, c):
        try:
            tag = ''
            start_reg = 0
            if c == 1 and 0 < r < 15:
                if r == 1:
                    tag = 'SEL_D_HIMID'
                    start_reg = 8194
                if r == 2:
                    tag = 'SEL_D_SPEED'
                    start_reg = 8195
                if r == 3:
                    tag = 'SEL_DW_FORSE'
                    start_reg = 8196
                if r == 4:
                    tag = 'SEL_DWL_FORSE'
                    start_reg = 8197
                if r == 5:
                    tag = 'NUM_DW_FORSE'
                    start_reg = 8198
                if r == 6:
                    tag = 'NUM_DWL_FORSE'
                    start_reg = 8199
                if r == 7:
                    tag = 'ADR_DW_FORSE'
                    start_reg = 8200
                if r == 8:
                    tag = 'ADR_DWL_FORSE'
                    start_reg = 8201
                if r == 9:
                    tag = 'ADR_MS'
                    start_reg = 8202
                if r == 10:
                    tag = 'PER_DATCH'
                    start_reg = 8203
                if r == 11:
                    tag = 'PER_OBMEN'
                    start_reg = 8204
                if r == 12:
                    tag = 'SEL_TYPE_TRANS_A'
                    start_reg = 8205
                if r == 13:
                    tag = 'SEL_TYPE_TRANS_B'
                    start_reg = 8206
                if r == 14:
                    tag = 'NUM_MODEM'
                    start_reg = 8207
                if r == 16:
                    tag = 'NUM_DEV'
                    start_reg = 1
                if r == 17:
                    tag = 'PER_RSTSYST'
                    start_reg = 4
                self.winWriteShow(tag, start_reg)
            else:
                pass

        except Exception as e:
            print('ERROR in clickedRowColumn')
            print(str(e))
