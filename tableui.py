from PyQt5.QtWidgets import QTableWidgetItem


class TableView:
    def initTableBasic(self, table_obj, data):
        try:
            table_obj.setColumnCount(2)
            table_obj.setRowCount(12)
            table_obj.setHorizontalHeaderLabels(['Наименование', 'Значение'])
            table_obj.setItem(0, 0, QTableWidgetItem('Время посылки'))
            table_obj.setItem(1, 0, QTableWidgetItem('Тип датчика\nвлажности'))
            table_obj.setItem(2, 0, QTableWidgetItem('Тип датчика\nветра'))
            table_obj.setItem(3, 0, QTableWidgetItem('Тип проводного\nдатчика усилия'))
            table_obj.setItem(4, 0, QTableWidgetItem('Тип беспроводного\nдатчика усилия'))
            table_obj.setItem(5, 0, QTableWidgetItem('Количество\nпроводных датчиков'))
            table_obj.setItem(6, 0, QTableWidgetItem('количество\nбеспровоных датчиков'))
            table_obj.setItem(7, 0, QTableWidgetItem('Начальный адрес\nпроводных датчиков'))
            table_obj.setItem(8, 0, QTableWidgetItem('Начальный адрес\nбеспроводных датчиков'))
            table_obj.setItem(9, 0, QTableWidgetItem('Адрес контроллера\nметеостанции'))
            table_obj.setItem(10, 0, QTableWidgetItem('Период опроса\nдатчиков, сек'))
            table_obj.setItem(11, 0, QTableWidgetItem('Период сеанса связи\nпункта наблюдения, сек'))

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
            table_obj.setRowCount(42)
            table_obj.setHorizontalHeaderLabels(['Наименование', 'Значение,\nВес, кг', 'Темература\nдатчика, ℃',
                                                 'Температура\nпровода, ℃', 'Напряжение, В'])
            table_obj.setItem(0, 0, QTableWidgetItem('Время посылки'))
            table_obj.setItem(1, 0, QTableWidgetItem('Номер контроллера'))
            table_obj.setItem(2, 0, QTableWidgetItem('Программный сброс, мин'))
            table_obj.setItem(3, 0, QTableWidgetItem('Температура с датчика\nвлажности, ℃'))
            table_obj.setItem(4, 0, QTableWidgetItem('Влажность с датчика\nвлажности, %'))
            table_obj.setItem(5, 0, QTableWidgetItem('Угол направления\nветра, град'))
            table_obj.setItem(6, 0, QTableWidgetItem('Скорость ветра, м/сек'))
            table_obj.setItem(7, 0, QTableWidgetItem('Напряжение питания, В'))
            table_obj.setItem(8, 0, QTableWidgetItem('Значение внешнего\nтермометра DS18S20, ℃'))
            table_obj.setItem(9, 0, QTableWidgetItem('Концевик шкафа'))
            table_obj.setItem(10, 0, QTableWidgetItem('Проводные датчики'))
            num_row = 11
            for i in range(num_dw):
                table_obj.setItem(num_row, 0, QTableWidgetItem('Датчик №{}'.format(adr_dw + i)))
                num_row += 1

            table_obj.setItem(num_row, 0, QTableWidgetItem('Беспроводные датчики'))
            for i in range(num_dwl):
                table_obj.setItem(num_row + 1, 0, QTableWidgetItem('Датчик №{}'.format(adr_dwl + i)))
                num_row += 1

            table_obj.setItem(0, 1, QTableWidgetItem(data.time_msg))
            table_obj.setItem(1, 1, QTableWidgetItem(data.num_dev))
            table_obj.setItem(2, 1, QTableWidgetItem(data.per_rstsyst))
            table_obj.setItem(3, 1, QTableWidgetItem(data.t_vlagn))
            table_obj.setItem(4, 1, QTableWidgetItem(data.vlagn))
            table_obj.setItem(5, 1, QTableWidgetItem(data.napr_vetr))
            table_obj.setItem(6, 1, QTableWidgetItem(data.scor_vetr))
            table_obj.setItem(7, 1, QTableWidgetItem(data.napr_pit))
            table_obj.setItem(8, 1, QTableWidgetItem(data.t_ds18s20))
            table_obj.setItem(9, 1, QTableWidgetItem(data.status_int))

            num_row = 11
            for i in range(num_dw):
                table_obj.setItem(num_row, 1, QTableWidgetItem(data.f_w[i]))
                table_obj.setItem(num_row, 2, QTableWidgetItem(data.t_w[i]))
                num_row += 1

            for i in range(num_dwl):
                table_obj.setItem(num_row + 1, 1, QTableWidgetItem(data.f_wl[i]))
                table_obj.setItem(num_row + 1, 2, QTableWidgetItem(data.t_wl[i]))
                table_obj.setItem(num_row + 1, 3, QTableWidgetItem(data.tp_wl[i]))
                table_obj.setItem(num_row + 1, 4, QTableWidgetItem(data.u_wl[i]))
                num_row += 1

        except Exception as e:
            print('ERROR in init table data')
            print(str(e))

    def initTableConnect(self, table_obj, data):
        try:
            table_obj.setColumnCount(2)
            table_obj.setRowCount(20)
            table_obj.setHorizontalHeaderLabels(['Наименование', 'Значение'])
            table_obj.setItem(0, 0, QTableWidgetItem('Время посылки'))
            table_obj.setItem(1, 0, QTableWidgetItem('Тип передачи\nпервого модема'))
            table_obj.setItem(2, 0, QTableWidgetItem('Тип передачи\nвторого модема'))
            table_obj.setItem(3, 0, QTableWidgetItem('Количество модемов'))
            table_obj.setItem(4, 0, QTableWidgetItem('Отслеживание\nпревышения усилия'))
            table_obj.setItem(5, 0, QTableWidgetItem('Период передачи GPRS\nв нормальных условиях, мин'))
            table_obj.setItem(6, 0, QTableWidgetItem('Статический IP адрес\nпервого модема'))
            table_obj.setItem(7, 0, QTableWidgetItem('Статический IP адрес\nвторого модема'))
            table_obj.setItem(8, 0, QTableWidgetItem('Статический IP адрес\nПСД'))
            table_obj.setItem(9, 0, QTableWidgetItem('Номер порта\nпервого модема'))
            table_obj.setItem(10, 0, QTableWidgetItem('Номер порта\nвторого модема'))
            table_obj.setItem(11, 0, QTableWidgetItem('Номер порта\nдля GPRS связи'))
            table_obj.setItem(12, 0, QTableWidgetItem('Основной номер телефона\nпервого модема'))
            table_obj.setItem(13, 0, QTableWidgetItem('Основной номер телефона\nвторого модема'))
            table_obj.setItem(14, 0, QTableWidgetItem('Логин первого модема'))
            table_obj.setItem(15, 0, QTableWidgetItem('Логин второго модема'))
            table_obj.setItem(16, 0, QTableWidgetItem('Пароль первого модема'))
            table_obj.setItem(17, 0, QTableWidgetItem('Пароль второго модема'))
            table_obj.setItem(18, 0, QTableWidgetItem('APN первого модема'))
            table_obj.setItem(19, 0, QTableWidgetItem('APN второго модема'))

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
            table_obj.setRowCount(33)
            table_obj.setHorizontalHeaderLabels(['Датчик', 'Пороговый вес, кг'])
            table_obj.setItem(0, 0, QTableWidgetItem('Время посылки'))
            table_obj.setItem(1, 0, QTableWidgetItem('Проводные датчики'))
            num_row = 2
            for i in range(num_dw):
                table_obj.setItem(num_row, 0, QTableWidgetItem('Датчик №{}'.format(adr_dw + i)))
                num_row += 1
            table_obj.setItem(num_row, 0, QTableWidgetItem('Беспроводные датчики'))
            for i in range(num_dwl):
                table_obj.setItem(num_row + 1, 0, QTableWidgetItem('Датчик №{}'.format(adr_dwl + i)))
                num_row += 1

            table_obj.setItem(0, 1, QTableWidgetItem(data.time_msg))
            num_row = 2
            for i in range(num_dw):
                table_obj.setItem(num_row, 1, QTableWidgetItem(data.f_w_max[i]))
                num_row += 1
            for i in range(num_dwl):
                table_obj.setItem(num_row + 1, 1, QTableWidgetItem(data.f_wl_max[i]))
                num_row += 1

        except Exception as e:
            print('ERROR in init table threshold')
            print(str(e))
