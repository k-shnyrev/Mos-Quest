# Квест на знание Москвы

## Описание проекта

Веб-сервер с вопросами на знание Москвы.

Чтобы увидеть вопросы, нужно зарегистрироваться.

Почту можно указать любую, восстановление пароля не предусмотрено.

На заглавной странице всегда показываются набранные баллы всех зарегистрированных пользователей.

За ответ с первого раза даётся **10 баллов**,
за каждый ошибочный ответ **снимается балл**,
неснижаемый остаток на каждый вопрос - **1 балл**.

## Запуск проекта

Для запуска сервера достаточно запустить файл app.py.

При запуске из командной строки программа принимает
опциональные аргументы host и port.

Значения по умолчанию:\
host - 127.0.0.1\
port - 5000

После запуска сервера достаточно ввести хост и порт в качестве адреса.\
Для значений по умолчанию: http://127.0.0.1:5000/

Для корректной работы необходимо соединение с Интернетом.

## Структура проекта

* data - директория, содержащая описания структур данных.
* db - директория, в которой находится база с вопросами, ответами
  и пользователями.\
  _При отсутствии база создаётся заново, заполняясь пятью вопросами._
* forms - директория, содержащая описания форм регистрации, входа и ответа на вопросы.
* static/img - директория с изображениями.
  * static/img/questions - директория, куда загружаются изображения с Яндекс.Карт, 
    полученные при помощи Static API. Изображение — важная иллюстрация к вопросу.
* templates - директория с шаблонами для Flask
* app.py - основной файл программы.
* maps.py - вспомогательный файл для работы с API Яндекс.Карт.
* readme.md - описание проекта (этот файл).
* requirements.txt - список зависимостей — библиотек, необходимых для запуска проекта.