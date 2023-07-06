from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem


class TableView:
    def initTableBasic(self, table_obj):
        try:
            table_obj.setColumnCount(2)
            table_obj.setRowCount(11)
            table_obj.setHorizontalHeaderLabels(['Register', 'DATA'])
            table_obj.setItem(0, 0, QTableWidgetItem('SEL_D_HIMID'))
            table_obj.setItem(1, 0, QTableWidgetItem('SEL_D_SPEED'))
            table_obj.setItem(2, 0, QTableWidgetItem('SEL_DW_FORSE'))
            table_obj.setItem(3, 0, QTableWidgetItem('SEL_DWL_FORSE'))
            table_obj.setItem(4, 0, QTableWidgetItem('NUM_DW_FORSE'))
            table_obj.setItem(5, 0, QTableWidgetItem('NUM_DWL_FORSE'))
            table_obj.setItem(6, 0, QTableWidgetItem('ADR_DW_FORSE'))
            table_obj.setItem(7, 0, QTableWidgetItem('ADR_DWL_FORSE'))
            table_obj.setItem(8, 0, QTableWidgetItem('ADR_MS'))
            table_obj.setItem(9, 0, QTableWidgetItem('PER_DATCH'))
            table_obj.setItem(10, 0, QTableWidgetItem('PER_OBMEN'))

        except Exception as e:
            print('ERROR in init table basic')
            print(str(e))

    def initTableData(self, table_obj, num_dw, adr_dw, num_dwl, adr_dwl):
        try:
            table_obj.setColumnCount(5)
            table_obj.setRowCount(31)
            table_obj.setHorizontalHeaderLabels(['Register', 'DATA', 'DATA', 'DATA', 'DATA'])
            table_obj.setItem(0, 0, QTableWidgetItem('TIME_MSG'))
            table_obj.setItem(1, 0, QTableWidgetItem('ADR_DEV'))
            table_obj.setItem(2, 0, QTableWidgetItem('NUM_DEV'))
            table_obj.setItem(3, 0, QTableWidgetItem('PER_RSTSYST'))
            table_obj.setItem(4, 0, QTableWidgetItem('T_VLAGN'))
            table_obj.setItem(5, 0, QTableWidgetItem('VLAGN'))
            table_obj.setItem(6, 0, QTableWidgetItem('NAPR_VETR'))
            table_obj.setItem(7, 0, QTableWidgetItem('SCOR_VETR'))
            table_obj.setItem(8, 0, QTableWidgetItem('NAPR_PIT'))
            table_obj.setItem(9, 0, QTableWidgetItem('T_DS18S20'))
            table_obj.setItem(10, 0, QTableWidgetItem('STATUS_INT'))

            num_row = 11
            for i in range(num_dw):
                table_obj.setItem(num_row, 0, QTableWidgetItem('F & T {}_W'.format(adr_dw + i)))
                num_row += 1

            for i in range(num_dwl):
                table_obj.setItem(num_row, 0, QTableWidgetItem('F & T & TP & U {}_WL'.format(adr_dwl + i)))
                num_row += 1

        except Exception as e:
            print('ERROR in init table data')
            print(str(e))

    def initTableConnect(self, table_obj):
        try:
            table_obj.setColumnCount(2)
            table_obj.setRowCount(19)
            table_obj.setItem(0, 0, QTableWidgetItem('SEL_TYPE_TRANS_A'))
            table_obj.setItem(1, 0, QTableWidgetItem('SEL_TYPE_TRANS_B'))
            table_obj.setItem(2, 0, QTableWidgetItem('NUM_MODEM'))
            table_obj.setItem(3, 0, QTableWidgetItem('FORSE_EN'))
            table_obj.setItem(4, 0, QTableWidgetItem('GPRS_PER_NORM'))
            table_obj.setItem(5, 0, QTableWidgetItem('ADR_IP_MODEM_A'))
            table_obj.setItem(6, 0, QTableWidgetItem('ADR_IP_MODEM_B'))
            table_obj.setItem(7, 0, QTableWidgetItem('ADR_IP_PSD'))
            table_obj.setItem(8, 0, QTableWidgetItem('NUM_PORT_MODEM_A'))
            table_obj.setItem(9, 0, QTableWidgetItem('NUM_PORT_MODEM_B'))
            table_obj.setItem(10, 0, QTableWidgetItem('NUM_PORT_PSD'))
            table_obj.setItem(11, 0, QTableWidgetItem('NUM_TEL_A'))
            table_obj.setItem(12, 0, QTableWidgetItem('NUM_TEL_B'))
            table_obj.setItem(13, 0, QTableWidgetItem('LOGIN_MODEM_A'))
            table_obj.setItem(14, 0, QTableWidgetItem('LOGIN_MODEM_B'))
            table_obj.setItem(15, 0, QTableWidgetItem('PAROLE_MODEM_A'))
            table_obj.setItem(16, 0, QTableWidgetItem('PAROLE_MODEM_B'))
            table_obj.setItem(17, 0, QTableWidgetItem('APN_MODEM_A'))
            table_obj.setItem(18, 0, QTableWidgetItem('APN_MODEM_B'))

        except Exception as e:
            print('ERROR in init table connect')
            print(str(e))

    def initTableThreshold(self, table_obj, num_dw, adr_dw, num_dwl, adr_dwl):
        try:
            table_obj.setColumnCount(2)
            table_obj.setRowCount(30)
            num_row = 0
            for i in range(num_dw):
                table_obj.setItem(i, 0, QTableWidgetItem('F_{}_W_Max'.format(adr_dw + i)))
                num_row += 1
            for i in range(num_dwl):
                table_obj.setItem(i + num_row, 0, QTableWidgetItem('F_{}_WL_Max'.format(adr_dwl + i)))

        except Exception as e:
            print('ERROR in init table threshold')
            print(str(e))
