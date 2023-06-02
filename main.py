import time
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import random
import pyodbc
from PIL import ImageTk, Image

root = Tk()
root.geometry("1450x700")
root.config(bg="steel blue")
img = PhotoImage(file="bg.png")
l_img = Label(root, image=img, bg="blue").pack(pady=25)


def exit():
    output = messagebox.askyesno("Al-Nahdi Care", "Do you want to leave?")
    if output > 0:
        root.destroy()


def new():
    global logo
    m = Toplevel()
    m.title("New window")
    m.geometry("1450x700")
    f_title = Frame(m, bd=10, relief=RIDGE, height=70, bg="white")
    f_title.pack(side=TOP, fill=X)
    f_title.pack_propagate(FALSE)
    title = Label(
        f_title,
        bg="white",
        fg="midnight blue",
        text="AL-NAHDI PHARMACY",
        font=("Times", 30, "bold", "italic"),
    )
    title.pack()
    img2 = Image.open(r"C:\Users\sana4\Downloads\nahdibg.png")
    resize_img = img2.resize((200, 50))
    logo = ImageTk.PhotoImage(resize_img)
    l_logo = Label(f_title, image=logo)
    l_logo.place(x=0, y=0)
    frm = Frame(m, bd=10, relief=RIDGE, width=750, height=407, bg="steel blue4")
    frm.place(x=0, y=70)
    frm2 = Frame(m, bd=10, relief=RIDGE, width=1365, height=80, bg="steel blue4")
    frm2.place(x=0, y=478)
    data1_frm = Frame(m, bd=10, relief=RIDGE, bg="snow3", width=615, height=255)
    data1_frm.place(x=750, y=70)
    data1_frm.pack_propagate(0)
    data2_frm = Frame(m, bd=10, relief=RIDGE, bg="snow3", height=145)
    data2_frm.pack(side=BOTTOM, fill=X)
    data2_frm.pack_propagate(0)
    data3_frm = Frame(m, bd=10, relief=RIDGE, bg="steel blue4", width=615, height=150)
    data3_frm.place(x=750, y=327)

    o_ID = StringVar()
    c_ID = StringVar()
    f_name = StringVar()
    l_name = StringVar()
    c_mail = StringVar()
    c_contact = StringVar()
    category = StringVar()
    medicine = StringVar()
    issue_date = StringVar()
    exp_date = StringVar()
    price = StringVar()
    quantity = StringVar()
    tax = StringVar()
    subtotal = StringVar()
    total = StringVar()
    discount = StringVar()
    discount_amount = StringVar()

    x = random.randint(10000, 50000)
    y = str(x)
    c_ID.set(y)

    def exit_m():
        output = messagebox.askyesno("Al-Nahdi Care", "Do you wish to leave?", parent=m)
        if output > 0:
            messagebox.showinfo(
                "AL-Nahdi Care",
                "Thank you for choosing Nahdi Clinics. Have a pleasant day.",
                parent=m,
            )
            root.destroy()

    def display():
        global tree1
        global tree1_scroll

        con = pyodbc.connect(
            (
                r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                r"DBQ=C:\Users\sana4\Documents\Pharmacy.accdb;"
            )
        )
        cur1 = con.cursor()
        stock = cur1.execute("select * from Medicine")
        tree1_scroll = Scrollbar(data2_frm, orient=VERTICAL)
        tree1_scroll.pack(side=RIGHT, fill=Y)
        tree1 = ttk.Treeview(
            data2_frm, selectmode=BROWSE, yscrollcommand=tree1_scroll.set
        )
        tree1.pack(fill=BOTH, expand=1)
        tree1_scroll.config(command=tree1.yview)
        tree1["columns"] = ["1", "2", "3", "4", "5", "6", "7"]
        tree1["show"] = "headings"
        tree1.column("1", width=50, anchor="w")
        tree1.column("2", width=90, anchor="c")
        tree1.column("3", width=90, anchor="c")
        tree1.column("4", width=80, anchor="c")
        tree1.column("5", width=100, anchor="c")
        tree1.column("6", width=87, anchor="c")
        tree1.heading("1", text="Medicine ID")
        tree1.heading("2", text="Medicine Name")
        tree1.heading("3", text="Medicine Type")
        tree1.heading("4", text="Price")
        tree1.heading("5", text="Manufacture date")
        tree1.heading("6", text="Expiry date")
        for i in stock:
            tree1.insert("", END, values=i)
        con.close()

    def add_to_cart():
        global prz
        prz = []
        z = price.get()
        a = z.split(".")
        prz_each = int(a[1]) * int(quantity.get())
        prz.append(prz_each)
        o = random.randint(99, 999)
        z = str(o)
        o_ID.set(z)
        con = pyodbc.connect(
            (
                r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                r"DBQ=C:\Users\sana4\Documents\Pharmacy.accdb;"
            )
        )
        cur1 = con.cursor()
        num = cur1.execute("SELECT [Amount] FROM Stock")
        contact = [i[0] for i in num]
        elements = [category, medicine, issue_date, exp_date, price, quantity]
        for i in range(len(contact)):
            if contact[i] <= 0:
                del contact[i]
                contact.insert(i, 0)
                cur1.execute(
                    f"UPDATE Stock SET Amount = {contact[i]} WHERE Stock_ID = {str(i + 1)}"
                )
        con.commit()

        if medicine.get() == "Ibubrufen":
            if contact[0] == 0:
                messagebox.showwarning(
                    "ALERT",
                    "We apologize for the unavailability of this item. Please select any other.",
                    parent=m,
                )
            else:
                rem_quan = int(contact[0]) - int(quantity.get())
                del contact[0]
                contact.insert(0, rem_quan)
                cur1.execute(f"UPDATE Stock SET Amount = {rem_quan} WHERE Stock_ID = 1")
                con.commit()
                cur1.execute(
                    f"INSERT INTO Receipt([Order_ID],[Customer_ID],[First Name],[Last Name],[Customer Contact],[Item Purchased],[Price],[Amount_Ordered])"
                    f" values('{o_ID.get()}','{c_ID.get()}','{f_name.get()}','{l_name.get()}','{c_contact.get()}','{medicine.get()}','{price.get()}','{quantity.get()}')"
                )
                con.commit()
                con.close()
                answer = messagebox.askyesno(
                    "My Cart",
                    "Order Successfully Added to Cart. Would you like to order again?",
                    parent=m,
                )
                if answer > 0:
                    for i in elements:
                        i.set("")
        elif medicine.get() == "Erythromycin":
            if contact[1] == 0:
                messagebox.showwarning(
                    "ALERT",
                    "We apologize for the unavailability of this item. Please select any other.",
                    parent=m,
                )
            else:
                rem_quan = contact[1] - int(quantity.get())
                del contact[1]
                contact.insert(1, rem_quan)
                cur1.execute(f"UPDATE Stock SET Amount = {rem_quan} WHERE Stock_ID = 2")
                con.commit()
                cur1.execute(
                    f"INSERT INTO Receipt([Order_ID],[Customer_ID],[First Name],[Last Name],[Customer Contact],[Item Purchased],[Price],[Amount_Ordered])"
                    f" values('{o_ID.get()}','{c_ID.get()}','{f_name.get()}','{l_name.get()}','{c_contact.get()}','{medicine.get()}','{price.get()}','{quantity.get()}')"
                )
                con.commit()
                con.close()
                answer = messagebox.askyesno(
                    "My Cart",
                    "Order Successfully Added to Cart. Would you like to order again?",
                    parent=m,
                )
                if answer > 0:
                    for i in elements:
                        i.set("")
        elif medicine.get() == "Augmentin":
            if contact[2] == 0:
                messagebox.showwarning(
                    "ALERT",
                    "We apologize for the unavailability of this item. Please select any other.",
                    parent=m,
                )
            else:
                rem_quan = contact[2] - int(quantity.get())
                del contact[2]
                contact.insert(2, rem_quan)
                cur1.execute(f"UPDATE Stock SET Amount = {rem_quan} WHERE Stock_ID = 3")
                con.commit()
                cur1.execute(
                    f"INSERT INTO Receipt([Order_ID],[Customer_ID],[First Name],[Last Name],[Customer Contact],[Item Purchased],[Price],[Amount_Ordered])"
                    f" values('{o_ID.get()}','{c_ID.get()}','{f_name.get()}','{l_name.get()}','{c_contact.get()}','{medicine.get()}','{price.get()}','{quantity.get()}')"
                )
                con.commit()
                con.close()
                answer = messagebox.askyesno(
                    "My Cart",
                    "Order Successfully Added to Cart. Would you like to order again?",
                    parent=m,
                )
                if answer > 0:
                    for i in elements:
                        i.set("")
        elif medicine.get() == "Metoclopramide":
            if contact[3] == 0:
                messagebox.showwarning(
                    "ALERT",
                    "We apologize for the unavailability of this item. Please select any other.",
                    parent=m,
                )
            else:
                rem_quan = contact[3] - int(quantity.get())
                del contact[3]
                contact.insert(3, rem_quan)
                cur1.execute(f"UPDATE Stock SET Amount = {rem_quan} WHERE Stock_ID = 4")
                con.commit()
                cur1.execute(
                    f"INSERT INTO Receipt([Order_ID],[Customer_ID],[First Name],[Last Name],[Customer Contact],[Item Purchased],[Price],[Amount_Ordered]) "
                    f"values('{o_ID.get()}','{c_ID.get()}','{f_name.get()}','{l_name.get()}','{c_contact.get()}','{medicine.get()}','{price.get()}','{quantity.get()}')"
                )
                con.commit()
                con.close()
                answer = messagebox.askyesno(
                    "My Cart",
                    "Order Successfully Added to Cart. Would you like to order again?",
                    parent=m,
                )
                if answer > 0:
                    for i in elements:
                        i.set("")
        elif medicine.get() == "Nystatin":
            if contact[4] == 0:
                messagebox.showwarning(
                    "ALERT",
                    "We apologize for the unavailability of this item. Please select any other.",
                    parent=m,
                )
            else:
                rem_quan = contact[4] - int(quantity.get())
                del contact[4]
                contact.insert(4, rem_quan)
                cur1.execute(f"UPDATE Stock SET Amount = {rem_quan} WHERE Stock_ID = 5")
                con.commit()
                cur1.execute(
                    f"INSERT INTO Receipt([Order_ID],[Customer_ID],[First Name],[Last Name],[Customer Contact],[Item Purchased],[Price],[Amount_Ordered])"
                    f" values('{o_ID.get()}','{c_ID.get()}','{f_name.get()}','{l_name.get()}','{c_contact.get()}','{medicine.get()}','{price.get()}','{quantity.get()}')"
                )
                con.commit()
                con.close()
                answer = messagebox.askyesno(
                    "My Cart",
                    "Order Successfully Added to Cart. Would you like to order again?",
                    parent=m,
                )
                if answer > 0:
                    for i in elements:
                        i.set("")
        elif medicine.get() == "Metronidazol":
            if contact[5] == 0:
                messagebox.showwarning(
                    "ALERT",
                    "We apologize for the unavailability of this item. Please select any other.",
                    parent=m,
                )
            else:
                rem_quan = contact[5] - int(quantity.get())
                del contact[5]
                contact.insert(5, rem_quan)
                cur1.execute(f"UPDATE Stock SET Amount = {rem_quan} WHERE Stock_ID = 6")
                con.commit()
                cur1.execute(
                    f"INSERT INTO Receipt([Order_ID],[Customer_ID],[First Name],[Last Name],[Customer Contact],[Item Purchased],[Price],[Amount_Ordered])"
                    f" values('{o_ID.get()}','{c_ID.get()}','{f_name.get()}','{l_name.get()}','{c_contact.get()}','{medicine.get()}','{price.get()}','{quantity.get()}')"
                )
                con.commit()
                con.close()
                answer = messagebox.askyesno(
                    "My Cart",
                    "Order Successfully Added to Cart. Would you like to order again?",
                    parent=m,
                )
                if answer > 0:
                    for i in elements:
                        i.set("")
        elif medicine.get() == "Dulcolax":
            if contact[6] == 0:
                messagebox.askretrycancel(
                    "ALERT",
                    "We apologize for the unavailability of this item. Please select any other.",
                    parent=m,
                )
            else:
                rem_quan = contact[6] - int(quantity.get())
                del contact[6]
                contact.insert(6, rem_quan)
                cur1.execute(f"UPDATE Stock SET Amount = {rem_quan} WHERE Stock_ID = 7")
                con.commit()
                cur1.execute(
                    f"INSERT INTO Receipt([Order_ID],[Customer_ID],[First Name],[Last Name],[Customer Contact],[Item Purchased],[Price],[Amount_Ordered])"
                    f" values('{o_ID.get()}','{c_ID.get()}','{f_name.get()}','{l_name.get()}','{c_contact.get()}','{medicine.get()}','{price.get()}','{quantity.get()}')"
                )
                con.commit()
                con.close()
                answer = messagebox.askyesno(
                    "My Cart",
                    "Order Successfully Added to Cart. Would you like to order again?",
                    parent=m,
                )
                if answer > 0:
                    for i in elements:
                        i.set("")
        elif medicine.get() == "Atenolol":
            if contact[7] == 0:
                messagebox.showwarning(
                    "ALERT",
                    "We apologize for the unavailability of this item. Please select any other.",
                    parent=m,
                )
            else:
                rem_quan = contact[7] - int(quantity.get())
                del contact[7]
                contact.insert(7, rem_quan)
                cur1.execute(f"UPDATE Stock SET Amount = {rem_quan} WHERE Stock_ID = 8")
                con.commit()
                cur1.execute(
                    f"INSERT INTO Receipt([Order_ID],[Customer_ID],[First Name],[Last Name],[Customer Contact],[Item Purchased],[Price],[Amount_Ordered]) "
                    f"values('{o_ID.get()}','{c_ID.get()}','{f_name.get()}','{l_name.get()}','{c_contact.get()}','{medicine.get()}','{price.get()}','{quantity.get()}')"
                )
                con.commit()
                con.close()
                answer = messagebox.askyesno(
                    "My Cart",
                    "Order Successfully Added to Cart. Would you like to order again?",
                    parent=m,
                )
                if answer > 0:
                    for i in elements:
                        i.set("")
        elif medicine.get() == "Aldomet":
            if contact[8] == 0:
                messagebox.showwarning(
                    "ALERT",
                    "We apologize for the unavailability of this item. Please select any other.",
                    parent=m,
                )
            else:
                rem_quan = contact[8] - int(quantity.get())
                del contact[8]
                contact.insert(8, rem_quan)
                cur1.execute(f"UPDATE Stock SET Amount = {rem_quan} WHERE Stock_ID = 9")
                con.commit()
                cur1.execute(
                    f"INSERT INTO Receipt([Order_ID],[Customer_ID],[First Name],[Last Name],[Customer Contact],[Item Purchased],[Price],[Amount_Ordered])"
                    f" values('{o_ID.get()}','{c_ID.get()}','{f_name.get()}','{l_name.get()}','{c_contact.get()}','{medicine.get()}','{price.get()}','{quantity.get()}')"
                )
                con.commit()
                con.close()
                answer = messagebox.askyesno(
                    "My Cart",
                    "Order Successfully Added to Cart. Would you like to order again?",
                    parent=m,
                )
                if answer > 0:
                    for i in elements:
                        i.set("")
        elif medicine.get() == "Paracetamol":
            if contact[9] == 0:
                messagebox.askretrycancel(
                    "ALERT",
                    "We apologize for the unavailability of this item. Please select any other.",
                    parent=m,
                )
            else:
                rem_quan = contact[9] - int(quantity.get())
                del contact[9]
                contact.insert(9, rem_quan)
                cur1.execute(
                    f"UPDATE Stock SET Amount = {rem_quan} WHERE Stock_ID = 10"
                )
                con.commit()
                cur1.execute(
                    f"INSERT INTO Receipt([Order_ID],[Customer_ID],[First Name],[Last Name],[Customer Contact],[Item Purchased],[Price],[Amount_Ordered]) "
                    f"values('{o_ID.get()}','{c_ID.get()}','{f_name.get()}','{l_name.get()}','{c_contact.get()}','{medicine.get()}','{price.get()}','{quantity.get()}')"
                )
                con.commit()
                con.close()
                answer = messagebox.askyesno(
                    "My Cart",
                    "Order Successfully Added to Cart. Would you like to order again?",
                    parent=m,
                )
                if answer > 0:
                    for i in elements:
                        i.set("")

    def get_receipt():
        global prz
        global tree2
        global tree2_scroll
        con = pyodbc.connect(
            (
                r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                r"DBQ=C:\Users\sana4\Documents\Pharmacy.accdb;"
            )
        )
        sum_prz = sum(prz)
        Gst = sum_prz * (17 / 100)
        rounded_GST = round(Gst, 2)
        Total = sum_prz + rounded_GST
        subtotal.set("Rs.{}".format(sum_prz))
        tax.set("Rs.{}".format(rounded_GST))
        discount.set("0%")
        total.set("Rs.{}".format(Total))
        discount_amount.set("Rs.0")
        cur1 = con.cursor()
        num = cur1.execute("select [Customer Contact No] FROM Customer")
        contact_info = [i[0] for i in num]
        print(contact_info)
        for number in contact_info:
            if number == int(c_contact.get()):
                messagebox.showinfo(
                    "Congratulations!",
                    "Thank you visiting again. We provide you a 40% discount voucher on your purchase today.",
                    parent=m,
                )
                disc = float(Total) * 0.4
                rounded_amount = "{:.2f}".format(disc)
                new_amount = Total - float(rounded_amount)
                new_new = str(new_amount)
                total.set("Rs.{}".format(new_new))
                discount.set("40%")
                discount_amount.set("Rs.{:.2f}".format(disc))
        cur1 = con.cursor()
        order = cur1.execute("select * from Receipt")
        cur2 = con.cursor()
        cur2.execute(
            f"INSERT INTO Customer([Customer ID],[First Name],[Last Name],[Customer Email],[Customer Contact No]) "
            f"values('{c_ID.get()}','{f_name.get()}','{l_name.get()}','{c_mail.get()}','{c_contact.get()}')"
        )

        tree2_scroll = Scrollbar(data1_frm, orient=HORIZONTAL)
        tree2_scroll.pack(side=BOTTOM, fill=X)
        tree2 = ttk.Treeview(
            data1_frm, selectmode=BROWSE, xscrollcommand=tree2_scroll.set
        )
        tree2.pack(fill=BOTH, expand=1)
        tree2_scroll.config(command=tree2.xview)
        tree2["columns"] = ("1", "2", "3", "4", "5", "6", "7", "8")
        tree2["show"] = "headings"
        tree2.column("1", width=100, anchor="w")
        tree2.column("2", width=100, anchor="c")
        tree2.column("3", width=100, anchor="c")
        tree2.column("4", width=100, anchor="c")
        tree2.column("5", width=100, anchor="c")
        tree2.column("6", width=100, anchor="c")
        tree2.column("7", width=100, anchor="w")
        tree2.column("8", width=100, anchor="w")
        tree2.heading("1", text="Order_ID")
        tree2.heading("2", text="Customer_ID")
        tree2.heading("3", text="First Name")
        tree2.heading("4", text="Last Name")
        tree2.heading("5", text="Customer Contact")
        tree2.heading("6", text="Item Purchased")
        tree2.heading("7", text="Price")
        tree2.heading("8", text="Amount_Ordered")
        for i in order:
            tree2.insert("", END, values=i)
        con.commit()
        con.close()

    def clear():
        global tree1
        global tree2
        global tree2_scroll
        global tree1_scroll
        o = random.randint(10000, 20000)
        z = str(o)
        c_ID.set(z)
        data = [
            f_name,
            l_name,
            c_mail,
            c_contact,
            category,
            medicine,
            issue_date,
            exp_date,
            price,
            quantity,
            subtotal,
            tax,
            total,
            discount,
            discount_amount,
        ]
        for i in data:
            i.set("")
        con = pyodbc.connect(
            (
                r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
                r"DBQ=C:\Users\sana4\Documents\Pharmacy.accdb;"
            )
        )
        cur1 = con.cursor()
        cur1.execute("DELETE * from Receipt")
        con.commit()
        con.close()
        tree2_scroll.destroy()
        tree2.destroy()
        tree1_scroll.destroy()
        tree1.destroy()
        messagebox.showinfo("CLEAR", "All fields cleared.", parent=m)

    def confirm(cb2):
        val = cb2.get()
        date = time.strftime("%d/%m/%Y")
        issue_date.set(date)
        if val == "Paracetamol":
            exp_date.set("9/4/2023")
            price.set("Rs.150")
        elif val == "Ibubrufen":
            exp_date.set("18/4/2023")
            price.set("Rs.200")
        elif val == "Erythromycin":
            exp_date.set("8/7/2023")
            price.set("Rs.250")
        elif val == "Augmentin":
            exp_date.set("10/3/2023")
            price.set("Rs.330")
        elif val == "Metronidazol":
            exp_date.set("1/6/2023")
            price.set("Rs.360")
        elif val == "Metoclopramide":
            exp_date.set("8/3/2023")
            price.set("Rs.400")
        elif val == "Nystatin":
            exp_date.set("31/3/2023")
            price.set("Rs.400")
        elif val == "Atenolol":
            exp_date.set("30/6/2023")
            price.set("Rs.1000")
        elif val == "Aldomet":
            exp_date.set("18/2/2023")
            price.set("Rs.900")
        elif val == "Dulcolax":
            exp_date.set("12/5/2023")
            price.set("Rs.550")

    def get(cb, cb2):
        val = cb.get()
        messagebox.showinfo("SELECTION", "Please Select A Medicine", parent=m)
        if val == "Analgesic":
            cb2["values"] = ("Paracetamol", "Ibubrufen")
        elif val == "Antibiotic":
            cb2["values"] = ("Erythromycin", "Augmentin")
        elif val == "Antidiarrheal":
            cb2["values"] = "Metronidazol"
        elif val == "Antiemetic":
            cb2["values"] = "Metoclopramide"
        elif val == "Antifungal":
            cb2["values"] = "Nystatin"
        elif val == "Anti-Hypertensive":
            cb2["values"] = ("Atenolol", "Aldomet")
        elif val == "Laxative":
            cb2["values"] = "Dulcolax"

    label1 = Label(
        frm,
        text="Customer ID",
        bg="light blue",
        borderwidth=5,
        width=15,
        font=("Times", 14, "italic", "bold"),
    ).place(x=15, y=30)
    label2 = Label(
        frm,
        text="First name",
        bg="light blue",
        borderwidth=5,
        width=15,
        font=("Times", 14, "italic", "bold"),
    ).place(x=15, y=100)
    label16 = Label(
        frm,
        text="Last name",
        bg="light blue",
        borderwidth=5,
        width=15,
        font=("Times", 14, "italic", "bold"),
    ).place(x=15, y=170)
    label3 = Label(
        frm,
        text="Customer Email",
        bg="light blue",
        borderwidth=5,
        width=15,
        font=("Times", 14, "italic", "bold"),
    ).place(x=15, y=240)
    label4 = Label(
        frm,
        text="Customer Contact No.",
        bg="light blue",
        borderwidth=5,
        width=16,
        font=("Times", 14, "italic", "bold"),
    ).place(x=13, y=310)
    label5 = Label(
        frm,
        text="Medicine Type",
        bg="light blue",
        borderwidth=5,
        width=13,
        font=("Times", 12, "italic", "bold"),
    ).place(x=400, y=18)
    label6 = Label(
        frm,
        text="Medicine Name",
        bg="light blue",
        borderwidth=5,
        width=13,
        font=("Times", 12, "italic", "bold"),
    ).place(x=400, y=82)
    label7 = Label(
        frm,
        text="Issue Date",
        bg="light blue",
        borderwidth=5,
        width=13,
        font=("Times", 12, "italic", "bold"),
    ).place(x=400, y=150)
    label8 = Label(
        frm,
        text="Expiry Date",
        bg="light blue",
        borderwidth=5,
        width=13,
        font=("Times", 12, "italic", "bold"),
    ).place(x=400, y=210)
    label9 = Label(
        frm,
        text="Price Per piece",
        bg="light blue",
        borderwidth=5,
        width=13,
        font=("Times", 12, "italic", "bold"),
    ).place(x=400, y=270)
    label10 = Label(
        frm,
        text="Quantity",
        bg="light blue",
        borderwidth=5,
        width=13,
        font=("Times", 12, "italic", "bold"),
    ).place(x=400, y=330)
    label11 = Label(
        data3_frm,
        text="Paid Tax",
        bg="light blue",
        borderwidth=5,
        width=10,
        font=("Times", 14, "italic", "bold"),
    ).place(x=15, y=10)
    label14 = Label(
        data3_frm,
        text="Discount",
        bg="light blue",
        borderwidth=5,
        width=10,
        font=("Times", 14, "italic", "bold"),
    ).place(x=15, y=50)
    label12 = Label(
        data3_frm,
        text="Subtotal",
        bg="light blue",
        borderwidth=5,
        width=10,
        font=("Times", 14, "italic", "bold"),
    ).place(x=15, y=90)
    label13 = Label(
        data3_frm,
        text="Total Amount",
        bg="light blue",
        borderwidth=5,
        width=10,
        font=("Times", 14, "italic", "bold"),
    ).place(x=300, y=70)
    label15 = Label(
        data3_frm,
        text="Discount Amount",
        bg="light blue",
        borderwidth=5,
        width=13,
        font=("Times", 11, "italic", "bold"),
    ).place(x=300, y=20)
    entry1 = Entry(
        frm,
        width=15,
        textvariable=c_ID,
        font=("Times", 14, "bold"),
        bd=3,
        justify=CENTER,
    ).place(x=215, y=30)
    entry2 = Entry(
        frm, width=15, textvariable=f_name, font=("Times", 14, "bold"), bd=3
    ).place(x=215, y=100)
    entry14 = Entry(
        frm, width=15, textvariable=l_name, font=("Times", 14, "bold"), bd=3
    ).place(x=215, y=170)
    entry3 = Entry(
        frm, width=15, textvariable=c_mail, font=("Times", 14, "bold"), bd=3
    ).place(x=215, y=240)
    entry4 = Entry(
        frm, width=15, textvariable=c_contact, font=("Times", 14, "bold"), bd=3
    ).place(x=215, y=310)
    entry5 = Entry(
        frm, width=15, textvariable=issue_date, font=("Times", 13, "bold"), bd=3
    ).place(x=550, y=150)
    entry6 = Entry(
        frm, width=15, textvariable=exp_date, font=("Times", 13, "bold"), bd=3
    ).place(x=550, y=210)
    entry7 = Entry(
        frm, width=15, textvariable=price, font=("Times", 13, "bold"), bd=3
    ).place(x=550, y=270)
    entry8 = Entry(
        frm, width=15, textvariable=quantity, font=("Times", 13, "bold"), bd=3
    ).place(x=550, y=330)
    entry9 = Entry(
        data3_frm, textvariable=tax, width=11, font=("Times", 14, "bold"), bd=3
    ).place(x=160, y=10)
    entry12 = Entry(
        data3_frm, width=11, textvariable=discount, font=("Times", 14, "bold"), bd=3
    ).place(x=160, y=50)
    entry10 = Entry(
        data3_frm, width=11, textvariable=subtotal, font=("Times", 14, "bold"), bd=3
    ).place(x=160, y=90)
    entry11 = Entry(
        data3_frm, width=11, textvariable=total, font=("Times", 14, "bold"), bd=3
    ).place(x=440, y=70)
    entry13 = Entry(
        data3_frm,
        width=11,
        textvariable=discount_amount,
        font=("Times", 14, "bold"),
        bd=3,
    ).place(x=440, y=20)
    value = (
        "Analgesic",
        "Antibiotic",
        "Antidiarrheal",
        "Antiemetic",
        "Antifungal",
        "Anti-Hypertensive",
        "Laxative",
    )
    combo1 = ttk.Combobox(
        frm, width=13, textvariable=category, values=value, font=("Times", 13, "bold")
    )
    combo1.place(x=550, y=18)
    comb1_btn = Button(
        frm,
        width=10,
        text="Confirm",
        font=("Times", 8, "bold"),
        command=lambda: get(combo1, combo2),
    )
    comb1_btn.place(x=580, y=44)
    combo2 = ttk.Combobox(
        frm, width=13, textvariable=medicine, font=("Times", 13, "bold")
    )
    combo2.place(x=550, y=82)
    comb2_btn = Button(
        frm,
        width=10,
        text="Confirm",
        font=("Times", 8, "bold"),
        command=lambda: confirm(combo2),
    )
    comb2_btn.place(x=580, y=108)
    btn3 = Button(
        frm2,
        width=14,
        text="Display Stock",
        font=("Times", 16, "bold"),
        activebackground="snow3",
        bd=7,
        bg="snow3",
        command=display,
    )
    btn3.place(x=60, y=3)
    btn3 = Button(
        frm2,
        width=14,
        text="Add to Cart",
        font=("Times", 16, "bold"),
        activebackground="snow3",
        bd=7,
        bg="snow3",
        command=add_to_cart,
    )
    btn3.place(x=310, y=3)
    btn3 = Button(
        frm2,
        width=14,
        text="Get Receipt",
        font=("Times", 16, "bold"),
        activebackground="snow3",
        bd=7,
        bg="snow3",
        command=get_receipt,
    )
    btn3.place(x=580, y=3)
    btn3 = Button(
        frm2,
        width=14,
        text="Clear",
        font=("Times", 16, "bold"),
        activebackground="snow3",
        bd=7,
        bg="snow3",
        command=clear,
    )
    btn3.place(x=850, y=3)
    btn3 = Button(
        frm2,
        width=14,
        text="EXIT",
        font=("Times", 16, "bold"),
        activebackground="red",
        bd=7,
        bg="red",
        command=exit_m,
    )
    btn3.place(x=1100, y=3)


btn1 = Button(
    root,
    bg="cadet blue",
    width=15,
    height=1,
    bd=10,
    text="Proceed to Store",
    font=("Times", 20, "italic", "bold"),
    justify=CENTER,
    activebackground="cadet blue",
    activeforeground="white",
    command=new,
).place(x=1000, y=550)
btn2 = Button(
    root,
    bg="red",
    width=15,
    height=1,
    bd=10,
    text="EXIT",
    font=("Times", 20, "italic", "bold"),
    justify=CENTER,
    activebackground="red",
    activeforeground="white",
    command=exit,
).place(x=100, y=550)
root.mainloop()
