#import stuff
import MySQLdb
from types import *
#from numpy import *
import sys, time

##In order to import this toolbox into a python script you need to 
##do the following. Copy the following lines of code below
# import sys
# sys.path.append('/home/carlos/Dropbox/BlackBox/sql')
# from pysql_commands import *

# or

# In order to get python to search for all of your lovely blackbox 
# python routines. Add this to your .bashrc file

# for d in /home/carlos/Dropbox/BlackBox/*/; do
# 	PYTHONPATH+=:$d
# done
# export PYTHONPATH


class PYSQL():
    '''This is PySQL class'''
    def __init__(self,dbname,maintable,attr,debug=False):
        '''connect to mysql server'''
        if sys.platform == 'linux2':
            # It's possible here to get an access denied error. This happened to me when I upgraded 
            # to Ubuntu 16.04 from 14.04. What you want to do is see if you can even login to sql by itself
            # ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)
            # This means that you have a password but unfortunately you don't know what it is.
            # if you try 
            # $ mysql -u root
            # or
            # $ sudo mysql -u root
            # it means you can't login
            # Anyway - try this
            # $ service mysql stop
            # $ sudo mysqld_safe --skip-grant-tables
            # $ mysql -u root
            # -> UPDATE user SET Password=PASSWORD('YOURNEWPASSWORD') WHERE User='root'; FLUSH PRIVILEGES; exit;
            # you should be able to test everything in python
            # I actually totally fucked this up and ended up reinstalling mysql
            # Funny thing is the error was still here so I did the service stop thing
            # and that didn't work so I uninstalled again and deleted the entire /etc/mysql folder
            # when I tried to reinstall mysql it wouldn't work because I deleted that folder
            # so I went ahead and did a purge
            # $ sudo apt-get remove --purge mysql-\*
            # but that removed python-mysqldb, flightgear AND mysql-server. Holy shit.
            # so I'm reinstalling flightgear right now....ugh. I have to download 1.5 GB what the fuck. This is so insane
            # Ok flightgear done. Now time for mysql-server. I just installed mysql-server and guess what!? It still doesn't
            # log in. what the actual fuck. This is driving me crazy
            # Ok I found a new website and did this
            # $ sudo /etc/init.d/mysql stop            
            # $ sudo /usr/sbin/mysqld --skip-grant-tables --skip-networking &
            # $ mysql -u root
            # and then I get this error!
            # ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/run/mysqld/mysqld.sock' (2)
            # this is the website: https://help.ubuntu.com/community/MysqlPasswordReset
            # apparently there was a mysql.cnf file linked through /etc/alternatives. It references a file in mysql.conf.d
            # so I commented out the includedir in mysql.conf.d to see if that did anything
            # It didn't like that. Mainly because the mysql files in conf.d are completely different than mysql.conf.d
            # ok damn. I tried to go back into my ArchiveOS to copy /var/run/mysqld/*.socket and I couldn't find it. Like 
            # the file doesn't exist. But! I did go into debian.cnf and find a password. So I'm going to restart mysql
            # $ sudo service mysql restart
            # $ mysql -u root -p 
            # and type in the crazy password. Here we go            
            # ok welp the user name is actually drum roll please debian-sys-maint. So you may as well just copy that into 
            # the row below. Make sure to use the password generated in /etc/mysql/debian.cnf
            try:
                #WHat computer is this? Need to write this down
                self.sql = MySQLdb.connect(host="localhost",user="debian-sys-maint",passwd="OConsqELCLmkVWzl")
            except:
                try:
                    ##Same here
                    self.sql = MySQLdb.connect(host="localhost",user="debian-sys-maint",passwd="x8lLZ6r3ID4KoMqT")
                except:
                    try :
                        #Home laptop
                        self.sql = MySQLdb.connect(host="localhost",user="debian-sys-maint",passwd="lZP7QT25viMN6QfM")
                    except:
                        #Work Laptop - X1 Carbon - Ubuntu 18.04 - Last change - 5/16/2019
                        self.sql = MySQLdb.connect(host="localhost",user="debian-sys-maint",passwd="SEWBn0SHP7eQySY3")
                        
        else:
            self.sql = MySQLdb.connect(host="localhost",user="root",passwd="password")
        self.ptr = self.sql.cursor() #save cursor object that interacts with sql
        #create and use database
        self.DropDB(dbname)
        self.createDB(dbname)

        #create tables
        self.createTB(maintable,attr,debug)

    def close(self):
        '''close and disconnect from server'''
        self.ptr.close()
        self.sql.close()

    #create definitions
    def createDB(self,dbname):
        create = "CREATE DATABASE IF NOT EXISTS " + dbname
        self.ptr.execute(create)
        self.useDB(dbname)

    def useDB(self,dbname):
        use = "USE " + dbname
        self.ptr.execute(use)

    def display(self,tablename,debug=False):
        disp = "SELECT * FROM " + tablename
        self.ptr.execute(disp)
        result = []
        while(1):
            val = self.ptr.fetchone()
            if val == None: break
            if debug == True:
                print val
            result.append(val)
        return result

    def DropTB(self,tablename):
        drop = "DROP TABLE IF EXISTS " + tablename
        self.ptr.execute(drop)

    def createTB(self,tablename,list,debug=False):
        create = "CREATE TABLE IF NOT EXISTS " + tablename + "("
        length = len(list)
        for x in range(0,length):
            row = list[x]
            create += row[0] + " " + row[1]
            if x < length-1:
                create += ","
            else:
                create += ")"
	if debug == True:
	    print create
        self.ptr.execute(create)
        self.deleteTable(tablename);

    def add2TB(self,tablename,tableattr,values,debug=False):
        length = len(tableattr)
        add = "INSERT INTO " + tablename + " ("
        for x in range(0,length):
            attr = tableattr[x]
            add += attr[0]
            if x < length-1:
                add += ","
            else:
                add += ")"
                add += " VALUES ("
        for x in range(0,length):
            if length == 1:
                val = values
            else:
                val = values[x]
            if type(val) == type(2):
                #value is an integer
                add += str(val)
            else:
                #value is a string
                add += "'" + val + "'"
            if x < length-1:
                add += ","
            else:
                add += ") "
        if debug==True:
            print "length of table: ", length
            print "table: ",tablename
            print "attr: ",tableattr
            print "values: ",values
            print add
        else:
            self.ptr.execute(add)

    def unique(self,tablename,tableattr,tableattr2=None,tableattr3=None):
        if tableattr2 == None and tableattr3 == None:
            unique = "SELECT DISTINCT " + tableattr + " FROM " + tablename + " ORDER BY " + tableattr
        if tableattr2 != None and tableattr3 == None:
            unique = "SELECT DISTINCT " + tableattr + " FROM " + tablename + " WHERE Artist LIKE '%" + tableattr2 + "%'"
        if tableattr2 != None and tableattr3 != None:
            unique = "SELECT DISTINCT " + tableattr + " FROM " + tablename + " WHERE Artist LIKE '%" + tableattr2 + "%' AND Album LIKE '%" + tableattr3 + "%'"
            
        self.ptr.execute(unique)

        result = []
        while(1):
            val = self.ptr.fetchone()
            if val == None: break
            #print val
            result.append(val)
        return result

    def search(self,tablename,tableattr,value,order=None):
        search = "SELECT * FROM " + tablename + " WHERE " + tableattr + " LIKE '%"
        if type(value) == type(2):
            #value is an integer
            search += str(value)
        else:
            #value is a string
            search += value
            search += "%'"

        if order != None:
            search += " ORDER BY " + order

        self.ptr.execute(search)

        result = []
        while(1):
            val = self.ptr.fetchone()
            if val == None: break
            #print val
            result.append(val)
        return result

    def saveDB(self,tablename,order):
        result = []
        search = "SELECT * FROM " + tablename + " ORDER BY " + order
        self.ptr.execute(search)
        while (1):
            val = self.ptr.fetchone()
            if val == None: break
            result.append(val)
        return result

    def DropDB(self,dbname):
        self.ptr.execute("DROP DATABASE IF EXISTS " + dbname)

    def deleteTable(self,tablename):
        delete = "DELETE FROM " + tablename
        self.ptr.execute(delete)

    def deleteField(self,tablename,title):
        delete = "DELETE FROM " + tablename + " WHERE title = " + "'" + title + "'";
        self.ptr.execute(delete)



# Copyright - Carlos Montalvo 2016
# You may freely distribute this file but please keep my name in here
# as the original owner
