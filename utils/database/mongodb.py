import asyncio

import pymongo

from bson.objectid import ObjectId


class Database:
    def __init__(self, host: str = "localhost", port: int = 27017):
        self.client = pymongo.MongoClient(f"mongodb://{host}:{port}")
        self.table_users = self.client["rksi_parse"]["users"]

    async def add_one_user(self, data: dict):
        self.table_users.insert_one(data)
        print("great!")

    async def get_one_user(self, data: dict) -> None | dict:
        result = self.table_users.find_one(data)
        return result

    async def get_all_users(self) -> list:
        return list(self.table_users.find())

    async def del_one_user(self, data: dict) -> bool:
        try:

            self.table_users.delete_one(data)
            return True

        except Exception as e:
            return False

    async def update_one_user(self, data_to_find: dict, new_data: dict):
        data_to_change: dict = {"$set": new_data}
        self.table_users.update_one(data_to_find, data_to_change)

    def __str__(self):
        return "Class Database return information from database"