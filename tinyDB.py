from tinydb import TinyDB

class ProjectBinDatabase:
    def __init__(self, db_path="/home/ciara/Documents/FinalYrPro/db.json"):
        
        self.db = TinyDB(db_path)

    def insert_detection(self, data):
        """Insert detection data into TinyDB."""
        self.db.insert(data)

    def get_all_detections(self):
        """Retrieve all stored detections."""
        return self.db.all()