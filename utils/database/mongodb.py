import pymongo


class Database:
    def __init__(self, host: str = "localhost", port: int = 27017):
        self.client = pymongo.MongoClient(f"mongodb://{host}:{port}")
        self.table_users = self.client["rksi_parse"]["users"]

    def add_one_user(self, data: dict):
        self.table_users.insert_one(data)
        print("great!")

    def get_one_user(self, data: dict) -> None:
        try:
            self.table_users.select_one(data)
        except TypeError as te:
            return None

    def get_all_users(self) -> list:
        return list(self.table_users.find())

    def del_one_user(self, data: dict):
        self.table_users.delete_one(data)

    def update_one_user(self, data_to_find: dict, new_data: dict):
        data_to_change: dict = {"$set": new_data}
        self.table_users.update_one(data_to_find, data_to_change)

    def __str__():
        return "Class Database return information from database"