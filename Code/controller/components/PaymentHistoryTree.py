import tkinter as tk
from tkinter import ttk


class PayTree:
    cols = ['Bike Number', 'Duration', 'Amount', 'rental status','Payment Status','Start Time']

    def __init__(self, parent, payment_hist):
        self.parent = parent

        tree_height = len(payment_hist)
        self.tree = ttk.Treeview(
            parent.frame, columns=self.cols, show='headings', height=tree_height, selectmode = "extended" )
        self.tree.tag_configure('evenrow', background = '#E2F0CB')
        self.tree.tag_configure('oddrow', background = '#B5EAD7')
        



        for col in self.cols:
            self.tree.heading(col, text=col)

        for payment in payment_hist:
            self.tree.insert("", "end", values=payment)
