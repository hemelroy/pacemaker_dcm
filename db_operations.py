import sqlite3

def connect():
	conn=sqlite3.connect("records.db")
	cur=conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY, username text, password text)")
	cur.execute("CREATE TABLE IF NOT EXISTS Attributes (user_id integer NOT NULL, v Amp , a Amp, FOREIGN KEY(user_id) REFERENCES Users (user_id))")
	#cur.execute("CREATE TABLE IF NOT EXISTS Attributes (FOREIGN KEY(user_id) REFERENCES Users(user_id), v Amp, a Amp)")
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


def register_user(r_username, r_password):
	conn=sqlite3.connect("records.db")
	cur=conn.cursor()
	cur.execute("INSERT INTO Users VALUES (NULL,?,?)",(r_username,r_password))
	cur.execute("SELECT user_id FROM Users WHERE username =? AND password=?",(r_username, r_password))  
	id = cur.fetchall()[0][0]
	print (id)
	conn.commit()
	conn.close()
	return id
	
def add_attribute(id,v_value, a_value):
	conn=sqlite3.connect("records.db")
	cur=conn.cursor()
	#cur.execute("INSERT INTO Attributes VALUES (NULL,?,?)",(v_value, a_value))
	cur.execute("INSERT INTO Attributes VALUES (?,?,?)",(id,v_value, a_value))
	conn.commit()
	conn.close()

def database_fetch():
	conn=sqlite3.connect("records.db")
	cur=conn.cursor()
	cur.execute('SELECT * FROM Users')
	rows = cur.fetchall()
	for row in rows:
		print(row)
	cur.execute('SELECT * FROM Attributes')
	rows = cur.fetchall()
	for row in rows:
		print(row)

#check if existing user exists. If so, log them in
def login_user(user, password):
	conn=sqlite3.connect("records.db")
	cur=conn.cursor()
	cur.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE username=? AND password=?)", (user, password))
	exists = cur.fetchall()[0][0]
	if exists:
		cur.execute("SELECT user_id FROM Users WHERE username=? AND password=?", (user, password)) 
		id = cur.fetchall()[0][0]
		cur.execute("SELECT * FROM Attributes WHERE user_id=?", (id,)) 
		parameters = cur.fetchall()[0]
		print(parameters)
		return parameters
	else:
		return ()
	conn.close()

		
connect()
#myID = register_user('hemel','myPass')
#add_attribute(5, '3.9','2.1')
#database_fetch()

