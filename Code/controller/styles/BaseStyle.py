import tkinter
from tkinter import ttk

class BaseStyle:
    def __init__(self):
        #super().__init__()
        style = ttk.Style()
        print(style.theme_names())
        style.theme_use('clam')
        style.configure("Treeview", background="#b5d9ea",
                        foreground="black",
                        rowheight=35
                        , fieldbackground="#b5d9ea")
        style.map('Treeview', background=[('selected', "#1788CC")], foreground=[('selected', "white")],
                  font=[('selected', ("Helvetica, Arial, FreeSans", 20))])

        #Textbox style
        style.configure('TEntry', foreground = 'black',background ='#FFCCBC' , font = ('Helvetica,Arial,FreeSans', 10, 'bold'))
        #Label style
        style.configure('TLabel', font=('Helvetica,Arial,FreeSans', 8, 'bold'), justify = 'center')

        #Buttons style

        style.configure('TButton',  relief = 'raised',
                        width = 10, borderwidth = 2, focusthickness = 3, focuscolor = '#4091c2',font = ('Helvetica,Arial,FreeSans', 10, 'bold')
                         )
        style.map('TButton',
                  foreground=[('!active', 'white'), ('pressed', 'black'), ('active', 'white')],
                  background=[('!active',  '#1788CC'),('pressed', '#4091c2'), ('active', '#4091c2')])

