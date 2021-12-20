import sys
import os
import tkinter as tk
from tkinter import ttk
from Login import Login
from Operator import Operator
from Manager import Manager
from controller.styles.BaseStyle import BaseStyle
from controller.components.BaseNotebook import BaseNotebook


class App:
    user_id = None
    customer_id = None
    role_id = None
    user_full_name = None

    def mainLoop(self):
        if(self.user_id):
            if self.role_id == 1:
                self.customer_view()
            elif self.role_id == 2:
                self.operator_view()
            elif self.role_id == 3:
                self.manager_view()
        else:
            Login(self).launch_login_window()

    def operator_view(self):
        Operator().launch_operator_window(self.user_id, self.role_id, self.logout_handler)

    def manager_view(self):
        Manager().launch_manager_window(self.user_id, self.role_id, self.logout_handler)

    def customer_view(self):
        self.root = tk.Tk()
        self.root.title("Welcome to Bike Share System")
        self.root.geometry("1500x800")
        if "nt" == os.name:
            self.root.wm_iconbitmap(bitmap="resources/img/bicycle-rider.ico")
        else:
            self.root.wm_iconbitmap(bitmap="@resources/img/bicycle-rider.xbm")
            # root.iconbitmap("resources/img/bicycle-rider.xbm")
        BaseStyle()
        BaseNotebook(self.root, self.user_id, self.user_full_name, self.customer_id, self.logout_handler)
        self.root.mainloop()

    def login_handler(self, login_details):
        self.user_id = login_details[0]
        self.role_id = login_details[1]
        self.user_full_name = f'{login_details[2].capitalize()} {login_details[3].capitalize()}'
        self.customer_id = login_details[4]
        print(f'fetched login user {self.user_id}, role_id {self.role_id} user full name {self.user_full_name}')
        self.mainLoop()

    def logout_handler(self):
        print("Logging out!")
        if self.role_id == 1:
            self.root.destroy()
        self.user_id = None
        self.role_id = None
        self.user_full_name = None
        self.mainLoop()


if __name__ == "__main__":
    App().mainLoop()

