import sqlite3

cnt = sqlite3.connect("ShopStore.db")

def getAllProducts():

    sql = ''' SELECT * FROM products '''
    result = cnt.execute(sql)
    row = result.fetchall()
    return row

def getAllCarts(uid):

    sql = ''' SELECT * FROM carts WHERE uid = ? '''
    result = cnt.execute(sql, (uid,))
    row = result.fetchall()
    return row

def buyValidation(pid, qnt):

    if pid == "" or qnt == "":
        return False, "Please Fill the inputs"
    
    sql = ''' SELECT * FROM products WHERE id = ? '''
    result = cnt.execute(sql , (pid,))
    row = result.fetchone()

    if not row:
        return False, "Wrong Product id"

    sql = ''' SELECT * FROM products WHERE id = ? AND qnt >= ? '''
    result = cnt.execute(sql , (pid,qnt))
    row = result.fetchone()

    if not row:
        return False, "Not Enough Products"

    return True, ""

def AddProductValidate(pname, price, qnt):

    if pname == "" or price == "" or qnt == "":
        return False, "Please Fill the inputs"

    if int(price) < 0 or int(qnt) < 0:
        return False, "Wrong price or quantity Values"

    sql = ''' SELECT * FROM products WHERE pname = ?'''
    result = cnt.execute(sql , (pname,))
    row = result.fetchone()

    if row:
        return False, "Product has already Exist"

    return True, ""

def AddProduct(pname, price, qnt):
    
    sql = ''' INSERT INTO  products (pname, price, qnt) VALUES (?,?,?) '''
    cnt.execute(sql, (pname, price, qnt))
    cnt.commit()

def savetocart(uid, pid, qnt):

    sql = ''' INSERT INTO carts (uid, pid, qnt)  VALUES(?,?,?) '''
    cnt.execute(sql, (uid, pid, qnt))
    cnt.commit()

def updateqnt(pid, qnt):

    sql = ''' UPDATE products SET qnt = (qnt)-? WHERE id = ? '''
    cnt.execute(sql, (qnt, pid))
    cnt.commit()
