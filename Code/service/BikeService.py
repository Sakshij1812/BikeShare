
class BikeService:
    def __init__(self, dao):
        self.dao = dao


    def get_bike_number(self,bike_number):
        bike_number = self.dao.get_bike_number(bike_number)
        return bike_number