import sqlite3

conn = sqlite3.connect('not_telegram.db')
cursor = conn.cursor()


def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users(
    id INT PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    age INT NOT NULL,
    balance INT NOT NULL
    )
    ''')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users(email)')

    for i in range(1, 5):
        cursor.execute('INSERT INTO Products(id, title, description, price) VALUES(?, ?, ?, ?)',
                       (str(i), f"Продукт {i}", f"Описание {i}", str(i * 100)))
        conn.commit()

def get_all_products():
    cursor.execute('SELECT title, description, price FROM Products')
    conn.commit()
    return cursor.fetchall()


def add_user(username, email, age):
    cursor.execute(f'INSERT INTO Users(username, email, age, balance) VALUES("{username}", "{email}", "{age}", 1000)')
    conn.commit()


def is_included(username):
    cursor.execute('SELECT username FROM Users WHERE username=?', (username,))
    return cursor.fetchone()
