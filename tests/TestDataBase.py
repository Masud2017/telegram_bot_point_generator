import unittest
from src.DataBase import DataBase

class TestSessionHandler(unittest.TestCase):
    # def test_get_an_unique_id(self):
    #    db = DataBase("rediss://127.0.0.1:6379")
    #    id = db.get_an_unique_box_id()
    #    self.assertEqual(id,8)


    def test_get_user_by_id(self):
        db = DataBase("rediss://127.0.0.1:6379")
        user_obj = db.get_user_by_user_id("5594221540")
        print(user_obj)

        self.assertEqual("Masuf", user_obj["first_name"], "User name is not matched.")