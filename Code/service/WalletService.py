


class WalletService:
    bal = 0

    def destroy(self):
        self.frame.destroy()


    def __init__(self, user_id,dao):
        self.user_id = user_id
        self.dao = dao


    def get_payment_history(self):
        return self.dao.get_rent_details()

    #def get_current_bal(self):
        #return self.bal

    def recharge_bal(self, val):
        #self.bal += val
        return self.dao.wallet_recharge(val)


    def get_user(self):
        return self.dao.customer_data()

    def update_phone_number(self,phone_val):
        return self.dao.update_user_phone(phone_val)

    def update_email_address(self,email_val):
        return self.dao.update_user_email(email_val)
