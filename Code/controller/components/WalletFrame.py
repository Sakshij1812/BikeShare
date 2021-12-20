import time
import tkinter as tk
from tkinter import ttk

import service.py_utilities
from controller.components.PaymentHistoryTree import PayTree
from tkinter.messagebox import *
from service.py_utilities import *
import datetime

class WalletFr:


    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent.notebook, width=800, height=800, bg='white')
        self.frame.pack(fill="both", expand=1)


        self.bal = tk.StringVar()

        self.update_state_val = tk.StringVar()


        # pull data from data layer
        user_details = self.populate_user_details()
        if(self.populate_user_details()):
            if len(user_details) > 0:
                u_name = str(user_details[0]).capitalize() + " "+str(user_details[1]).capitalize()
                email = user_details[2]

                wallet_balance = str(user_details[4])
                phone_number = user_details[3]
        else:
            showerror(title  = "Error", message= "user not found")
            return None


        greeting_label_frame = ttk.LabelFrame(self.frame, text = "Hey "+u_name+", ")
        now = datetime.datetime.now()
        
        #to display different greetings based on time of the day
        text = None
        if now.hour >= 5 and now.hour <= 11:
            text="Good Morning! 🌞"
        elif now.hour >= 12 and now.hour <= 16:
            text="Good Afternoon! ☀️"
        elif now.hour >= 17 and now.hour <= 20:
            text="Good Evening! 🌅"
        else:
            text="Its a lovely night! 🌙"
        
        text = text + "\n\nWelcome to BikeShare system!"
        greeting_label = ttk.Label(greeting_label_frame, text=text, width=30)
        greeting_label.grid(column = 0, row = 0,  padx = 110, pady = 30, sticky = tk.W, columnspan = 30)
        greeting_label_frame.grid(column = 0, row = 0, padx = 30, pady = 30, sticky = tk.W, columnspan = 30)
        
        # #greetuser
        # greetings = "Dear {} greetings from BikeShare System ! Your Profile below".format(u_name)
        # wish_user = ttk.Label(self.frame, padding = 10, text = greetings, width = 52, foreground = '#4091c2')
        # wish_user.grid(column = 0, row = 0, padx = 30, pady = 30, sticky = tk.W, columnspan = 10)

        #map controls
        Name = ttk.Label(self.frame, padding=10, text = "Name:", width = 10)
        Name.grid(column=0, row=1,  padx=30, pady=20,sticky=tk.W)

        Name_val = ttk.Label(self.frame, width=30, foreground = "#000000", text = u_name)
        Name_val.grid(column=1, row=1,  padx=30, pady=20,sticky=tk.E, ipady = 7)

        Email = ttk.Label(self.frame, padding=10, text = "Email:", width = 10)
        Email.grid(column=0, row=2,  padx=30, pady=20,sticky=tk.W)

        self.Email_val = ttk.Label(self.frame, width = 30,foreground = "#000000", text = email)
        self.Email_val.grid(column=1, row=2,  padx=30, pady=20,sticky=tk.E, ipady = 7)

        update_email = ttk.Button(self.frame, text="Update email", command=lambda: self.create_popup("Update email"), width = 13)
        update_email.grid(column=4, row=2, padx=30, pady=20, sticky=tk.W)

        phone = ttk.Label(self.frame, padding=10, text = "phone:", width = 10)
        phone.grid(column=0, row=3,  padx=30, pady=20,sticky=tk.W)

        self.phone_val = ttk.Label(self.frame, width=30,foreground = "#000000", text = phone_number)
        self.phone_val.grid(column=1, row=3,  padx=30, pady=20,sticky=tk.E, ipady = 7)

        update_phone =ttk.Button(self.frame, text="Update phone", command=lambda: self.create_popup("Update phone"), width = 13)
        update_phone.grid(column=4, row=3, padx=30, pady=20, sticky=tk.W)

        balance_label = ttk.Label(self.frame, text="Balance:", padding=10, width = 10)
        balance_label.grid(column=0, row=4, padx=30, pady=20, sticky=tk.W)

        self.balance_val = ttk.Label(self.frame,width = 30,foreground = "#000000", text = '£'+wallet_balance)
        self.balance_val.grid(column=1, row=4, sticky=tk.E,  padx=30, pady=20, ipady = 7)

        #padding removed to align button size
        recharge_button = ttk.Button(self.frame, text="Recharge", command=lambda: self.create_popup("Recharge"),width = 13)
        recharge_button.grid(column=4, row=4, padx=30, pady=20, sticky=tk.W)


        #table_label = ttk.Label(self.frame, padding = 10, width = 30, foreground = '#000000', background = '#FFFFFF')
        #table_label.grid(column = 0, row = 5, sticky = tk.SW,columnspan = 10)

        table_label = ttk.Label(self.frame, padding= 10,text = "Latest Trips", width = 30, foreground = '#000000', background = '#b5d9ea')
        table_label.grid(column = 0, row = 6, padx = 30, sticky = tk.SW,columnspan = 10)

        def timed_refresh(self):
            # this after statement is set for every 6 seconds
            self.after(600, self.timed_refresh)
            self.refresh()


        payment_hist = self.parent.get_rent_history()
        pay_tree = PayTree(self, payment_hist)
        pay_tree.tree.grid(column=0, row=7, padx=30, pady=30, sticky=tk.W, columnspan = 30)

    def refresh_data(self):
        user_details = self.populate_user_details()
        wallet_balance = str(user_details[4])
        self.balance_val.configure(text = '£'+ wallet_balance)
        self.balance_val.update()

    def populate_user_details(self):
        customer_details = self.parent.get_current_user_details()
        return customer_details

    def create_popup(self,windowtitle):
        self.popup = tk.Toplevel(self.frame)
        self.popup.geometry("500x500")
        self.popup.title(windowtitle)
        if windowtitle == 'Recharge' :
            balance_label = ttk.Label(self.popup, text="Amount:", padding=10)
            recharge_button = ttk.Button(self.popup, text="Recharge", padding=7, command=self.recharge_popup_handler)
        elif windowtitle == 'Update email':
            balance_label = ttk.Label(self.popup, text="email:", padding=10)
            recharge_button = ttk.Button(self.popup, text="Update", padding=7, command=self.update_email)
        else:
            balance_label = ttk.Label(self.popup, text="phone:", padding=10)
            recharge_button = ttk.Button(self.popup, text="Update", padding=7, command=self.update_phone)
        balance_label.grid(column=0, row=0, padx=30, pady=30, sticky=tk.W)
        recharge_button.grid(column=0, row=1, padx=30, pady=30, sticky=tk.W)
        self.popup_field = ttk.Entry(self.popup)
        self.popup_field.grid(column=1, row=0, sticky=tk.E,  padx=30, pady=30)


    def recharge_popup_handler(self):
        popup_field_val = self.popup_field.get()
        print(popup_field_val)
        print((popup_field_val))
        isfloat = service.py_utilities.check_double_Values(popup_field_val)
        is_non_numeric = service.py_utilities.check_if_only_numeric_values(popup_field_val)
        print("what is this ", isfloat, is_non_numeric)
        if (isfloat or is_non_numeric) and popup_field_val != "":
            self.popup.destroy()
            updated_row_count = self.parent.recharge_wallet(float(popup_field_val))
            if updated_row_count:
                showinfo(title = "Info", message= "Recharge successful")
            else:
                showinfo(title = "Info", message= "Unable to complete action at the moment")
                return None
            #populate updated values
            updated_user_details = self.populate_user_details()
            if updated_user_details:
                bal = str(updated_user_details[4])
            self.balance_val.configure(text = '£'+ bal)
            self.balance_val.update()
        else:
            showerror(title="Error", message="Recharge amount cannot be non numeric value")
            self.popup.destroy()
            return None

    #update phone details
    def update_phone(self):
        phone_val = self.popup_field.get()
        #empty field validation
        if phone_val == "":
            showerror(title="Error", message="phone number cannot be empty")
            return None

        #phone number length validation
        msg = service.py_utilities.check_phone_length(phone_val)
        if msg != "":
            showerror(title= "Error", message= msg)
            return None

        # non numeric validation
        is_non_number = service.py_utilities.check_if_only_numeric_values(phone_val)
        if is_non_number != 1:
            print(phone_val)
            self.popup.destroy()
            rowcount,updated_phone_val= self.parent.update_phone(phone_val)
            if rowcount >= 0:
                self.phone_val.configure(text = updated_phone_val)
                self.phone_val.update()
                showinfo(title= "Info", message = "Phone number is updated successfully")
        else:
            showerror(title= "Error", message= "Phone number cannot be non numeric value")
            self.popup.destroy()
            return None

    #upadte email address
    def update_email(self):
        email_val = self.popup_field.get()
        if email_val == "":
            showerror(title= "Error", message= "email address cannot be empty")
            return None
        isValid_email = service.py_utilities.check_email(email_val)
        if isValid_email == 1:
            print(email_val)
            self.popup.destroy()
            rowcount, updated_email_val = self.parent.update_email(email_val)
            if rowcount >= 0:
                self.Email_val.configure(text=updated_email_val)
                self.Email_val.update()
                showinfo(title="Info", message="email address is updated successfully")
        else:
            showerror(title="Error", message="please enter a valid email id")
            self.popup.destroy()
            return None
