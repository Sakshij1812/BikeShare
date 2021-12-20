import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter.messagebox import showerror, showinfo
import service.py_utilities
from service.py_utilities import *
class ReportDefectFr:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent.notebook, width=800, height=800, bg='white')
        self.frame.pack(fill="both", expand=1)

        bike_number = ttk.Label(self.frame, text="Bike number:", padding=10, style = 'TLabel')
        bike_number.grid(column=0, row=10, padx=30, pady=10, sticky=tk.W)

        self.bike_number_field = ttk.Entry(self.frame, style = 'TEntry', width = 42)
        self.bike_number_field.grid(column = 1, row = 10, padx = 30, pady = 30, sticky = tk.W, ipady = 6, ipadx = 20)

        defect_desc = ttk.Label(self.frame, text = "Defect \n description:", padding = 10, style = 'TLabel')
        defect_desc.grid(column= 0, row = 11, padx = 30, pady = 30,sticky=tk.W)

        self.defect_desc_field = scrolledtext.ScrolledText(self.frame, wrap = tk.WORD, width = 40, height = 10, font = ('Helvetica', 10))
        self.defect_desc_field.grid(column= 1, row = 11, padx = 30, pady = 30, sticky = tk.E)

        button_ok = ttk.Button(self.frame, text="Submit", padding=10, command = self.handle_submit)
        button_ok.grid(column= 0, row = 60,sticky = tk.SW,padx = 30, pady = 150)

        button_cancel = ttk.Button(self.frame, text="Clear", padding=10, command = self.clear_data, )
        button_cancel.grid(column= 1, row = 60, padx = 30, pady = 150)





    def handle_submit(self):
        bike_number = self.bike_number_field.get()
        if service.py_utilities.check_if_only_numeric_values(bike_number) == 1:
            showerror(title = "Error", message= "Please enter only numeric values from 0-9")
            self.bike_number_field.delete(0,tk.END)
            return None

        defect_desc = self.defect_desc_field.get('1.0',tk.END)
        defect_desc = str(defect_desc).strip()
        if (not defect_desc) or len(str(defect_desc)) == 0:
            showerror(title = "Error", message= "Defect description cannot be empty")
            return None
        if len(str(defect_desc)) > 200:
            showerror(title = "Error", message= "Please limit the description to 200 characters")
            return None
        bike_number = self.parent.get_bike(bike_number)
        if not bike_number:
            showerror(title= "Error", message= "Bike record not found, please check the number again")
            return None
        print(type(bike_number))
        defect_id = self.parent.create_defect(bike_number,defect_desc)
        if defect_id:
            showinfo(title= "info", message= "Defect logged in our system")
            msg = "Sorry for the inconvenience. We are now working on your complaint!\nFor any further assistance, please reachout to our operators"
            msg_label = ttk.Label(self.frame, text= msg,style='TLabel', foreground = 'green', font = ('Helvetica', 10, 'bold'))
            msg_label.grid(row = 100, column = 0, sticky  = tk.SW, columnspan=4, padx = 30)





        # defect
    def clear_data(self):
        self.bike_number_field.delete(0, tk.END)
        self.defect_desc_field.delete('1.0',tk.END)
