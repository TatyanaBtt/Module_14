import sqlite3

conn = sqlite3.connect('not_telegram.db')
cursor = conn.cursor()
#
def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    )
    ''')
    for i in range(1, 5):
        cursor.execute('INSERT INTO Products(id, title, description, price) VALUES(?, ?, ?, ?)', (str(i),f"Продукт {i}", f"Описание {i}", str(i*100)))
        conn.commit()

def get_all_products():
    cursor.execute('SELECT title, description, price FROM Products')
    return cursor.fetchall()
conn.commit()
