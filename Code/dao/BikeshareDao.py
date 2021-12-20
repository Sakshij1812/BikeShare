import sqlite3
from tkinter.messagebox import showerror
import random


class BikeshareDao:

    def __init__(self, user_id):
        self.user_id = user_id
        with sqlite3.connect("bikesharedatabase.db") as db:
            self.db = db


    def __del__(self):
        self.db.close()

    def customer_data(self):
        cursor = self.db.cursor()
        customer_details = []
        print("fetching cust data")
        try:
            customer_details= cursor.execute("""select u.first_name, u.last_name, u.email, u.phone,c.wallet_balance 
            from login_user u, customer c where  u.customer_id = c.id and u. id = ?""",[self.user_id]).fetchone()
            if len(customer_details) > 0:
                return customer_details
            cursor.close()

        except:
            print("oops!user not found")

    def get_rent_details(self):
        cursor = self.db.cursor()
        print("inside getRentdetails")
        cursor.execute("""select bike.bike_number, rental.duration,rental.amount, rental.rental_status, rental.payment_status, rental.start_time
        from login_user, rental, bike 
        where bike.id = rental.bike_id and login_user.customer_id = rental.customer_id and login_user.id = ?  order by rental.start_time desc Limit 5
        """,[self.user_id])
        rentdetails = cursor.fetchall()
        cursor.close()
        return rentdetails


    def get_bike_number(self,bike_number):
        cursor = self.db.cursor()
        print("inside get_bike_number")
        bike_number =  cursor.execute("Select bike_number from bike b where b.bike_number = ?",[bike_number]).fetchone()
        if bike_number:
            bike_number = bike_number[0]
        print("trying to print", bike_number)
        cursor.close()
        return bike_number

    def create_defect_record(self,bike_number,defect_desc):
        #Generate defect_number
        defect_number = 'BKDF'
        number = random.randint(1000, 9999)
        defect_number = defect_number + str(number)

        #cursor creation
        cursor = self.db.cursor()
        print("Inserting record")
        print(type(bike_number))
        bike_details = cursor.execute("select id from bike where bike_number= ?",[bike_number]).fetchone()
        print(bike_details, type(bike_details))
        bike_id = bike_details[0]
        station_id = (cursor.execute("select station_id from bike_status where bike_id = ?", [bike_id]).fetchone())
        if station_id:
            station_id = station_id[0]
        #check open defect
        open_defect_id = cursor.execute("""select id from defect where defect_status in ('open','inprogress') and bike_id =?""", [bike_id]).fetchone()
        if  open_defect_id:
            open_defect_id = open_defect_id[0]
            print("open_defect found",open_defect_id)
            showerror(title="Error", message= "There is already an open defect on this bike.\nFor further assistance please contact our Operators")
            return None
        #Create new if no defect found
        insert_record = """insert into defect(bike_id, defect_found_time,defect_status, station_id, defect_remarks)
        values(?,datetime(), 'open',?, ?)"""
        cursor.execute(insert_record, (bike_id,station_id,defect_desc ))
        defect_id = cursor.execute("select id from defect where bike_id= ?",[bike_id]).fetchone()
        cursor.close()
        self.db.commit()
        print("defect Id",defect_id)
        return defect_id


        #update wallet balance
    def wallet_recharge(self,val):
        print("inside wallet recharge")
        try:
            cursor = self.db.cursor()
            current_wallet_bal = cursor.execute("select wallet_balance from customer where id = (select customer_id from login_user where id = ?)",[self.user_id]).fetchone()
            print(type(current_wallet_bal))
            if current_wallet_bal:
               current_wallet_bal = int(current_wallet_bal[0])
               val =  val+ current_wallet_bal
            else:
                val = val
            cursor.execute("update customer set wallet_balance = ? where id = (select customer_id from login_user where id = ?)",(val,self.user_id))
            self.db.commit()
            cursor.close()
            return cursor.rowcount

        except:
            print("Unable to update your request at the moment.")
            return 0

    def update_user_phone(self,phone_val):
        cursor = self.db.cursor()
        try:
            cursor.execute("update login_user set phone = ? where id = ?",(phone_val,self.user_id))
            self.db.commit()
            return cursor.rowcount, phone_val
            cursor.close()
        except:
            print("unable to update your request at the moment.")
            return 0

    def update_user_email(self,email_val):
        cursor = self.db.cursor()
        try:
            cursor.execute("update login_user set email = ? where id = ?",(email_val,self.user_id))
            self.db.commit()
            return cursor.rowcount, email_val
            cursor.close()
        except:
            print("unable to update your request at the moment.")
            return 0
