import sqlite3
sqlite_connection = sqlite3.connect('products.db')
cursor = sqlite_connection.cursor()
def convert_tuple(c_tuple): 
  str='' 
  for i in c_tuple: 
    if isinstance(i, float) or isinstance(i, int):
       str = str+repr(i)+'||'
    else:
       str = str+i+'||'
  return str 
 


def output_sql_table(cursor, filename):
    print("Текущее содержимое таблицы products")
    data = cursor.execute("SELECT * FROM products")
    fout = open(filename, 'w')
    for row in data:
        str = convert_tuple(row)
        fout.write(str+'\n')
    fout.close
output_sql_table(cursor, 'output.txt')