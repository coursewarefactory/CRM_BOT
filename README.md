## Простая CRM система для курьерской службы в виде телеграм бота. 

### Техническое задание:
Реализовать простую CRM систему для курьерской службы в виде бота.
Представьте, что есть несколько городов: A city, B city, C city и тд. В каждом городе есть один курьер нашей компании, у которого есть смартфон, через который он будет отчитываться о всех действиях: принял новую посылку, отдал посылку адресату. Каждой новой посылке должно быть присвоено ID, с помощью которого мы будем их отличать.

### Реализовать основные функции:
- Принял новую посылку: в какой город отправить, имя адресата
- Отдал посылку адресату: номер посылки и фото получателя с посылкой    
    
Информация о всех посылка должны храниться в режиме онлайн в таблице в Google Docs, чтобы менеджеры могли наглядно видеть, что делают курьеры.

У каждой посылки в таблице должны быть следующие данные: ID, город отправителя, город получателя, время и дата получения посылки, время и дата доставки посылки (если уже доставлена) и фото получателя с посылкой (если ее уже доставили).

### Основные файлы:

- crm_bot.py - главный файл бота
- logistic.py - модуль, в котором реализованы основные пользовательские функции
- g_utilities.py - модуль, в котором реализованы основные функции для работы с базами Google Sheets

    
### Краткая инструкция

1. Добавьте бота @CRM_111bot и нажмите /start. Вы окажитесь в меню команд.
2. Команда /1 - отправка отчета о приеме посылки. После нажатия /1 вы получите запрос на ввод имени получателя. Введите имя получателя и нажмите "отправить". Далее вы получите запрос на ввод города получателя. Введите город получателя и нажмите "отправить". Вы получите подтверждение о добавлении данных в таблицу Google и 6-значный трек номер. Для продолжение нажмите /menu.

Таблицу Google можно посмотреть по ссылке:
https://docs.google.com/spreadsheets/d/1zBhtvPaivNAHfi5oVOlZK0AVR5WFOC8WVwTKpqZhFHc/edit#gid=0

3. Команда /2 - отправка отчета о доставке посылки. После нажатия /2 вы получите запрос на ввод трек номера. Введите трек номер и нажмите "отправить". Если введен неверный трек номер вы получите сообщение об этом и повторный запрос на ввод трек номера. После успешного ввода трек номера вы получите запрос на отправку фото. Отправьте фото. После успешной отправки фото вы получите сообщение "запись добавлена". Для продолжения нажмите /menu. Для просмотра обновленной таблицы Google воспользутесь вышеуказанной таблицей.

