# Python Script to Implement Hney Password

This is a demo script to implement Honey Passowrds as per https://people.csail.mit.edu/rivest/honeywords/.

# Honey Password for all account is "dummy", I have kept this for demo purpose.

### Working of Script

* Run the Python Script and Register a user.
* Rerun the script and trying loging as the user you have created. 
* This all three test cases:
1. Enter correct username and password to login
2. Enter wrong username and password
3. Enter out our honey password, that we assume attacker will get if he compromises the database. Honey password is "dummy"
4. On entering, it will promt that honey password is entered. Please note, this is just for demo, in real case it will not prompt to attacker, it will send message to system admin.

Also check the usr.db file, there you will find two tables, one having Username and Honey Password in form of MD5 and another table have user and the original password entered during registered in md5.

Have already created user "harsh" and password "harsh"

I have added screenshots and this is just a initial version of script.

Want to contribute? Great!
Clone, Change it and Commit it :P



