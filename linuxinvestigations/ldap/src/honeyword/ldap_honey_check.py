#!/usr/bin/python
#this script will basically check the password u entered by finding the appropriate mmethod 
#first it will find the id or the index of the password u entered and match it against the index stored in the honechecker database i.e. honey_checker.db

import sys
import sqlite3

def getindex(passwd):
	ldap_con = sqlite3.connect('ldap_hw.db')
	cursor = ldap_con.execute("SELECT ID, NAME, PASSWORD FROM USERS")
	for row in cursor:
		#print row[0]
		#print row[2]
		#print passwd
		if row[2] == passwd:
			#print "\n****************print succesful\n"
			return row[0]
		else:
			continue
	return 

def honey_check():
	honey_con = sqlite3.connect('honey_checker.db')
	cursor = honey_con.execute("SELECT NAME, ID FROM PASS_INDEX")
	index=getindex(sys.argv[2])
	if index:
		for row in cursor:
			if row[0] == sys.argv[1]:
				if row[1] == index:
					return True
				else:
					return False
			else:
				continue	
	else:
		print("password/user does not exists")
		sys.exit(-1)

def main():
	h=honey_check()
	if h:
		print "user exists and logined with authentic password"
	else:
		print "user trying to authenticate using honeyword "

main()







