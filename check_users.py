import sqlite3

def check_users():
    conn = sqlite3.connect('instance/flaskr.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    conn.close()
    return users

if __name__ == '__main__':
    users = check_users()
    if not users:
        print("No users in the database.")
    else:
        print(f"Users in the database: {users}")
