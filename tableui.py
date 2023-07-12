from PyQt5.QtWidgets import QTableWidgetItem


class TableView:
    def initTableBasic(self, table_obj, data):
        try:
            table_obj.setColumnCount(2)
            table_obj.setRowCount(12)
            table_obj.setHorizontalHeaderLabels(['Register', 'DATA'])
            table_obj.setItem(0, 0, QTableWidgetItem('TIME_MSG'))
            table_obj.setItem(1, 0, QTableWidgetItem('SEL_D_HIMID'))
            table_obj.setItem(2, 0, QTableWidgetItem('SEL_D_SPEED'))
            table_obj.setItem(3, 0, QTableWidgetItem('SEL_DW_FORSE'))
            table_obj.setItem(4, 0, QTableWidgetItem('SEL_DWL_FORSE'))
            table_obj.setItem(5, 0, QTableWidgetItem('NUM_DW_FORSE'))
            table_obj.setItem(6, 0, QTableWidgetItem('NUM_DWL_FORSE'))
            table_obj.setItem(7, 0, QTableWidgetItem('ADR_DW_FORSE'))
            table_obj.setItem(8, 0, QTableWidgetItem('ADR_DWL_FORSE'))
            table_obj.setItem(9, 0, QTableWidgetItem('ADR_MS'))
            table_obj.setItem(10, 0, QTableWidgetItem('PER_DATCH'))
            table_obj.setItem(11, 0, QTableWidgetItem('PER_OBMEN'))

            table_obj.setItem(0, 1, QTableWidgetItem(data.time_msg))
            table_obj.setItem(1, 1, QTableWidgetItem(data.sel_d_himid))
            table_obj.setItem(2, 1, QTableWidgetItem(data.sel_d_speed))
            table_obj.setItem(3, 1, QTableWidgetItem(data.sel_dw_forse))
            table_obj.setItem(4, 1, QTableWidgetItem(data.sel_dwl_forse))
            table_obj.setItem(5, 1, QTableWidgetItem(data.num_dw_forse))
            table_obj.setItem(6, 1, QTableWidgetItem(data.num_dwl_forse))
            table_obj.setItem(7, 1, QTableWidgetItem(data.adr_dw_forse))
            table_obj.setItem(8, 1, QTableWidgetItem(data.adr_dwl_forse))
            table_obj.setItem(9, 1, QTableWidgetItem(data.adr_ms))
            table_obj.setItem(10, 1, QTableWidgetItem(data.per_datch))
            table_obj.setItem(11, 1, QTableWidgetItem(data.per_obmen))

        except Exception as e:
            print('ERROR in init table basic')
            print(str(e))

    def initTableData(self, table_obj, num_dw, adr_dw, num_dwl, adr_dwl, data):
        try:
            table_obj.setColumnCount(5)
            table_obj.setRowCount(41)
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

            table_obj.setItem(0, 1, QTableWidgetItem(data.time_msg))
            table_obj.setItem(1, 1, QTableWidgetItem(data.adr_dev))
            table_obj.setItem(2, 1, QTableWidgetItem(data.num_dev))
            table_obj.setItem(3, 1, QTableWidgetItem(data.per_rstsyst))
            table_obj.setItem(4, 1, QTableWidgetItem(data.t_vlagn))
            table_obj.setItem(5, 1, QTableWidgetItem(data.vlagn))
            table_obj.setItem(6, 1, QTableWidgetItem(data.napr_vetr))
            table_obj.setItem(7, 1, QTableWidgetItem(data.scor_vetr))
            table_obj.setItem(8, 1, QTableWidgetItem(data.napr_pit))
            table_obj.setItem(9, 1, QTableWidgetItem(data.t_ds18s20))
            table_obj.setItem(10, 1, QTableWidgetItem(data.status_int))

            num_row = 11
            for i in range(num_dw):
                table_obj.setItem(num_row, 1, QTableWidgetItem(data.f_w[i]))
                table_obj.setItem(num_row, 2, QTableWidgetItem(data.t_w[i]))
                num_row += 1

            for i in range(num_dwl):
                table_obj.setItem(num_row, 1, QTableWidgetItem(data.f_wl[i]))
                table_obj.setItem(num_row, 2, QTableWidgetItem(data.t_wl[i]))
                table_obj.setItem(num_row, 3, QTableWidgetItem(data.tp_wl[i]))
                table_obj.setItem(num_row, 4, QTableWidgetItem(data.u_wl[i]))
                num_row += 1

        except Exception as e:
            print('ERROR in init table data')
            print(str(e))

    def initTableConnect(self, table_obj, data):
        try:
            table_obj.setColumnCount(2)
            table_obj.setRowCount(20)
            table_obj.setItem(0, 0, QTableWidgetItem('TIME_MSG'))
            table_obj.setItem(1, 0, QTableWidgetItem('SEL_TYPE_TRANS_A'))
            table_obj.setItem(2, 0, QTableWidgetItem('SEL_TYPE_TRANS_B'))
            table_obj.setItem(3, 0, QTableWidgetItem('NUM_MODEM'))
            table_obj.setItem(4, 0, QTableWidgetItem('FORSE_EN'))
            table_obj.setItem(5, 0, QTableWidgetItem('GPRS_PER_NORM'))
            table_obj.setItem(6, 0, QTableWidgetItem('ADR_IP_MODEM_A'))
            table_obj.setItem(7, 0, QTableWidgetItem('ADR_IP_MODEM_B'))
            table_obj.setItem(8, 0, QTableWidgetItem('ADR_IP_PSD'))
            table_obj.setItem(9, 0, QTableWidgetItem('NUM_PORT_MODEM_A'))
            table_obj.setItem(10, 0, QTableWidgetItem('NUM_PORT_MODEM_B'))
            table_obj.setItem(11, 0, QTableWidgetItem('NUM_PORT_PSD'))
            table_obj.setItem(12, 0, QTableWidgetItem('NUM_TEL_A'))
            table_obj.setItem(13, 0, QTableWidgetItem('NUM_TEL_B'))
            table_obj.setItem(14, 0, QTableWidgetItem('LOGIN_MODEM_A'))
            table_obj.setItem(15, 0, QTableWidgetItem('LOGIN_MODEM_B'))
            table_obj.setItem(16, 0, QTableWidgetItem('PAROLE_MODEM_A'))
            table_obj.setItem(17, 0, QTableWidgetItem('PAROLE_MODEM_B'))
            table_obj.setItem(18, 0, QTableWidgetItem('APN_MODEM_A'))
            table_obj.setItem(19, 0, QTableWidgetItem('APN_MODEM_B'))

            table_obj.setItem(0, 1, QTableWidgetItem(data.time_msg))
            table_obj.setItem(1, 1, QTableWidgetItem(data.sel_type_trans_a))
            table_obj.setItem(2, 1, QTableWidgetItem(data.sel_type_trans_b))
            table_obj.setItem(3, 1, QTableWidgetItem(data.num_modem))
            table_obj.setItem(4, 1, QTableWidgetItem(data.forse_en))
            table_obj.setItem(5, 1, QTableWidgetItem(data.gprs_per_norm))
            table_obj.setItem(6, 1, QTableWidgetItem(data.adr_ip_modem_a))
            table_obj.setItem(7, 1, QTableWidgetItem(data.adr_ip_modem_b))
            table_obj.setItem(8, 1, QTableWidgetItem(data.adr_ip_psd))
            table_obj.setItem(9, 1, QTableWidgetItem(data.num_port_modem_a))
            table_obj.setItem(10, 1, QTableWidgetItem(data.num_port_modem_b))
            table_obj.setItem(11, 1, QTableWidgetItem(data.num_port_psd))
            table_obj.setItem(12, 1, QTableWidgetItem(data.num_tel_a))
            table_obj.setItem(13, 1, QTableWidgetItem(data.num_tel_b))
            table_obj.setItem(14, 1, QTableWidgetItem(data.login_modem_a))
            table_obj.setItem(15, 1, QTableWidgetItem(data.login_modem_b))
            table_obj.setItem(16, 1, QTableWidgetItem(data.parole_modem_a))
            table_obj.setItem(17, 1, QTableWidgetItem(data.parole_modem_b))
            table_obj.setItem(18, 1, QTableWidgetItem(data.apn_modem_a))
            table_obj.setItem(19, 1, QTableWidgetItem(data.apn_modem_b))

        except Exception as e:
            print('ERROR in init table connect')
            print(str(e))

    def initTableThreshold(self, table_obj, num_dw, adr_dw, num_dwl, adr_dwl, data):
        try:
            table_obj.setColumnCount(2)
            table_obj.setRowCount(31)
            table_obj.setItem(0, 0, QTableWidgetItem('TIME_MSG'))
            num_row = 1
            for i in range(num_dw):
                table_obj.setItem(i + 1, 0, QTableWidgetItem('F_{}_W_Max'.format(adr_dw + i)))
                num_row += 1
            for i in range(num_dwl):
                table_obj.setItem(i + num_row, 0, QTableWidgetItem('F_{}_WL_Max'.format(adr_dwl + i)))

            table_obj.setItem(0, 1, QTableWidgetItem(data.time_msg))
            num_row = 1
            for i in range(num_dw):
                table_obj.setItem(i + 1, 1, QTableWidgetItem(data.f_w_max[i]))
                num_row += 1
            for i in range(num_dwl):
                table_obj.setItem(i + num_row, 1, QTableWidgetItem(data.f_wl_max[i]))

        except Exception as e:
            print('ERROR in init table threshold')
            print(str(e))
