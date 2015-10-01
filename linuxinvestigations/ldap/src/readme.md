#Installation of openldap in centos 6 
#so basically ldap is the lightweight directive access protocol which runs over TCP and the openldap is the free implementation of LDAP.
#openldap is the client-server implementation in which there is a sever which holds various records in his own maintained database and various client query #the database for various purpose, for example, getting information, for authentication,etc.
#so let's begin:

#first we are going to configure the server:

so lets suppose i have a machine whose ip address is 10.0.2.4/24 in cidr notation and we are going to make it ldap-server
 Various steps to be followed are as below:

 a). yum install openldap* -y   #installing all the packages of openldap
 b). rpm -qa| grep openldap     #checking whether it is installed or not
 c). slappasswd      #run this command which gives u the hash for the password u provide interactively, which we are going to make root password for ldap 
 d). vim /etc/openldap/slapd.d/cn=config/olcDatabase={2}hdb.ldif   #we are going to edit the following file for setting the password and the domain
 e). If the "olcRootPW" attribute does not already exist, create it. Then set the value to be the hash you created from slappasswd. For example:
 		change the following line in the olcDatabase={2}hdb.ldif file
 
						olcRootDN: cn=Manager,dc=acme,dc=com #acme is the domain name whatever u want write, it can be anything..like secure720,etc
						olcSuffix: dc=acme,dc=com          #same here       
						olcRootPW: {SSHA}5lPFVw19zeh7LT53hQH69znzj8TuBrLv #this {SSHA} is the hash u generate in step 3 i.e. slappasswd
 f). vim /etc/openldap/slapd.d/cn=config/olcDatabase\=\{1\}monitor.ldif and change the following
 		olcAccess: {0}to * by dn.base="gidNumber=0+uidNumber=0,cn=peercred,cn=external,cn=auth" read by dn.base="cn=Manager,dc=acme,dc=com" read by * none
 		#in this change acme to whatever u decided in my case i changed it to secure720
 g). the root user for your LDAP is cn=Manager,dc=acme,dc=com. The root user's password is the password that you entered using slappasswd (see step 3)
 h). vim /etc/openldap/slapd.d/cn=config/olcDatabase={2}hdb.ldif and add the following at the end of the file

					olcAccess: {0}to attrs=userPassword by self write by dn.base="cn=Manager,dc=acme,dc=com" write by anonymous auth by * none

					olcAccess: {1}to * by dn.base="cn=Manager,dc=acme,dc=com" write by self write by * read	
				Adding the following two lines to the end, restrict users from viewing other users' password hash.

 i). now we are configured with slapd demon which is the server program in openldap so we can start now,
 			service slapd start
 j). till now we have configured the ldap server but the schema or database is empty so we need to populate it. first we are going to add the root entry.
 	1. create a file name anything but with .ldif extension which is the extension for ldapserver. in my case, acme.ldif
 		vim acme.ldif #add the following line to the file
 		dn: dc=acme,dc=com
		objectClass: dcObject
		objectClass: organization
		dc: acme
		o : acme
		# these five lines creates the root entry in the file in our case root is acme
	2. add these setting in the ldap database
		ldapadd -f acme.ldif -D cn=Manager,dc=acme,dc=com -w "root password created using slappasswd not the hash only password"
	3. verify the entry by using the following command
		ldapsearch -x -LLL -b dc=acme,dc=com
			dn: dc=acme,dc=com 
			objectClass: dcObject
			objectClass: organization
			dc: acme
			o: acme
			#if the following output is shown then we are done with adding entries
 k). by default openldap server listens on 389 port so configure your iptables to allow traffic input through 389 port. for that
 			iptables --flush or iptables -f #this flushes all the rules in the iptables.
 			you can also add "iptables -A INPUT -p tcp --dport 389 -j ACCEPT" if the above method does not work
 l). similarly for adding organization unit create a file using extension supposer users.ldif and add the following line to the file
 			dn: ou=Users,dc=acme,dc=com
			objectClass: organizationalUnit
			ou: Users
 m). ldapadd -f users.ldif -D cn=Manager,dc=acme,dc=com -w "root password created using slappasswd not the hash only password"
 n). to add a user do the following thing by using name.ldif file
 		dn: cn=rishabh,ou=Users,dc=acme,dc=com
		cn: rishabh
		sn: kushwaha
		objectClass: inetOrgPerson
		uid: rk
 o). ldapadd -f name.ldif -D cn=Manager,dc=acme,dc=com -w "root password created using slappasswd not the hash only password"
 now u have created a user named rishabh in the ldap database, similarly we can create more and add entry respectively..
 we can also use migrationtools designed specially for ldap server for adding user,groups, etc things.
 now we are going to configure the client for ldap server
 p). install the following packages for clients configuration
 	yum install openldap-clients openldap openldap-devel
 	yum install authconfig authconfig-gtk
 q). run authconfig-gtk and configure the system authentication through ldap server and give the server ip and domain component
 r). run ldapsearch -x -b "dc=acme,dc=com" for checking that the client is able to reach the server or not
 s). now try to use the su user command u will be able to authenticate if the user is in the ldap database but the home directory will not be created
 t). for sharing the home directory we will use the nfs mount system and edit /etc/exports file and add the following line
 		/home/ldap ldapserverip/255.255.255.0(octet)(*) or (rw,root_squash)
  u). sevice nfs restart
  v). step t and u should be peformed on the server
  w). for the client open /etc/auto.master and below the /misc *,  add the following line 
  		/home/ldap 			/etc/auto.ldap
  x). vim auto.ldap and add the followind line
  		*	-rw server.acme.com:/home/&
  y). service autofs restart
  z). su user1	#now u will be able to login in the system
  for enabling the home directory creation use "authconfig --enablemkhomedir --update" commmand or we can use pam_mkhomedir.so module to do that.




