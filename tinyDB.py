from tinydb import TinyDB


class ProjectBinDatabase:
    def __init__(self, db_path="/home/ciara/Documents/FinalYrPro/db.json"):
        
        self.db = TinyDB(db_path)

    def insert_detection(self, data):
       
        self.db.insert(data)

    def get_all_detections(self):
        
        return self.db.all()