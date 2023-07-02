import sys
from mainui import Ui_MainWindow
from writeui import WriteWindow
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem


class AppWindow(QMainWindow):
    def __init__(self, model):
        super(AppWindow, self).__init__()
        self.model = model
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.win_write = WriteWindow()
        self.com_port()
        self.buttons()
        self.initTable()

        self.start_reg = 0

        self.model.signal.finish_read.connect(self.viewTable)

    def closeEvent(self, event):
        self.model.exitRead()
        self.model.exitWrite()
        self.model.closeContr()
        self.close()

    def com_port(self):
        try:
            for i in range(len(self.model.available_ports)):
                self.ui.com_port_CB.addItem(self.model.available_ports[i])

            self.model.com_port = self.ui.com_port_CB.currentText()
            self.ui.com_port_CB.activated[str].connect(self.select_port)

        except Exception as e:
            print(str(e))

    def select_port(self, port):
        try:
            self.model.com_port = port

        except Exception as e:
            print(str(e))

    def buttons(self):
        try:
            self.ui.connect_BTN.clicked.connect(self.model.connectContr)
            self.ui.read_nastr_BTN.clicked.connect(self.readNastrContr)
            self.ui.read_BTN.clicked.connect(self.readDataContr)
            self.ui.stop_BTN.clicked.connect(self.model.stopRead)
            # self.win_write.write_value_btn.clicked.connect(self.initWriteVal)
            # self.win_write.cancel_value_btn.clicked.connect(self.clickedCancel)

        except Exception as e:
            print(str(e))

    # def clickedCancel(self):
    #     self.close()

    def initTable(self):
        try:
            self.ui.tableWidget.setColumnCount(2)
            self.ui.tableWidget.setRowCount(125)
            self.ui.tableWidget.setHorizontalHeaderLabels(['Register', 'DATA'])
            self.ui.tableWidget.setItem(0, 0, QTableWidgetItem('TIME_MSG'))
            self.ui.tableWidget.setItem(1, 0, QTableWidgetItem('SEL_D_HIMID'))
            self.ui.tableWidget.setItem(2, 0, QTableWidgetItem('SEL_D_SPEED'))
            self.ui.tableWidget.setItem(3, 0, QTableWidgetItem('SEL_DW_FORSE'))
            self.ui.tableWidget.setItem(4, 0, QTableWidgetItem('SEL_DWL_FORSE'))
            self.ui.tableWidget.setItem(5, 0, QTableWidgetItem('NUM_DW_FORSE'))
            self.ui.tableWidget.setItem(6, 0, QTableWidgetItem('NUM_DWL_FORSE'))
            self.ui.tableWidget.setItem(7, 0, QTableWidgetItem('ADR_DW_FORSE'))
            self.ui.tableWidget.setItem(8, 0, QTableWidgetItem('ADR_DWL_FORSE'))
            self.ui.tableWidget.setItem(9, 0, QTableWidgetItem('ADR_MS'))
            self.ui.tableWidget.setItem(10, 0, QTableWidgetItem('PER_DATCH'))
            self.ui.tableWidget.setItem(11, 0, QTableWidgetItem('PER_OBMEN'))
            self.ui.tableWidget.setItem(12, 0, QTableWidgetItem('SEL_TYPE_TRANS_A'))
            self.ui.tableWidget.setItem(13, 0, QTableWidgetItem('SEL_TYPE_TRANS_B'))
            self.ui.tableWidget.setItem(14, 0, QTableWidgetItem('NUM_MODEM'))

            self.ui.tableWidget.setItem(15, 0, QTableWidgetItem('ADR_DEV'))
            self.ui.tableWidget.setItem(16, 0, QTableWidgetItem('NUM_DEV'))
            self.ui.tableWidget.setItem(17, 0, QTableWidgetItem('PER_RSTSYST'))
            self.ui.tableWidget.setItem(18, 0, QTableWidgetItem('T_VLAGN'))
            self.ui.tableWidget.setItem(19, 0, QTableWidgetItem('VLAGN'))
            self.ui.tableWidget.setItem(20, 0, QTableWidgetItem('NAPR_VETR'))
            self.ui.tableWidget.setItem(21, 0, QTableWidgetItem('SCOR_VETR'))
            self.ui.tableWidget.setItem(22, 0, QTableWidgetItem('NAPR_PIT'))
            self.ui.tableWidget.setItem(23, 0, QTableWidgetItem('T_DS18S20'))
            self.ui.tableWidget.setItem(24, 0, QTableWidgetItem('STATUS_INT'))

            self.ui.tableWidget.cellClicked[int, int].connect(self.clickedRowColumn)

        except Exception as e:
            print('ERROR in init table')
            print(str(e))

    def readDataContr(self):
        self.model.startRead()

    def readNastrContr(self):
        self.model.startRead()

    def winWriteShow(self, text_lbl):
        try:
            self.model.flag_write = False
            self.model.stopRead()
            while not self.model.flag_write:
                self.model.startWrite(0, [5])

            self.model.startRead()

            # self.win_write.value_LE.clear()
            # self.win_write.show()
            # self.win_write.label.setText(text_lbl)
            # self.win_write.write_value_btn.clicked.connect(self.initWriteVal)

        except Exception as e:
            print(str(e))

    def initWriteVal(self):
        try:
            pass
            # # temp = self.win_write.value_LE.text()
            # if len(temp) > 0:
            #     # self.model.stopRead()
            #     temp_v = []
            #     temp_v.append(int(temp))
            #     self.model.writeValues(self.start_reg, temp_v)
            #     self.win_write.value_LE.clear()
            #     self.win_write.close()
            #     # self.model.startRead('nastr')
            #     # self.model.startRead('data')
            #
            # else:
            #     txt = 'НЕКОРРЕКТНОЕ ЗНАЧЕНИЕ'
            #     self.win_write.value_LE.setText(txt)

        except Exception as e:
            print(str(e))
            print('ERROR in initWriteVal')

    def viewTable(self, tag):
        try:
            self.ui.tableWidget.blockSignals(True)
            if tag == 'nastr':
                temp = self.model.set_cont.adr_dw_forse
                num_row = 25
                for i in range(0, self.model.set_cont.num_dw_forse * 2, 2):
                    self.ui.tableWidget.setItem(num_row + i, 0, QTableWidgetItem('F_{}_W'.format(temp)))
                    self.ui.tableWidget.setItem(num_row + 1 + i, 0, QTableWidgetItem('T_{}_W'.format(temp)))
                    temp += 1

                num_row = self.model.set_cont.num_dw_forse * 2 + 25
                temp = self.model.set_cont.adr_dwl_forse
                for i in range(0, self.model.set_cont.num_dwl_forse * 4, 4):
                    self.ui.tableWidget.setItem(num_row + i, 0, QTableWidgetItem('F_{}_WL'.format(temp)))
                    self.ui.tableWidget.setItem(num_row + 1 + i, 0, QTableWidgetItem('T_{}_WL'.format(temp)))
                    self.ui.tableWidget.setItem(num_row + 2 + i, 0, QTableWidgetItem('TP_{}_WL'.format(temp)))
                    self.ui.tableWidget.setItem(num_row + 3 + i, 0, QTableWidgetItem('U_{}_WL'.format(temp)))
                    temp += 1
                er_cod = 1
                self.ui.tableWidget.setItem(0, 1, QTableWidgetItem(str(self.model.data_cont.time_msg)))
                self.ui.tableWidget.setItem(1, 1, QTableWidgetItem(str(self.model.set_cont.sel_d_himid)))
                self.ui.tableWidget.setItem(2, 1, QTableWidgetItem(str(self.model.set_cont.sel_d_speed)))
                self.ui.tableWidget.setItem(3, 1, QTableWidgetItem(str(self.model.set_cont.sel_dw_forse)))
                self.ui.tableWidget.setItem(4, 1, QTableWidgetItem(str(self.model.set_cont.sel_dwl_forse)))
                er_cod = 2
                self.ui.tableWidget.setItem(5, 1, QTableWidgetItem(str(self.model.set_cont.num_dw_forse)))
                self.ui.tableWidget.setItem(6, 1, QTableWidgetItem(str(self.model.set_cont.num_dwl_forse)))
                self.ui.tableWidget.setItem(7, 1, QTableWidgetItem(str(self.model.set_cont.adr_dw_forse)))
                self.ui.tableWidget.setItem(8, 1, QTableWidgetItem(str(self.model.set_cont.adr_dwl_forse)))
                self.ui.tableWidget.setItem(9, 1, QTableWidgetItem(str(self.model.set_cont.adr_ms)))
                er_cod = 3
                self.ui.tableWidget.setItem(10, 1, QTableWidgetItem(str(self.model.set_cont.per_datch)))
                self.ui.tableWidget.setItem(11, 1, QTableWidgetItem(str(self.model.set_cont.per_obmen)))
                self.ui.tableWidget.setItem(12, 1, QTableWidgetItem(str(self.model.set_cont.sel_type_trans_a)))
                self.ui.tableWidget.setItem(13, 1, QTableWidgetItem(str(self.model.set_cont.sel_type_trans_b)))
                self.ui.tableWidget.setItem(14, 1, QTableWidgetItem(str(self.model.set_cont.num_modem)))
                er_cod = 4

            if tag == 'data':
                self.ui.tableWidget.setItem(15, 1, QTableWidgetItem(str(self.model.data_cont.adr_dev)))
                self.ui.tableWidget.setItem(16, 1, QTableWidgetItem(str(self.model.data_cont.num_dev)))
                self.ui.tableWidget.setItem(17, 1, QTableWidgetItem(str(self.model.data_cont.per_rstsyst)))
                er_cod = 5
                self.ui.tableWidget.setItem(18, 1, QTableWidgetItem(str(self.model.data_cont.t_vlagn)))
                self.ui.tableWidget.setItem(19, 1, QTableWidgetItem(str(self.model.data_cont.vlagn)))
                self.ui.tableWidget.setItem(20, 1, QTableWidgetItem(str(self.model.data_cont.napr_vetr)))
                self.ui.tableWidget.setItem(21, 1, QTableWidgetItem(str(self.model.data_cont.scor_vetr)))
                er_cod = 8
                self.ui.tableWidget.setItem(22, 1, QTableWidgetItem(str(self.model.data_cont.napr_pit)))
                self.ui.tableWidget.setItem(23, 1, QTableWidgetItem(str(self.model.data_cont.t_ds18s20)))
                self.ui.tableWidget.setItem(24, 1, QTableWidgetItem(str(self.model.data_cont.status_int)))
                er_cod = 9

                temp = 0
                num_row = 25
                for i in range(0, self.model.set_cont.num_dw_forse * 2, 2):
                    self.ui.tableWidget.setItem(num_row + i, 1, QTableWidgetItem(str(self.model.data_cont.f_w[temp])))
                    self.ui.tableWidget.setItem(num_row + 1 + i, 1, QTableWidgetItem(str(self.model.data_cont.t_w[temp])))
                    temp += 1
                er_cod = 6

                num_row = self.model.set_cont.num_dw_forse * 2 + 25
                temp = 1
                for i in range(0, self.model.set_cont.num_dwl_forse * 4, 4):
                    self.ui.tableWidget.setItem(num_row + i, 1, QTableWidgetItem(str(self.model.data_cont.f_wl[temp - 1])))
                    self.ui.tableWidget.setItem(num_row + 1 + i, 1, QTableWidgetItem(str(self.model.data_cont.t_wl[temp - 1])))
                    self.ui.tableWidget.setItem(num_row + 2 + i, 1, QTableWidgetItem(str(self.model.data_cont.tp_wl[temp - 1])))
                    self.ui.tableWidget.setItem(num_row + 3 + i, 1, QTableWidgetItem(str(self.model.data_cont.u_wl[temp - 1])))
                    temp += 1
                er_cod = 7

            self.ui.tableWidget.blockSignals(False)

        except Exception as e:
            print('ERROR in view table in er_code = {}'.format(er_cod))
            print(str(e))

    def clickedRowColumn(self, r, c):
        try:
            tag = ''
            if c == 1:
                if r == 1:
                    tag = 'SEL_D_HIMID'
                    self.start_reg = 8194
                if r == 2:
                    tag = 'SEL_D_SPEED'
                    self.start_reg = 8195
                if r == 3:
                    tag = 'SEL_DW_FORSE'
                    self.start_reg = 8196
                if r == 4:
                    tag = 'SEL_DWL_FORSE'
                    self.start_reg = 8197
                if r == 5:
                    tag = 'NUM_DW_FORSE'
                    self.start_reg = 8198
                if r == 6:
                    tag = 'NUM_DWL_FORSE'
                    self.start_reg = 8199
                if r == 7:
                    tag = 'ADR_DW_FORSE'
                    self.start_reg = 8200
                if r == 8:
                    tag = 'ADR_DWL_FORSE'
                    self.start_reg = 8201
                if r == 9:
                    tag = 'ADR_MS'
                    self.start_reg = 8202
                if r == 10:
                    tag = 'PER_DATCH'
                    self.start_reg = 8203
                if r == 11:
                    tag = 'PER_OBMEN'
                    self.start_reg = 8204
                if r == 12:
                    tag = 'SEL_TYPE_TRANS_A'
                    self.start_reg = 8205
                if r == 13:
                    tag = 'SEL_TYPE_TRANS_B'
                    self.start_reg = 8206
                if r == 14:
                    tag = 'NUM_MODEM'
                    self.start_reg = 8207
                if r == 16:
                    tag = 'NUM_DEV'
                    self.start_reg = 1
                if r == 17:
                    tag = 'PER_RSTSYST'
                    self.start_reg = 4
                self.winWriteShow(tag)
            else:
                pass

        except Exception as e:
            print('ERROR in clickedRowColumn')
            print(str(e))
