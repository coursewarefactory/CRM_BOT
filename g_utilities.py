# -*- coding: utf-8 -*-
#! /usr/bin/env python 

from datetime import datetime
import calendar
import locale
#locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') 
from pprint import pprint
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials

def connect_to_sheets():
    """функция подключает к таблице Google. Предварительно нужно настроить доступ к API
       в Google аккаунте.
       Если соединение с сервером google не установлено возвращает соответствующее сообщение 
       """    
    flag = True
    CREDENTIALS_FILE = 'elite-coral-241813-08f497bfe238.json'  #  
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    try:
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # пробуем авторизоваться в гугл таблицах
    except Exception as e:
        report =' Сервер google временно недоступен. Повторите попытку позже. Чтобы продолжить введите команду /menu'
        flag = False
        return flag, report    
    spreadsheetId = '1zBhtvPaivNAHfi5oVOlZK0AVR5WFOC8WVwTKpqZhFHc'
    email = 'tvr33k@gmail.com' # почта 
    driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth)
    shareRes = driveService.permissions().create(
    fileId = spreadsheetId,
    #body = {'type': 'anyone', 'role': 'writer'},  # доступ на редактирование кому угодно
    body = {'type': 'user', 'role': 'writer', 'emailAddress': email},
    fields = 'id').execute()
    report =''
    return flag, report

def get_cell_value(coordinate_1):
    """Функция возвращает значение ячейки по координате.
       Если соединение с сервером google не установлено возвращает соответствующее сообщение"""

    flag = True
    CREDENTIALS_FILE = 'elite-coral-241813-08f497bfe238.json'  
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    try:
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # пробуем авторизоваться в гугл таблицах
    except Exception as e:
        report =' Сервер google временно недоступен. Повторите попытку позже. Чтобы продолжить введите команду /menu'
        flag = False
        return flag, report
    spreadsheetId = '1zBhtvPaivNAHfi5oVOlZK0AVR5WFOC8WVwTKpqZhFHc'
    range_name = 'Sheet1!{0}'   # по умолчанию ищем на листе с названием Sheet1
    range_name=range_name.format(coordinate_1)
    table = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=range_name).execute() # получаем словарь значений, где 'values' -  значение ячейки
    ans_value = table['values'][0][0] # получаем значение ячейки
    return flag, ans_value

def get_cell_range(start, finish):
    """Функция возвращает массив значений заданного диапазона ячеек.
       Значения пустых ячеек в массив не записываются.
       Если соединение с сервером google не установлено возвращает соответствующее сообщение
       """
    flag = True
    CREDENTIALS_FILE = 'elite-coral-241813-08f497bfe238.json'  
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    try:
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # пробуем авторизоваться в гугл таблицах
    except Exception as e:
        report =' Сервер google временно недоступен. Повторите попытку позже. Чтобы продолжить введите команду /menu'
        flag = False
        return flag, report
    spreadsheetId = '1zBhtvPaivNAHfi5oVOlZK0AVR5WFOC8WVwTKpqZhFHc'
    
    range_name = 'Sheet1!{0}:{1}'
    range_name=range_name.format(start, finish)
    table = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=range_name).execute()
    table = service.spreadsheets().values().get(spreadsheetId=spreadsheetId, range=range_name).execute()
    ans_value = table['values']
    res=[]
    for element in ans_value:
        res.append(element[0])
    #print(res)
    return flag, res


def write_cell_value(coordinate, value):
    """Функция записывает значение в ячейку по заданной координате"""

    flag = True
    CREDENTIALS_FILE = 'elite-coral-241813-08f497bfe238.json'  
    credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    try:
        service = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # пробуем авторизоваться в гугл таблицах
    except Exception as e:
        report =' Сервер google временно недоступен. Повторите попытку позже. Чтобы продолжить введите команду /menu'
        flag = False
        return flag, report
    spreadsheetId = '1zBhtvPaivNAHfi5oVOlZK0AVR5WFOC8WVwTKpqZhFHc'
    
    list_title = 'Sheet1'
    cell = coordinate
    value = value
    service.spreadsheets().values().batchUpdate(spreadsheetId=spreadsheetId, 
    body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": list_title + "!" + cell,
         "majorDimension": "ROWS",
         "values": [[value]]}

            ]
        }).execute()
    report =''
    return flag, report
