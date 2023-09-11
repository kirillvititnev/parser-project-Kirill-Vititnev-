# parser-project-Kirill-Vititnev-
wildberries parser

Для запуска необходима установка chromedriver v114:
https://chromedriver.chromium.org/downloads 


parserWB.py:

0) Введите путь к скачанному chromedriver
2) Получает на вход категорию(url) и необходимое количество страниц для считывания
3) С этих страниц parser получает ссылки на товары данной категории, сохраняя их во временный файл links.txt
4) Создает базу данных SQlite products.db  с таблицей products формата: (brand, product_name, color, price, currency, in_stock, rating)
5) Добавляет каждый товар из links.txt в products.db

Для просмотра содержимого products.db запустите output_to_txt.py (содержимое таблицы products попадет в файл output.txt
