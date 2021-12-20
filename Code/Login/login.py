"""
@author Harry
"""

from tkinter import *
from tkinter import messagebox
import sqlite3
import subprocess
import re

with sqlite3.connect("../Database/bikesharedatabase.db") as db:
    cursor = db.cursor()


def login(username, password, login_window):
    cursor.execute("SELECT EXISTS(SELECT 1 FROM login_user WHERE user_name = ? AND pwd = ?)", [username, password])
    [exists] = cursor.fetchone()
    if exists:
        cursor.execute("SELECT user_status FROM login_user WHERE user_name = ? AND pwd = ?", [username, password])
        if cursor.fetchone()[0] == "active":
            login_details = cursor.execute("SELECT id, login_role_id FROM login_user WHERE user_name = ? AND pwd = ?",
                                           [username, password]).fetchone()
            global logged_in_user_id
            logged_in_user_id = login_details[0]
            login_window.destroy()
            {1: subprocess.call(["python", "../Customer_View_Rent_Return/customer_view_rent_return.py"]),
             2: subprocess.call(["python", "../Operator View/operator.py"]),
             3: subprocess.call(["python", "../Manager View/manager_view.py"])}.get(login_details[1])

        else:
            messagebox.showwarning(title="Error", message="User is suspended")
    else:
        messagebox.showwarning(title="Error", message="Username/password incorrect")


def register(first_name, last_name, email, phone, username, password, register_window):
    if first_name == "" or last_name == "" or email == "" or phone == "" or username == "" or password == "":
        messagebox.showwarning(title="Error", message="Please make sure all fields are filled")
    if len(phone) != 10:
        messagebox.showwarning(title="Error", message="Phone number must be 10 numbers in length")
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if not re.fullmatch(regex, email):
        messagebox.showwarning(title="Error", message="Invalid email address")
    else:
        cursor.execute("SELECT EXISTS(SELECT 1 FROM login_user WHERE user_name = ? OR email = ? OR phone = ?)",
                       [username, email, phone])
        [exists] = cursor.fetchone()
        if exists:
            messagebox.showwarning(title="Error", message="Non-unique details entered")
        else:
            cursor.execute(
                "INSERT INTO login_user (user_name, pwd, login_role_id, first_name, last_name, email, phone, "
                "user_status) "
                "VALUES (?, ?, 1, ?, ?, ?, ?, 'active')", [username, password, first_name, last_name, email, phone])
            db.commit()
            messagebox.showinfo(title="Success", message="Customer successfully registered")
            register_window.destroy()
            launch_login_window()


def launch_register_window():
    register_window = Tk()

    first_name_lbl = Label(register_window, text="Please enter your first name:")
    last_name_lbl = Label(register_window, text="Please enter your last name:")
    email_lbl = Label(register_window, text="Please enter your email:")
    phone_lbl = Label(register_window, text="Please enter your phone number:")
    username_lbl = Label(register_window, text="Please choose a username:")
    password_lbl = Label(register_window, text="Please choose a password:")

    first_name = Entry(register_window, bd=5)
    last_name = Entry(register_window, bd=5)
    email = Entry(register_window, bd=5)
    phone = Entry(register_window, bd=5)
    username = Entry(register_window, bd=5)
    password = Entry(register_window, show="*", bd=5)

    register_btn = Button(register_window, text="Register",
                          command=lambda: register(first_name.get(), last_name.get(), email.get(), phone.get(),
                                                   username.get(),
                                                   password.get(), register_window))

    first_name_lbl.grid(row=1, column=1)
    first_name.grid(row=1, column=3)
    last_name_lbl.grid(row=2, column=1)
    last_name.grid(row=2, column=3)
    email_lbl.grid(row=3, column=1)
    email.grid(row=3, column=3)
    phone_lbl.grid(row=4, column=1)
    phone.grid(row=4, column=3)
    username_lbl.grid(row=5, column=1)
    username.grid(row=5, column=3)
    password_lbl.grid(row=6, column=1)
    password.grid(row=6, column=3)
    register_btn.grid(row=7, column=2)
    register_window.grid_rowconfigure((0, 14), weight=1)
    register_window.grid_columnconfigure((0, 4), weight=1)

    register_window.title("Register")
    register_window.geometry("500x500")

    register_window.mainloop()


def launch_login_window():
    login_window = Tk()

    username_lbl = Label(login_window, text="Please enter your username:")
    password_lbl = Label(login_window, text="Please enter your password:")

    username = Entry(login_window, bd=5)
    password = Entry(login_window, show="*", bd=5)

    login_btn = Button(login_window, text="Login",
                       command=lambda: [login(username.get(), password.get(), login_window)])
    register_btn = Button(login_window, text="Register",
                          command=lambda: [login_window.destroy(), launch_register_window()])

    username_lbl.grid(row=1, column=1, sticky="")
    username.grid(row=1, column=3, sticky="")
    password_lbl.grid(row=2, column=1, sticky="")
    password.grid(row=2, column=3, sticky="")
    login_btn.grid(row=3, column=2, sticky="")
    register_btn.grid(row=4, column=2, sticky="")

    login_window.grid_rowconfigure((0, 6), weight=1)
    login_window.grid_columnconfigure((0, 4), weight=1)

    login_window.title("Login")
    login_window.geometry("500x500")
    # login_window.attributes("-fullscreen", True)
    login_window.mainloop()


if __name__ == "__main__":
    launch_login_window()
    db.close()
