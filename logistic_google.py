import sqlite3
import datetime
import random
import config
import g_utilities

def accepted(user_id, name_of_receiver, city_of_receiver):
    '''Цель функции заполнить 7 строк таблицы:

 трек_номер(Id) | город отправителя | дата и время отправления | имя получателя | город получателя | дата доставки | ссылка на фото 

    имя получателя, город получателя - передаеются напрямую
    дата доставки, ссылка на фото  - всегда 'ожидаются'
    Track ID -  генерируем
    город отправителя - берется из базы курьеров
    дата и время отпрвления - через datetime     '''

    g_utilities.connect_to_sheets()           # подключаемся к базе
    start_1='A1'
    finish_1 = 'A1000'
    res = g_utilities.get_cell_range(start_1, finish_1) # получаем массив значений Track_ID

    Track_ID = random.randint(100000,999999)  # получили данные для 1го столбца
    Track_ID = str(Track_ID)
    while Track_ID in res:
        Track_ID = random.randint(100000,999999)
        Track_ID = str(Track_ID)
        
    city_of_sender = config.couriers[user_id] # получили данные для 2го столбца

    time = datetime.datetime.now()            
    date_time_of_acceptance=str(time)
    date_time_of_acceptance=date_time_of_acceptance[:-10] # получили данные для 3го столбца
             
    date_time_of_delivery = 'ожидается' # получили данные для 4го столбца
    link_photo = 'ожидается' # получили данные для 5го столбца

    start_2='A1'
    finish_2 = 'A1000'
    res = g_utilities.get_cell_range(start_2, finish_2) # получаем массив значений ключей
    value = len(res) + 1 # определяем номер следующей свободной строки для записи
    value = str(value)

    # записываем данные в таблицу

    coordinate = 'A' + value
    g_utilities.write_cell_value(coordinate, Track_ID) # записываем Track_ID в 1й столбец

    coordinate = 'B' + value
    g_utilities.write_cell_value(coordinate, city_of_sender) # записываем город ОТПРАВИТЕЛЯ во 2й столбец        

    coordinate = 'C' + value
    g_utilities.write_cell_value(coordinate, date_time_of_acceptance) # записываем время отправления в 3й столбец
    
    coordinate = 'D' + value
    g_utilities.write_cell_value(coordinate, name_of_receiver) # записываем имя получателя в 4й столбец
    
    coordinate = 'E' + value
    g_utilities.write_cell_value(coordinate, city_of_receiver) # записываем город ПОЛУЧАТЕЛЯ во 5й столбец

    coordinate = 'F' + value
    g_utilities.write_cell_value(coordinate, 'ожидается') # записываем время доставки во 6й столбец

    coordinate = 'G' + value
    g_utilities.write_cell_value(coordinate, 'ожидается') # записываем ссылку на фото в 7й столбец
    
    
    print('Track_ID: ', Track_ID)
    print('city_of_sender: ', city_of_sender)
    print('date_time_of_acceptance: ', date_time_of_acceptance)

    report = 'Запись добавлена! Не забудьте сообщить курьеру из {0} трек: {1}. Нажмите /Start чтобы продолжить'
    report = report.format(city_of_receiver, Track_ID)
    return report
    

#accepted('156185969', 'Steve Austin', 'Miami')

def delevered(user_id, track_number, link_photo):
    

    g_utilities.connect_to_sheets() # подключаемся к базе

    start_1 = 'A1'
    finish_1 = 'A1000'
    res = g_utilities.get_cell_range(start_1, finish_1) # получаем массив значений Track_ID
    if track_number not in res:                         # проверяем есть ли трек, введенный вторым курьером, в базе
        print('Вы ввели неправильный трек(ТРЕКА НЕТ В БАЗЕ). Повторите попытку')
        report = 'Вы ввели неправильный трек. Повторите попытку'
        return report

    row_number = res.index(track_number) + 1       # находим номер строки где находится Track_ID
    coordinate = 'E' + str(row_number)
    city_of_receiver =g_utilities.get_cell_value(coordinate)  # определяем город получателя
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

    coordinate = 'F' + str(row_number)
    g_utilities.write_cell_value(coordinate, date_time_of_delivery) # записываем время доставки во 6й столбец

    coordinate = 'G' + str(row_number)
    g_utilities.write_cell_value(coordinate, link_photo) # записываем ссылку на фото в 7й столбец

    print ('данные добавлены')

    report = 'Запись добавлена. Нажмите /Start чтобы продолжить'
    return report

#delevered('777', '651462', 'photos/2.jpg')
