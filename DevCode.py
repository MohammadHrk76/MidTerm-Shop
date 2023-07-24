import sqlite3

cnt = sqlite3.connect("ShopStore.db")

#----------------Create Product Table---------------------#
##sql = ''' CREATE TABLE products (
##       id INTEGER PRIMARY KEY,
##       pname CHAR (30) NOT NULL,
##        price INTEGER NOT NULL,
##        qnt INTEGER NOT NULL
##        ) '''
##cnt.execute(sql)

#----------------Insert Data into Product Table---------------------#

##sql = ''' INSERT INTO  products (pname, price, qnt)
##        VALUES ("Daewo Tv 4k", 880, 40) '''
##cnt.execute(sql)
##cnt.commit()

#----------------Create Cart Table----------------------------#

##sql = ''' CREATE TABLE cart (
##       id INTEGER PRIMARY KEY,
##       uid INTEGER NOT NULL,
##       pid INTEGER NOT NULL,
##       qnt INTEGER NOT NULL
##        ) '''
##cnt.execute(sql)
