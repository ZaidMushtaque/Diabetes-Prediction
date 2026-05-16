import sqlite3

# Connect database
conn = sqlite3.connect('users.db', check_same_thread=False)

# Create cursor
c = conn.cursor()

# Create table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT,
    password TEXT
)
''')

conn.commit()


# Add user
def add_user(username, password):
    c.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (username, password)
    )
    conn.commit()


# Check login
def login_user(username, password):
    c.execute(
        'SELECT * FROM users WHERE username=? AND password=?',
        (username, password)
    )

    data = c.fetchone()

    return data