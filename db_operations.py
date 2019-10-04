import sqlite3

def connect():
    conn=sqlite3.connect("records.db")
    cur=conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY, username text, password text)")
    conn.commit()
    conn.close()

#Check if more than 10 users have been registered
def check_user_count():
    is_full = True

    conn=sqlite3.connect("records.db")
    cur=conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Users")
    count = int(cur.fetchall()[0][0])
    if count <= 10:
        is_full = False
    conn.close()

    return is_full


def register_user(user, password):
    conn=sqlite3.connect("records.db")
    cur=conn.cursor()
    
    conn.commit()
    conn.close()



connect()