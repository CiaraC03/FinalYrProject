from tinydb import TinyDB


class ProjectBinDatabase:
    def __init__(self, db_path="/home/ciara/Documents/FinalYrPro/db.json"):
        self.db = TinyDB(db_path) 

    def detection(self, data):
        self.db.insert(data)

    def get_detections(self):  
        return self.db.all()