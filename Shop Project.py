import tkinter
import sqlite3
import ProductAction
#---------------------------------------------------------------------------#
def login():

    global session

    user = txt_user.get()
    pas = txt_pass.get()

    sql = ''' SELECT * FROM users WHERE username = ? AND pass = ?'''
    result = cnt.execute(sql, (user, pas))
    rows = result.fetchall()

    if len(rows) < 1:

        lbl_msg.configure(text = "Wrong username or Password!", fg = "red")

    else:
        lbl_msg.configure(text = "Welcome to Account!", fg = "green")
        session = rows[0][0]
        btn_login.configure(state = "disable")
        btn_logout.configure(state = "active")
        btn_shop.configure(state = "active")
        btn_cart.configure(state="active")
        btn_panel.configure(state = "disable")
        txt_user.delete(0 , "end")
        txt_pass.delete(0 , "end")

    if user == "admin" and pas == "123456789":
        btn_panel.configure(state = "active")
        txt_user.delete(0 , "end")
        txt_pass.delete(0 , "end")
        
#----------------------- Logout ----------------------------------------------#
def logout():

    btn_login.configure(state = "active")
    btn_logout.configure(state = "disabled")
    btn_shop.configure(state = "disabled")
    btn_cart.configure(state = "disabled")
    btn_panel.configure(state = "disable")
    lbl_msg.configure(text = "You are Logged Out!",fg="green")

#---------------------- Validation ----------------------------------------------#
def validation(user, pas,cpass, addr):

    if user == "" or pas == "" or addr == "":
        return False, "Fill in the Blanks!"

    if len(pas) < 8:
        return False, "Password Length Error!"

    if pas != cpass:
        return False, "Password and Cpass Mismatch!"

    sql = ''' SELECT * FROM users WHERE username = ?'''
    result = cnt.execute(sql, (user,))
    rows = result.fetchall()

    if len(rows) > 0:
        return False, "Username already exist!"

    return True, ""
#------------------------ Submit -------------------------------------------#    
def submit():
    def register():
        user = txt_user.get()
        pas = txt_pass.get()
        cpass = txt_cpass.get()
        addr = txt_addr.get()
        result, errorMSG = validation(user, pas,cpass, addr)

        if result:
            sql = ''' INSERT INTO users (username, pass, addr, grade)
                    VALUES(?,?,?,?) '''

            cnt.execute(sql, (user, pas, addr, 5))
            cnt.commit()
            lbl_msg.configure(text = "Submit done!", fg = "green")

            txt_user.delete(0 , "end")
            txt_pass.delete(0 , "end")
            txt_cpass.delete(0 , "end")
            txt_addr.delete(0 , "end")
            
        else:
             lbl_msg.configure(text = errorMSG, fg = "red")

#-------------------- Submit Window -----------------------------------#            

    win_submit = tkinter.Toplevel(win)  
    win_submit.title("Submit Panel")
    win_submit.geometry("300x400")
    
    lbl_user = tkinter.Label(win_submit,text = "Username: ")
    lbl_user.pack()

    txt_user = tkinter.Entry(win_submit)
    txt_user.pack()

    lbl_pass = tkinter.Label(win_submit,text = "Password: ")
    lbl_pass.pack()

    txt_pass = tkinter.Entry(win_submit, show = "*")
    txt_pass.pack()

    lbl_cpass = tkinter.Label(win_submit, text = "Confirmation Password : ")
    lbl_cpass.pack()

    txt_cpass = tkinter.Entry(win_submit, show = "*")
    txt_cpass.pack()
    
    lbl_addr = tkinter.Label(win_submit,text = "Address: ")
    lbl_addr.pack()

    txt_addr = tkinter.Entry(win_submit)
    txt_addr.pack()
    
    lbl_msg = tkinter.Label(win_submit,text = "")
    lbl_msg.pack()
    
    btn_submit = tkinter.Button(win_submit,text = "Submit",width = 10, command = register)
    btn_submit.pack()
    
    win_submit.mainloop()
    
#-------------------------- Shop -------------------------------------#
def shop():
    def buy():

        global session
        pid = txt_id.get()
        qnt = txt_qnt.get()

        result,msg = ProductAction.buyValidation(pid, qnt)

        if not result: #if result == False
              lbl_msg.configure(text = msg,fg = "red")  
              return

        ProductAction.savetocart(session,pid,qnt)

        lbl_msg.configure(text = "saved to cart",fg = "green") 
        txt_id.delete(0,"end")
        txt_qnt.delete(0,"end")
        
        ProductAction.updateqnt(pid,qnt)
        
        lstbx.delete(0,"end")
        products = ProductAction.getAllProducts()
        for product in products:
            text = f"id:{product[0]},   Name:{product[1]},   price:{product[2]},   quantity:{product[3]}"
            lstbx.insert("end",text)

#------------------------ Shop Window ------------------------------------------------------------#     

    win_shop = tkinter.Toplevel(win)
    win_shop.title("Shop panel")
    win_shop.geometry("400x350")
    
    lstbx = tkinter.Listbox(win_shop,width=65)
    lstbx.pack()
    
    products = ProductAction.getAllProducts()
    for product in products:
        text = f"id:{product[0]},   Name:{product[1]},   price:{product[2]},   quantity:{product[3]}"
        lstbx.insert("end",text)

    lbl_id = tkinter.Label(win_shop, text = "product id : ")
    lbl_id.pack()
    txt_id = tkinter.Entry(win_shop)
    txt_id.pack()

    lbl_qnt = tkinter.Label(win_shop, text = "quantity : ")
    lbl_qnt.pack()
    txt_qnt = tkinter.Entry(win_shop)
    txt_qnt.pack()

    lbl_msg = tkinter.Label(win_shop, text = "")
    lbl_msg.pack()

    btn_buy = tkinter.Button(win_shop, text = "buy", command = buy)
    btn_buy.pack()
    
    win_shop.mainloop()

#------------------------ Insert Product --------------------------------------------------#
def adminpanel():
    def insertProduct():
        pname = txt_pname.get()
        price = txt_price.get()
        qnt = txt_qnt.get()

        result,msg = ProductAction.AddProductValidate(pname, price, qnt)

        if not result:
            lbl_msg.configure(text = msg,fg = "red")
            return

        ProductAction.AddProduct(pname, price, qnt)

        lbl_msg.configure(text = "Product Added Successfully!", fg = "green")

        txt_pname.delete(0 , "end")
        txt_price.delete(0 , "end")
        txt_qnt.delete(0 , "end")
        
#---------------------- Admin Panel Window ------------------------------------------------#    
    win_panel = tkinter.Toplevel(win)
    win_panel.title("Admin Panel")
    win_panel.geometry("300x300")

    lbl_pname = tkinter.Label(win_panel,text = "Product Name: ")
    lbl_pname.pack()

    txt_pname = tkinter.Entry(win_panel, width = 24)
    txt_pname.pack()

    lbl_price = tkinter.Label(win_panel,text = "Price: ")
    lbl_price.pack()

    txt_price = tkinter.Entry(win_panel)
    txt_price.pack()

    lbl_qnt = tkinter.Label(win_panel,text = "Quantity: ")
    lbl_qnt.pack()

    txt_qnt = tkinter.Entry(win_panel)
    txt_qnt.pack()

    lbl_msg = tkinter.Label(win_panel, text = "")
    lbl_msg.pack()

    btn_add = tkinter.Button(win_panel, text = "Add Product",width = 10, command = insertProduct)
    btn_add.pack()

    win_panel.mainloop()

#---------------------- Cart Window -----------------------------------------------#
def mycart():
    
    win_cart = tkinter.Toplevel(win)
    win_cart.title("Cart Panel")
    win_cart.geometry("400x300")

    lstbx = tkinter.Listbox(win_cart, width = 60)
    lstbx.pack()

    uid = session

    carts = ProductAction.getAllCarts(uid)

    for cart in carts:
        if cart[1] == session:
            text = f"ID: {cart[0]}, UserID: {cart[1]},   ProductID: {cart[2]},   Quantity: {cart[3]}"
            lstbx.insert("end", text)

    win_cart.mainloop()
    
#---------------------- Main Window -----------------------------------------------#

session = False
cnt = sqlite3.connect("ShopStore.db")

win = tkinter.Tk()
win.title("Shop Project")
win.geometry("400x350")

lbl_user = tkinter.Label(win,text = "Username: ")
lbl_user.pack()

txt_user = tkinter.Entry(win)
txt_user.pack()

lbl_pass = tkinter.Label(win,text = "Password: ")
lbl_pass.pack()

txt_pass = tkinter.Entry(win, show = "*")
txt_pass.pack()

lbl_msg = tkinter.Label(win,text = "")
lbl_msg.pack()

btn_login = tkinter.Button(win,text = "Login", width = 10, command = login)
btn_login.pack(pady = "5")

btn_submit = tkinter.Button(win,text = "Submit", width = 10, command = submit)
btn_submit.pack(pady = "5")

btn_logout = tkinter.Button(win,text = "Logout", state = "disabled", width = 10, command = logout)
btn_logout.pack(pady = "5")

btn_shop = tkinter.Button(win,text = "Shop", state = "disabled" ,width = 10, command = shop)
btn_shop.pack(pady = "5")

btn_panel = tkinter.Button(win,text = "Admin Panel", state = "disable", width = 10, command = adminpanel)
btn_panel.pack(pady = "5")

btn_cart = tkinter.Button(win,text = "MyCart",state = "disabled", width = 10, command = mycart)
btn_cart.pack(pady = "5")

win.mainloop()
