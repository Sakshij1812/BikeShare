"""
@author Harry
"""

from tkinter import *
from tkinter import messagebox
import sqlite3
import re
import os



class Login:
    def __init__(self, parent):
        with sqlite3.connect("bikesharedatabase.db") as db:
            self.cursor = db.cursor()
            self.db = db
            self.parent = parent

    def login(self, username, password, login_window):
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM login_user WHERE user_name = ? AND pwd = ?)",
                            [username, password])
        [exists] = self.cursor.fetchone()
        if exists:
            self.cursor.execute("SELECT user_status FROM login_user WHERE user_name = ? AND pwd = ?",
                                [username, password])
            if self.cursor.fetchone()[0] == "active":
                login_details = self.cursor.execute(
                    "SELECT id, login_role_id, first_name, last_name, customer_id FROM login_user WHERE user_name = ? AND pwd = ?",
                    [username, password]).fetchone()
                global logged_in_user_id
                logged_in_user_id = login_details[0]
                login_window.destroy()

                self.cursor.close()
                self.db.close()
                self.parent.login_handler(login_details)
                # {1: subprocess.call(["python", "../Customer_View_Rent_Return/customer_view_rent_return.py"]),
                # 2: subprocess.call(["python", "../Operator View/operator.py"]),
                # 3: subprocess.call(["python", "../Manager View/manager_view.py"])}.get(login_details[1])

            else:
                messagebox.showwarning(title="Error", message="User is suspended")
        else:
            messagebox.showwarning(title="Error", message="Username/password incorrect")

    def register(self, first_name, last_name, email, phone, username, password, role, register_window):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if first_name == "" or last_name == "" or email == "" or phone == "" or username == "" or password == "":
            messagebox.showwarning(title="Error", message="Please make sure all fields are filled")
        elif len(phone) != 10:
            messagebox.showwarning(title="Error", message="Phone number must be 10 numbers in length")
        elif not phone.isdecimal():
            messagebox.showwarning(title="Error", message="Phone number must only contain digits")
        elif not re.fullmatch(regex, email):
            messagebox.showwarning(title="Error", message="Invalid email address")
        elif len(password) < 6 :
            messagebox.showerror(title= "Error", message= "Password cannot be less than 6 characters long")
        else:
            self.cursor.execute("SELECT EXISTS(SELECT 1 FROM login_user WHERE user_name = ? OR email = ? OR phone = ?)",
                                [username, email, phone]
                                )
            [exists] = self.cursor.fetchone()
            if exists:
                messagebox.showwarning(title="Error", message="Non-unique details entered")
            else:
                if role == "Customer":
                    self.cursor.execute("INSERT INTO customer (wallet_balance,name) VALUES (0,?)",[first_name])
                    self.db.commit()
                    self.cursor.execute("SELECT seq FROM sqlite_sequence WHERE name='customer'")
                    customer_id = int(self.cursor.fetchone()[0])
                    self.cursor.execute(
                        "INSERT INTO login_user (user_name, pwd, login_role_id, first_name, last_name, email, phone, "
                        "customer_id, user_status) "
                        "VALUES (?, ?, 1, ?, ?, ?, ?, ?, 'active')",
                        [username, password, first_name, last_name, email, phone, customer_id])
                    self.db.commit()
                    messagebox.showinfo(title="Success", message=f"Customer successfully registered")
                elif role == "Operator":
                    self.cursor.execute(
                        "INSERT INTO login_user (user_name, pwd, login_role_id, first_name, last_name, email, phone, "
                        "customer_id, user_status) "
                        "VALUES (?, ?, 2, ?, ?, ?, ?, null, 'new')",
                        [username, password, first_name, last_name, email, phone])
                    self.db.commit()
                    messagebox.showinfo(title="Success", message=f"Operator approval request sent to Management")

                register_window.destroy()
                self.launch_login_window()

    def launch_register_window(self, ):
        register_window = Tk()
        if "nt" == os.name:
            register_window.wm_iconbitmap(bitmap="resources/img/bicycle-rider.ico")
        else:
            register_window.wm_iconbitmap(bitmap="@resources/img/bicycle-rider.xbm")
        first_name_lbl = Label(register_window, text="Please enter your first name:")
        last_name_lbl = Label(register_window, text="Please enter your last name:")
        email_lbl = Label(register_window, text="Please enter your email:")
        phone_lbl = Label(register_window, text="Please enter your phone number:")
        username_lbl = Label(register_window, text="Please choose a username:")
        password_lbl = Label(register_window, text="Please choose a password:")
        role_lbl = Label(register_window, text="Please select a role:")

        first_name = Entry(register_window, bd=5)
        last_name = Entry(register_window, bd=5)
        email = Entry(register_window, bd=5)
        phone = Entry(register_window, bd=5)
        username = Entry(register_window, bd=5)
        password = Entry(register_window, show="*", bd=5)
        role_options = ["Customer", "Operator"]
        var = StringVar(register_window)
        var.set(role_options[0])
        role = OptionMenu(register_window, var, *role_options)

        register_btn = Button(register_window, text="Register",
                              command=lambda: self.register(first_name.get(), last_name.get(), email.get(), phone.get(),
                                                            username.get(),
                                                            password.get(), var.get(), register_window))
        back_to_login_btn = Button(register_window, text="Back to login",
                                   command=lambda: [register_window.destroy(), self.launch_login_window()])

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
        role_lbl.grid(row=7, column=1)
        role.grid(row=7, column=3)
        register_btn.grid(row=8, column=2)
        back_to_login_btn.grid(row=9, column=2)
        register_window.grid_rowconfigure((0, 18), weight=1)
        register_window.grid_columnconfigure((0, 4), weight=1)

        register_window.title("Register")
        register_window.geometry("1500x800")

        register_window.mainloop()

    def launch_login_window(self, ):
        login_window = Tk()
        if "nt" == os.name:
            login_window.wm_iconbitmap(bitmap="resources/img/bicycle-rider.ico")
        else:
            login_window.wm_iconbitmap(bitmap="@resources/img/bicycle-rider.xbm")
        username_lbl = Label(login_window, text="Please enter your username:")
        password_lbl = Label(login_window, text="Please enter your password:")

        username = Entry(login_window, bd=5)
        password = Entry(login_window, show="*", bd=5)

        login_btn = Button(login_window, text="Login", width = 10,
                           command=lambda: [self.login(username.get(), password.get(), login_window)])
        register_btn = Button(login_window, text="Register", width = 10,
                              command=lambda: [login_window.destroy(), self.launch_register_window()])

        username_lbl.grid(row=1, column=1, sticky="")
        username.grid(row=1, column=3, sticky="")
        password_lbl.grid(row=2, column=1, sticky="")
        password.grid(row=2, column=3, sticky="")
        login_btn.grid(row=3, column=2, sticky="")
        register_btn.grid(row=4, column=2, sticky="")

        login_window.grid_rowconfigure((0, 6), weight=1)
        login_window.grid_columnconfigure((0, 4), weight=1)

        login_window.title("Login")
        login_window.geometry("1500x800")
        # login_window.attributes("-fullscreen", True)
        login_window.mainloop()
