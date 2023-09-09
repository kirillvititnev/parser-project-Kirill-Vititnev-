import time 

import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.common.action_chains import ActionChains

import sqlite3
#starting WebDriver 
service = Service(executable_path=r'/opt/homebrew/bin/chromedriver')
options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=service, options=options)
links = open("links.txt", 'r')
def get_links_from_category(category_url, filename, num_of_pages):

    links = open("links.txt", 'w')
    if not category_url:
        return
    driver.get(category_url)

    for i in range(num_of_pages):
        time.sleep(1)
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CLASS_NAME, "pagination-next"))
        next_page_button = driver.find_element(By.CLASS_NAME, "pagination-next")
        speed = 8
        current_scroll_position, new_height= 0, 1
        while current_scroll_position <= new_height:
            current_scroll_position += speed
            driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
            new_height = driver.execute_script("return document.body.scrollHeight")

        links_on_page = driver.find_elements(By.CLASS_NAME, 'product-card__link')
        for link in links_on_page:
            links.write(link.get_attribute('href')+'\n')
        driver.get(next_page_button.get_attribute('href'))
    links.close()


def output_sql_table(cursor):
    print("Текущее содержимое таблицы products")
    data = cursor.execute("SELECT * FROM products")
    for row in data:
        print(row)

def insert_varible_into_table(cursor, brand, product_name, color, price, currnecy, in_stock, rating):
    try:
        

        sqlite_insert_with_param = """INSERT INTO products
                              (brand, product_name, color, price, currency, in_stock, rating)
                              VALUES (?, ?, ?, ?, ?, ?, ?);"""

        data_tuple = (brand, product_name, color, price, currency, in_stock, rating)
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqlite_connection.commit()
        print("Товар \""+product_name+"\" добавлен в таблицу Products")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)





try:
    sqlite_connection = sqlite3.connect('products.db')
    sqlite_create_table_query = '''CREATE TABLE products (
                                brand VARCHAR(30),
                                product_name VARCHAR(30),
                                color VARCHAR(20),
                                price INTEGER,
                                currency VARCHAR(10),
                                in_stock VARCHAR(15),
                                rating REAL);'''

    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    print("Таблица SQLite создана")
except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)



print("Отправьте url категории из которой считать товары:")
category_url = input()
print("Отправьте количество страниц из категории для считывания:")
num_pages = int(input())
get_links_from_category(category_url, "links.txt", num_pages)


for url in links:
    driver.get(url)
    WebDriverWait(driver, 10).until(lambda x: x.find_element(By.CLASS_NAME, "product-page__header"))
    title=driver.find_element(By.CLASS_NAME,'product-page__header' ).text
    article=driver.find_element(By.CLASS_NAME, 'product-article__copy').text
    colors_list=(driver.find_elements(By.CLASS_NAME,"color"))
    colors_string = ''
    for color in colors_list:
        colors_string+= color.text
    sold_out = driver.find_elements(By.CLASS_NAME, 'sold-out-product')
    rating = driver.find_element(By.CLASS_NAME, 'product-review__rating').text
    in_stock = "SOLD_OUT"
    if len(sold_out) == 0:
        price=driver.find_element(By.CLASS_NAME, 'price-block__final-price').text
        in_stock = "IN_STOCK"
    else:
        price = "0"
    currency = "none"
    if (price != 0 ) and (price[-1] == '₽'):
        price = price[0:-2]
        currency = 'RUB'
    if title.find('\n')!= -1:
        brand, title = title.split("\n")
    else:
        brand = ''
    insert_varible_into_table(cursor, brand, title, colors_string, price, currency, in_stock, rating) 

output_sql_table(cursor)
if (sqlite_connection):
    print("Всего строк, измененных после подключения к базе данных: ", sqlite_connection.total_changes)
    sqlite_connection.close()
    print("Соединение с SQLite закрыто")
driver.quit()
