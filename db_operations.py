import sqlite3

#setup and connect to database
def connect():
	conn=sqlite3.connect("records.db")
	cur=conn.cursor()
	cur.execute("CREATE TABLE IF NOT EXISTS Users (user_id INTEGER PRIMARY KEY, username text, password text)")
	cur.execute("CREATE TABLE IF NOT EXISTS Attributes (user_id integer NOT NULL, lrLimit, urLimit, vAmplitude, vPWidth,aAmplitude, aPWidth, FOREIGN KEY(user_id) REFERENCES Users (user_id))")
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

#Check if user already exists in database
def check_if_exists(user):
	conn=sqlite3.connect("records.db")
	cur=conn.cursor()
	cur.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE username=?)", (user,))
	exists = cur.fetchall()[0][0]
	if exists:
		return False
	return True
	conn.close()

#Add user to database
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

#Insert user's programmable parameters	
def add_attribute(id,lrLimit, urLimit, vAmplitude, vPWidth,aAmplitude, aPWidth):
	conn=sqlite3.connect("records.db")
	cur=conn.cursor()
	cur.execute("INSERT INTO Attributes VALUES (?,?,?,?,?,?,?)",(id,lrLimit, urLimit, vAmplitude, vPWidth,aAmplitude, aPWidth))
	conn.commit()
	conn.close()

#Update programmable parameter values
def update_attribute(id, parameters):
	conn=sqlite3.connect('records.db')
	cur=conn.cursor()
	cur.execute("Update Attributes set lrLimit=?, urLimit=?,vAmplitude=?,vPWidth=?, aAmplitude=?,aPWidth=? where user_id = ?",(parameters[0],parameters[1],parameters[2],parameters[3],parameters[4],parameters[5],id))
	conn.commit()
	conn.close()

#Fetch stored parameter values
def get_attributes(user_id):
	conn=sqlite3.connect('records.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM Attributes WHERE user_id=?", (user_id,))
	params = cur.fetchall()[0]
	conn.close() 
	return params

#Check if existing user exists. If so, indicate they can be logged in
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
		return id, parameters
	else:
		return -1, ()
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
		
connect()
# myID = register_user('hemel','myPass')
# add_attribute(1, '1.1','2.2','3.3','4.4','5.5','6.6')
# database_fetch()
# parameter_list = ['1.9','1.2','3.7','4.4','3.5','7.7']
# update_attribute(1,parameter_list)
# database_fetch()

