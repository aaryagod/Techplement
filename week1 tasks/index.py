# DEVELOPED BY Aarya Godbole

from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

root = Tk()
root.title("Contact Management System")
width = 700
height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)
root.config(bg="#fefae0")

# ============================VARIABLES===================================
FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()

# ============================METHODS=====================================

def Database():
    conn = sqlite3.connect("contact.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER NOT NULL  PRIMARY KEY AUTOINCREMENT, firstname TEXT, lastname TEXT, gender TEXT, age TEXT, address TEXT, contact TEXT)")
    cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SubmitData():
    if FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or AGE.get() == "" or ADDRESS.get() == "" or CONTACT.get() == "":
        tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contact.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `member` (firstname, lastname, gender, age, address, contact) VALUES(?, ?, ?, ?, ?, ?)", 
                       (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), ADDRESS.get(), CONTACT.get()))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")

def UpdateData():
    if GENDER.get() == "":
        tkMessageBox.showwarning('', 'Please Complete The Required Field', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contact.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE `member` SET `firstname` = ?, `lastname` = ?, `gender` = ?, `age` = ?, `address` = ?, `contact` = ? WHERE `mem_id` = ?", 
                       (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), ADDRESS.get(), CONTACT.get(), mem_id))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        AGE.set("")
        ADDRESS.set("")
        CONTACT.set("")

def OnSelected(event):
    global mem_id, UpdateWindow
    curItem = tree.focus()
    contents = tree.item(curItem)
    selecteditem = contents['values']
    mem_id = selecteditem[0]
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    GENDER.set(selecteditem[3])
    AGE.set(selecteditem[4])
    ADDRESS.set(selecteditem[5])
    CONTACT.set(selecteditem[6])

    UpdateWindow = Toplevel()
    UpdateWindow.title("Contact Management System")
    width = 400
    height = 300
    x = ((screen_width / 2) + 450) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    UpdateWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    UpdateWindow.resizable(0, 0)

    if 'NewWindow' in globals():
        NewWindow.destroy()

    FormTitle = Frame(UpdateWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(UpdateWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('arial', 14)).pack(side=LEFT)
    Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('arial', 14)).pack(side=LEFT)

    Label(FormTitle, text="Updating Contacts", font=('arial', 16), bg="#f4a261", width=300).pack(fill=X)
    Label(ContactForm, text="Firstname", font=('arial', 14), bd=5).grid(row=0, sticky=W)
    Label(ContactForm, text="Lastname", font=('arial', 14), bd=5).grid(row=1, sticky=W)
    Label(ContactForm, text="Gender", font=('arial', 14), bd=5).grid(row=2, sticky=W)
    Label(ContactForm, text="Age", font=('arial', 14), bd=5).grid(row=3, sticky=W)
    Label(ContactForm, text="Address", font=('arial', 14), bd=5).grid(row=4, sticky=W)
    Label(ContactForm, text="Contact", font=('arial', 14), bd=5).grid(row=5, sticky=W)

    Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14)).grid(row=0, column=1)
    Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14)).grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    Entry(ContactForm, textvariable=AGE, font=('arial', 14)).grid(row=3, column=1)
    Entry(ContactForm, textvariable=ADDRESS, font=('arial', 14)).grid(row=4, column=1)
    Entry(ContactForm, textvariable=CONTACT, font=('arial', 14)).grid(row=5, column=1)

    Button(ContactForm, text="Update", width=50, command=UpdateData).grid(row=6, columnspan=2, pady=10)

def DeleteData():
    if not tree.selection():
        tkMessageBox.showwarning('', 'Please Select Something First!', icon="warning")
    else:
        result = tkMessageBox.askquestion('', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            selecteditem = tree.item(curItem)['values']
            tree.delete(curItem)
            conn = sqlite3.connect("contact.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM `member` WHERE `mem_id` = ?", (selecteditem[0],))
            conn.commit()
            cursor.close()
            conn.close()

def AddNewWindow():
    global NewWindow
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")
    NewWindow = Toplevel()
    NewWindow.title("Contact Management System")
    width = 400
    height = 300
    x = ((screen_width / 2) - 455) - (width / 2)
    y = ((screen_height / 2) + 20) - (height / 2)
    NewWindow.geometry("%dx%d+%d+%d" % (width, height, x, y))
    NewWindow.resizable(0, 0)

    if 'UpdateWindow' in globals():
        UpdateWindow.destroy()

    FormTitle = Frame(NewWindow)
    FormTitle.pack(side=TOP)
    ContactForm = Frame(NewWindow)
    ContactForm.pack(side=TOP, pady=10)
    RadioGroup = Frame(ContactForm)
    Radiobutton(RadioGroup, text="Male", variable=GENDER, value="Male", font=('arial', 14)).pack(side=LEFT)
    Radiobutton(RadioGroup, text="Female", variable=GENDER, value="Female", font=('arial', 14)).pack(side=LEFT)

    Label(FormTitle, text="Adding New Contacts", font=('arial', 16), bg="#f4a261", width=300).pack(fill=X)
    Label(ContactForm, text="Firstname", font=('arial', 14), bd=5).grid(row=0, sticky=W)
    Label(ContactForm, text="Lastname", font=('arial', 14), bd=5).grid(row=1, sticky=W)
    Label(ContactForm, text="Gender", font=('arial', 14), bd=5).grid(row=2, sticky=W)
    Label(ContactForm, text="Age", font=('arial', 14), bd=5).grid(row=3, sticky=W)
    Label(ContactForm, text="Address", font=('arial', 14), bd=5).grid(row=4, sticky=W)
    Label(ContactForm, text="Contact", font=('arial', 14), bd=5).grid(row=5, sticky=W)

    Entry(ContactForm, textvariable=FIRSTNAME, font=('arial', 14)).grid(row=0, column=1)
    Entry(ContactForm, textvariable=LASTNAME, font=('arial', 14)).grid(row=1, column=1)
    RadioGroup.grid(row=2, column=1)
    Entry(ContactForm, textvariable=AGE, font=('arial', 14)).grid(row=3, column=1)
    Entry(ContactForm, textvariable=ADDRESS, font=('arial', 14)).grid(row=4, column=1)
    Entry(ContactForm, textvariable=CONTACT, font=('arial', 14)).grid(row=5, column=1)

    Button(ContactForm, text="Save", width=50, command=SubmitData).grid(row=6, columnspan=2, pady=10)

# ============================FRAMES======================================
Top = Frame(root, width=500, bd=1, relief=SOLID)
Top.pack(side=TOP)
Mid = Frame(root, width=500, bg="#fefae0")
Mid.pack(side=TOP)
MidLeft = Frame(Mid, width=100)
MidLeft.pack(side=LEFT, pady=10)
MidLeftPadding = Frame(Mid, width=370, bg="#fefae0")
MidLeftPadding.pack(side=LEFT)
MidRight = Frame(Mid, width=100)
MidRight.pack(side=RIGHT, pady=10)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)

# ============================LABELS======================================
Label(Top, text="Contact Management System", font=('arial', 16), width=500).pack(fill=X)

# ============================BUTTONS=====================================
Button(MidLeft, text="+ ADD NEW", bg="#f4a261", command=AddNewWindow).pack()
Button(MidRight, text="DELETE", bg="#e63946", command=DeleteData).pack(side=RIGHT)

# ============================TABLE=======================================
scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("MemberID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"),
                    height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbarx.config(command=tree.xview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Firstname', text="Firstname", anchor=W)
tree.heading('Lastname', text="Lastname", anchor=W)
tree.heading('Gender', text="Gender", anchor=W)
tree.heading('Age', text="Age", anchor=W)
tree.heading('Address', text="Address", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=80)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=90)
tree.column('#5', stretch=NO, minwidth=0, width=80)
tree.column('#6', stretch=NO, minwidth=0, width=120)
tree.column('#7', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

# ============================FOOTER======================================
Footer = Frame(root, width=700, bg="#fefae0")
Footer.pack(side=BOTTOM, fill=X)
Label(Footer, text="Developed by Aarya Godbole", font=("arial", 10, "italic"), bg="#fefae0", fg="#555555").pack(pady=5)

# ============================INITIALIZATION==============================
if __name__ == '__main__':
    Database()
    root.mainloop()
