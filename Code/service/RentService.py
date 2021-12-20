
class RentService:

    def __init__(self, user_id):
        self.user_id = user_id

    def get_existing(self):
        return [
            [123, 'YellowBike', '20 mins', 'station A'],
            [124, 'BlueBike', '20 mins', 'station A'],
            [125, 'GreenBike', '20 mins', 'station A']
        ]
