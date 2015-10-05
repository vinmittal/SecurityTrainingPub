#!/usr/bin/python
#this script will create entries of the user in the ldap database which is a sqlite database named ldap_hw.db into the table USERS
import sqlite3	
import sys
import subprocess

def main():
	#we are going to let the user input his name and password and we are going to append 20 honeywords for that user so total there are 21 sweetwords.
	ldap_con = sqlite3.connect('ldap_hw.db')
	curs = ldap_con.cursor()
	subprocess.call("python gen.py 20 ",shell=True)
	f=open('pwlist.txt','r')
	pwd_l=[]
	pwd_l=f.readlines()
	nlist=[]
	for i in pwd_l:
		nlist.append(i.rstrip('\n'))
	print nlist
	for i in nlist:
		ldap_con.execute("INSERT INTO USERS(NAME,PASSWORD) VALUES(?,?)",(sys.argv[1],i));
		ldap_con.commit()
	print("Records created successfully")
	ldap_con.execute("INSERT INTO USERS(NAME,PASSWORD) VALUES(?,?)",(sys.argv[1],sys.argv[2]));
	ldap_con.commit()
	subprocess.call("rm pwlist.txt ",shell=True)
	ldap_con.close()

main()
	#this scripts add one user at a time along with some honey words.....


