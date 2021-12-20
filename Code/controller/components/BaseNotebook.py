import tkinter as tk
from tkinter import ttk
from controller.components.ReportDefectFrame import ReportDefectFr
from controller.components.RentFrame import RentFr
from controller.components.WalletFrame import WalletFr
from service.WalletService import WalletService
from service.RentService import RentService
from dao.BikeshareDao import BikeshareDao
from service.DefectService import DefectService
from service.BikeService import BikeService


class BaseNotebook:
    def __init__(self, root, user_id, user_full_name, customer_id, logout_handler):
        self.user_id = user_id
        self.user_full_name = user_full_name
        self.customer_id = customer_id
        self.dao = BikeshareDao(user_id)
        self.wallet_service = WalletService(self.user_id, self.dao)
        self.rent_service = RentService(self.user_id)
        self.defect_service = DefectService(self.dao)
        self.bike_service = BikeService(self.dao)

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both",  expand=True)
        self.set_frames()
        logout_button = ttk.Button(self.notebook, text="Logout", width = 13, command=logout_handler)
        logout_button.grid(column=2, row=4, padx=1250, pady=60, sticky=tk.E)

        self.notebook.bind("<ButtonRelease-1>", self.test);

    def set_frames(self):
        self.wallet_fr = WalletFr(self)
        self.report_defect_fr = ReportDefectFr(self)
        self.rent_fr = RentFr(self, self.user_id, self.user_full_name, self.customer_id)
        self.notebook.add(self.rent_fr.frame, text='Rent/Return')
        self.notebook.add(self.report_defect_fr.frame, text='Report Defect')
        self.notebook.add(self.wallet_fr.frame, text='My Account')

    
    def test(self, *args):
        print("yyoooooasd askdjaklsjdklasjd", args)
        if self.wallet_fr :
            self.wallet_fr.refresh_data()
        if self.rent_fr:
            self.rent_fr.refresh_data()

    def get_rent_history(self):
        return self.wallet_service.get_payment_history()

    def get_current_wallet_bal(self):
        return self.wallet_service.get_current_bal()

    def recharge_wallet(self, val):
        return self.wallet_service.recharge_bal(val)

    def get_existing_rents(self):
        return self.rent_service.get_existing()

    def get_bike(self, bike_number):
        return self.bike_service.get_bike_number(bike_number)

    def create_defect(self, bike_number, defect_desc):
        return self.defect_service.create_defect(bike_number, defect_desc)

    def get_current_user_details(self):
        return self.wallet_service.get_user()

    def update_phone(self, phone_val):
        return self.wallet_service.update_phone_number(phone_val)

    def update_email(self, email_val):
        return self.wallet_service.update_email_address(email_val)
