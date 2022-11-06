import firebase_admin
from firebase_admin import credentials, firestore, db

cred = credentials.Certificate("dataKey.json")
firebase_admin.initialize_app(
    cred, {
        "databaseURL":
        "https://honang-bot-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })

class DataReceiver():
    
    def update(path, data):
        refPath = db.reference(f"{path}")

        refPath.update(data)

    def get(path, data):
        refPath = db.reference(f"{path}")

        return refPath.get()[f"{data}"]

    def check(user):
        refPath = db.reference(f"USERDATA/{user}")

        try: refPath.get()["1_Points"]
        except: return False
        else: return True