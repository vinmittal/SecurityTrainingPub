import random
import sqlite3
import hashlib
conn = sqlite3.connect('usr.db')
cursor = conn.cursor()
class User(object):
	'Common class for all Users'
	UsrId = 0
	UsrTotal = 0
	try:
		conn.execute("CREATE TABLE USERS (ID INT NOT NULL, NAME TEXT NOT NULL, HONEYPASS TEXT NOT NULL );")
		conn.commit()
		conn.execute("CREATE TABLE USERS_PASS (ID INT NOT NULL, PASS TEXT NOT NULL );")
		conn.commit()

	except sqlite3.OperationalError:
		pass

	def __init__(self,name,passwd):
		self.name = name
		honeypass = hashlib.md5("dummy").hexdigest()
		self.passwd = hashlib.md5(passwd).hexdigest()
		passwd = self.passwd
		self.honeypass = honeypass
		self.UsrId = random.randint(0,1000)
		conn.commit()
		id = self.UsrId
		cursor.execute("INSERT INTO USERS (ID,NAME,HONEYPASS) VALUES ( ?,?,? )", (id,name,honeypass));
		cursor.execute("INSERT INTO USERS_PASS (ID,PASS) VALUES ( ?,?)", (id,passwd));
		cursor.execute("SELECT COUNT(*) FROM USERS");
		result = cursor.fetchone()
		User.UsrTotal=result[0]
		conn.commit()

	def GetUsrDetail(self):
		return (self.UsrId, self.name, self.honeypass)

class Userlogin(object):
	'Common class for login Users'
	Rows = ''
	try:
		conn.execute("CREATE TABLE USERS (ID INT NOT NULL, NAME TEXT NOT NULL, HONEYPASS TEXT NOT NULL );")
		conn.commit()
		conn.execute("CREATE TABLE USERS_PASS (ID INT NOT NULL, PASS TEXT NOT NULL );")
		conn.commit()

	except sqlite3.OperationalError:
		pass

	def __init__(self,name,passwd):
		cursor.execute("SELECT * FROM USERS");
		rows = cursor.fetchall()
		Userlogin.Rows = rows
		conn.commit()

	def GetUsrDetail(self):
		return Userlogin.Rows

def dataentry():
	name = raw_input('Enter name: ')
	password = raw_input('Enter pasword: ')
	obj1 = User(name,password)
	detail1 = obj1.GetUsrDetail()
	if detail1:
		print 'Account created succesfully'

def checkpass(id,name,passwd):
		cursor.execute("SELECT * FROM USERS_PASS");
		rows = cursor.fetchall()
		i = 0
		for row in rows:
			if row[0] == id:
				if row[1] == hashlib.md5(passwd).hexdigest():
					print '*'*20
					print 'Login successfull'
					i = 1
					break
		if i == 0:
			print 'Incorrect Username or Password'
		conn.commit()

def usrlogin():
	name = raw_input('Enter name: ')
	password = raw_input('Enter pasword: ')
	obj1 = Userlogin(name,password)
	rows = obj1.GetUsrDetail()
	i = 0
	for row in rows:
		if row[1] == name and row[2] == hashlib.md5(password).hexdigest():
			print '*'*20
			print 'Honey Password enterd! Alerted the admin'
			print '*'*20
			i = 1
			break
		elif row[1] == name:
			checkpass(row[0], name, password)
			i = 1
			break
	if i == 0:
		print 'Incorrect Username or Password'
def main():
	print '\n'
	print '*'*20
	print 'Select your option'
	print '*'*20
	print '1. Register new Users'
	print '2. Login'
	inp = input('Enter Option: ')
	if inp == 1:
		dataentry()
	elif inp == 2:
		usrlogin()
	else:
		print '\n Enter Correct Option'
main()
