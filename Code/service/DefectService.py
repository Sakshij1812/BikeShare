from dao.BikeshareDao import BikeshareDao
class DefectService:
    def __init__(self, dao):
        self.dao = dao

    def create_defect(self, bike_number, defect_desc):
        return self.dao.create_defect_record(bike_number, defect_desc)


