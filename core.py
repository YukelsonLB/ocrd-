import psycopg2
from psycopg2 import OperationalError
import os
import easyocr


reader = easyocr.Reader(['en','ru'], gpu = False)
print('done')
###сортировка файлов###
unsorted_file_list = os.listdir(path=r"C:\Users\User\Desktop\ocrd+\images")
sortetd_file_list = sorted(unsorted_file_list)
os.chdir(path=r"C:\Users\User\Desktop\ocrd+\images")
print(sortetd_file_list)

image_list = []
for file in sortetd_file_list:
    if '.png' in file:
        image_list.append(file)
    elif '.jpg' in file:
        image_list.append(file)
    elif '.jpeg' in file:
        image_list.append(file)
    elif '.jfif' in file:
        image_list.append(file)
#print(image_list)

###Прогон картинок###
pile = []
for image in image_list:
    bond = reader.readtext(image)
    pile.append(bond)
#print(pile)


###Фильтр от всякого###
pile_copy = pile.copy()
trash_list = []
# print(pile_copy)
for trash in pile_copy:
    trash = list(map(list, trash))
    # print(trash)
    trash_list.append(trash)


for trash in trash_list:
    for i in trash:
        i.remove(i[0])
        i.remove(i[1])

tr = []
for i in trash_list:
    i = sum(i, [])
    tr.append(i)
for i in tr:
    for j in i:
        j.lower()

###создание массива строк найденых на картинок###
ansvers = []
for i in pile:
    for j in i:
        ansvers.append(j[1])
# print(ansvers)

for i in ansvers:
    if i == '':
        i =='None'
### создание словаря###
trash_dict = {key: value for key, value in zip(image_list, tr)}


###перебор словаря###
for i in trash_dict:
    trash_dict[i] = ' '.join(map(str,trash_dict[i]))
    trash_dict[i] = trash_dict[i].lower()

pict = []
for i in trash_dict.items():
    pict.append(i)
#print(trash_dict.items())
print(pict)
print('done')

### Создание базы###


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


connection = create_connection(
    "postgres", "postgres", "logocentrism1", "localhost", "5432"
)


def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

create_database_query = "CREATE DATABASE picture_base"
#create_database(connection, create_database_query)

###коннект###
connection = create_connection(
    "picture_base", "postgres", "logocentrism1", "127.0.0.1", "5432"
)

### создание таблицы###

def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

create_Pictures_table = """
CREATE TABLE IF NOT EXISTS Pictures (
  id SERIAL PRIMARY KEY,
  picture_name TEXT NOT NULL, 
  pict_text TEXT
)
"""

execute_query(connection, create_Pictures_table)
print('create_Pict_table: done')

###внесение данных в таблицу###
pict_records = ", ".join(["%s"] * len(pict))
insert_query = (
    f"INSERT INTO pictures (picture_name, pict_text) VALUES {pict_records}"
)

connection.autocommit = True
cursor = connection.cursor()
cursor.execute(insert_query, pict)
print('information insert into database')