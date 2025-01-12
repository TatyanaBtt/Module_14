import sqlite3

conn = sqlite3.connect('not_telegram.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users(email)')

# for i in range(1, 11):
#     cursor.execute('INSERT INTO Users(username, email, age, balance) VALUES(?, ?, ?, ?)',
#                    (f"User{i}", f"example{i}@gmail.com", str(i*10), 1000))
# for i in range(1, 10, 2):
#     cursor.execute('UPDATE Users SET balance = ? WHERE id = ?', (str(500), str(i)))
#
# for i in range(1, 11, 3):
#     cursor.execute('DELETE FROM Users WHERE id = ?', (str(i), ))

cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

cursor.execute('SELECT COUNT(*) FROM Users')
total1 =cursor.fetchone()[0]
cursor.execute('SELECT SUM(balance) FROM Users')
total2 = cursor.fetchone()[0]
print(total2/total1)

conn.commit()
conn.close()