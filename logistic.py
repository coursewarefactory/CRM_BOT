# -*- coding: utf-8 -*-
#! /usr/bin/env python 

import sqlite3
import datetime
import random
import config
import g_utilities


def accepted(user_id, name_of_receiver, city_of_receiver):
    ''' заполнить 7 строк таблицы:

 трек_номер(Id) | город отправителя | дата и время отправления | имя получателя | город получателя | дата доставки | ссылка на фото 

    имя получателя, город получателя - передаеются напрямую
    дата доставки, ссылка на фото  - всегда 'ожидаются'
    Track ID -  генерируем
    город отправителя - берется из базы курьеров
    дата и время отпрвления - через datetime     '''

    conn = sqlite3.connect("logistic.db") # подключаемся к базе
    cursor = conn.cursor()
    table_name = 'logistic_table_2'
    request = "SELECT rowid, * FROM {0} ORDER BY Track_ID"  # создаем запрос на список ID
    request = request.format(table_name)
    res = [] 
    for row in cursor.execute(request):   # создаем массив ID
        res.append(row[1])    
    
    Track_ID = random.randint(100000,999999)# получили данные для 1го столбца
    Track_ID = str(Track_ID)
    while Track_ID in res: # проверяем чтобы сгенерированный трек номер не совпадал с номерами из столбца с треками      
        Track_ID = random.randint(100000,999999)
        Track_ID = str(Track_ID)
        
    city_of_sender = config.couriers[user_id] # получили данные для 2го столбца

    time = datetime.datetime.now()            
    date_time_of_acceptance=str(time)
    date_time_of_acceptance=date_time_of_acceptance[:-10] # получили данные для 3го столбца         
    date_time_of_delivery = 'ожидается'
    link_photo = 'ожидается'
    new_information = [(Track_ID, city_of_sender, date_time_of_acceptance, name_of_receiver, city_of_receiver, date_time_of_delivery, link_photo)]
    cursor.executemany("INSERT INTO logistic_table_2 VALUES (?,?,?,?,?,?,?)", new_information) # добавляем запись в базу SQL lite
    conn.commit()    

    g_utilities.connect_to_sheets() # подключаемся к таблице google
    start_2='A1' # указываем значение начальной ячейки            
    finish_2 = 'A1000'# указываем значение конечной ячейки
    res = g_utilities.get_cell_range(start_2, finish_2) # получаем массив значений ключей (длина массива равна количеству непсутых строк)
    value = str(len(res) + 1) # определяем номер следующей свободной строки для записи
    # записываем данные в таблицу google
    coordinate = 'A' + value # задаем координату 1го столбца
    g_utilities.write_cell_value(coordinate, Track_ID) # записываем Track_ID в 1й столбец
    coordinate = 'B' + value # задаем координату 2го столбца
    g_utilities.write_cell_value(coordinate, city_of_sender) # записываем город ОТПРАВИТЕЛЯ во 2й столбец        
    coordinate = 'C' + value # задаем координату 3го столбца
    g_utilities.write_cell_value(coordinate, date_time_of_acceptance) # записываем время отправления в 3й столбец
    coordinate = 'D' + value # задаем координату 4го столбца
    g_utilities.write_cell_value(coordinate, name_of_receiver) # записываем имя получателя в 4й столбец
    coordinate = 'E' + value # задаем координату 5го столбца
    g_utilities.write_cell_value(coordinate, city_of_receiver) # записываем город ПОЛУЧАТЕЛЯ во 5й столбец
    coordinate = 'F' + value # задаем координату 6го столбца
    g_utilities.write_cell_value(coordinate, 'ожидается') # записываем время доставки во 6й столбец
    coordinate = 'G' + value # задаем координату 7го столбца
    g_utilities.write_cell_value(coordinate, 'ожидается') # записываем ссылку на фото в 7й столбец
    report = 'Запись добавлена! Не забудьте сообщить курьеру из {0} трек: {1}. Нажмите /Start чтобы продолжить' # формулируем сообщение о добавлении записи
    report = report.format(city_of_receiver, Track_ID)
    return report #  возвращаем сообщение
    
#accepted('156185969', 'stetem', 'Miami')

def delivered(user_id, track_number, link_photo):
    """Назначение функции: внести актуальные данные в столбцы 6(дата доставки) и 7(ссылка на фото) базы данных
       и вывести эти данные в таблицу Google.
       На входе функция получает ID пользователя, трек номер и ссылку на фото. Далее проводятся 2 проверки.
       1. Функция проверяет наличие трека в базе. Если трек номер не обнаружен в списке функция возвращает сообщение
       о том что введен неправильный трек. Если трек номер есть в списке - переходим ко второй проверке.
       2. По указаному трек номеру находим город получателя в базе. Создаем запрос на город курьера из файла конфигурации.
       Если города не совпадают функция возвращает соответствующее сообщение об ошибке. Если города совпадают вносим время доставки в базу
       """

    print('вызвана функция Delivered')
    conn = sqlite3.connect("logistic.db") # подключаемся к базе
    cursor = conn.cursor()
    table_name = 'logistic_table_2'
    request = "SELECT rowid, * FROM {0} ORDER BY Track_ID"  # создаем запрос на список ID
    request = request.format(table_name)
    res = []
    print('вызвана функция Delivered')
    for row in cursor.execute(request):   # создаем массив ID
        res.append(row[1])

    print (res)
    if track_number not in res:   # проверяем есть ли трек, введенный вторым курьером, в базе
        print('Вы ввели неправильный трек(ТРЕКА НЕТ В БАЗЕ). Повторите попытку')
        report = 'Вы ввели неправильный трек. Повторите попытку'
        return report

    track_number_sql = '"' + track_number + '"'
    sql = "SELECT city_of_receiver FROM logistic_table_2 WHERE Track_ID={0}"
    sql= sql.format(track_number_sql)
    cursor.execute(sql)
    city_of_receiver = cursor.fetchall()
    print ('city_of_receiver #0:', city_of_receiver)
    city_of_receiver =str(city_of_receiver[0][0])
    print (city_of_receiver)
    
    city_of_courier = config.couriers[user_id] # создаем запрос на город курьера из конфига
    print (city_of_courier)
    if city_of_receiver != city_of_courier:    # сравниваем города (город получателя и город курьера должны совпадать). если все ок - заносим время доставки и ссылку на фото в базу
        print('Вы ввели неправильный трек(НЕВЕРНЫй ГОРОД). Повторите попытку')
        report = 'Вы ввели трек для ДРУГОГО города. Повторите попытку'
        return report

    time = datetime.datetime.now()            
    date_time_of_delivery=str(time)
    date_time_of_delivery=date_time_of_delivery[:-10] # задаем время и дату доставки

    print(date_time_of_delivery) 
    date_time_of_delivery = '"' + date_time_of_delivery + '"' # приводим к необходимому формату для SQLlite запроса
    #track_number = '"' + track_number + '"' # приводим к необходимому фомрмату для SQLlite запроса    
    print('дата добавлена')

    #в данной части добавляем время доставки в базу
    sql = """
    UPDATE logistic_table_2     
    SET date_time_of_delivery = {0} 
    WHERE Track_ID = {1}""" #  формулируем запрос   
    sql= sql.format(date_time_of_delivery, track_number_sql) # форматируем запрос
    cursor.execute(sql)
    conn.commit()         # запускаем запрос

    #в данной части добавляем линк на фото в базу

    link_photo = '"' + link_photo + '"'
    sql = """
    UPDATE logistic_table_2     
    SET link_photo={0} 
    WHERE Track_ID={1} """ #  формулируем запрос   
    sql= sql.format(link_photo, track_number_sql) # форматируем запрос
    cursor.execute(sql)
    conn.commit()         # запускаем запрос

    print ('данные добавлены')

    g_utilities.connect_to_sheets() # подключаемся к таблице Google

    start_1 = 'A1'
    finish_1 = 'A1000'
    res = g_utilities.get_cell_range(start_1, finish_1) # получаем массив значений Track_ID
    row_number = res.index(track_number) + 1       # находим номер строки где находится Track_ID

    print(row_number)
    
    coordinate = 'F' + str(row_number) # определяем координату ячейки для записи
    g_utilities.write_cell_value(coordinate, date_time_of_delivery) # записываем время доставки во 6й столбец

    coordinate = 'G' + str(row_number)
    g_utilities.write_cell_value(coordinate, link_photo) # записываем ссылку на фото в 7й столбец

    print ('данные добавлены')

    report = 'Запись добавлена. Нажмите /Start чтобы продолжить'
    return report


#delivered('156185969', '782684', 'photos/file_20.jpg')
