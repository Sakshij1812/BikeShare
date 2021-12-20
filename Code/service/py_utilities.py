import re
import sqlite3
from tkinter.messagebox import showerror, showinfo


def check_spl_character(text):
    spl_chars_to_check = re.compile(r'[@"!£$%^&*()#/\}{`¬:;|]')
    if spl_chars_to_check.search(text):
        return 1


def check_if_only_numeric_values(val):

    if re.fullmatch(r'\d', val):
        return 1


def check_email(val):
    expression = r'\b[A-Za-z0-9.%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if re.fullmatch(expression, val):
        return 1




def check_double_Values(val):

    expression = r'(\d+\.)*\d+'
    if re.fullmatch(expression, val):
        return 1



def check_phone_length(val):
    if len(val) != 10:
        msg = "Please enter 10 digit mobile number"
    else:
        msg = ""
    return msg




def pay_rental(rent_id):
    with sqlite3.connect("bikesharedatabase.db") as db:
        cursor = db.cursor()
        rental_query = """select r.customer_id,r.rental_status,r.amount,r.payment_status,c.wallet_balance from rental r, customer c
                   where r.customer_id = c.id and r.id = ?"""
        customer_id, rental_status,rent_amount, payment_status, wallet_balance = cursor.execute(rental_query, [rent_id]).fetchone()

        if (rent_amount > 0 and payment_status == 'calculated' and rental_status == 'complete'):
            wallet_balance = wallet_balance- rent_amount
            print((wallet_balance))
            updated_payment_status = 'paid'
            try:
                if(wallet_balance <= -10):
                    showinfo(title = "Warning", message= "your wallet balance is below allowed limit, please recharge soon to avoid account suspension")
                cursor.execute("update customer set wallet_balance = ? where id = ?",[wallet_balance,customer_id])
                print(cursor.rowcount)
                if cursor.rowcount > 0:
                    cursor.execute("update rental set payment_status =? where id =?",[updated_payment_status,rent_id])
                    db.commit()
                    showinfo(title="Info", message="payment is complete")
                else:
                    showerror(title = "Error",message="sorry,unable to complete payment process")
                    return None
            except Exception as e:
                print(e)
                showerror(title = "Error", message= "There is some issue with the payment, please contact one of our operator.")
                return None
if __name__ == "__main__":
    check_if_only_numeric_values('7')
