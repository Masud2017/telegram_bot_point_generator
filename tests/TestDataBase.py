import unittest
from src.DataBase import DataBase

class TestSessionHandler(unittest.TestCase):
    def test_get_an_unique_id(self):
       db = DataBase("rediss://127.0.0.1:6379")
       id = db.get_an_unique_box_id()
       self.assertEqual(id,5)