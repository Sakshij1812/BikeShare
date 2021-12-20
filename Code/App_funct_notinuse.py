import tkinter as tk
from tkinter import ttk


def report_defect_frame(notebook):
    report_defect_f = tk.Frame(notebook, width  = 800, height = 800, bg = 'white')
    report_defect_f.pack(fill = "both", expand = 1)
    return report_defect_f


def wallet_frame(notebook):
    wallet_f = tk.Frame(notebook, width  = 800, height = 800, bg = 'white')
    wallet_f.pack(fill = "both", expand = 1)
    Label_wallet = ttk.Label(wallet_f, text = 'Wallet', style = "My.TLabel").grid(column = 10,row = 10, padx = 30,pady = 30)
    
    return wallet_f

def rent_frame(notebook):
    rent_f = tk.Frame(notebook, width  = 800, height = 800, bg = 'white')
    rent_f.pack(fill = "both", expand = 1)
    return rent_f

def tk_notebook(parent):
    notebook = ttk.Notebook(parent)
    notebook.pack(fill = "both",  expand=True)
    notebook.add(rent_frame(notebook), text='Rent/Return')
    notebook.add(report_defect_frame(notebook), text='Report Defect')
    notebook.add(wallet_frame(notebook), text='Wallet')


def root():
    root = tk.Tk()
    root.title("Welcome to Bike Share System")
    root.geometry("1280x720")
    root.iconbitmap("resources/img/bicycle-rider.ico")

    style = ttk.Style()
    style.configure("My.TLabel", foreground="white", background="blue")

    tk_notebook(root)
    root.mainloop()


if __name__ == "__main__":
    root()
