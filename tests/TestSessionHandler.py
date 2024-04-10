import unittest
from src.SessionHandler import SessionHandler

class TestSessionHandler(unittest.TestCase):
    def setUp(self) -> None:
        self.session_handler = SessionHandler()
        return super().setUp()
    
    def test_init_user_session(self):
        expected = {
            "user_id":"1",
            "phase":1,
            "command_name":"test"
        }

        self.session_handler.init_user_session("1","test")
        actual = self.session_handler.get_session_obj()[0]

        self.assertEqual(expected["user_id"],actual["user_id"])
        self.assertEqual(expected["phase"],actual["phase"])
        self.assertEqual(expected["command_name"],actual["command_name"])

    def test_is_user_using_sessioned_command(self):
        
        actual = self.session_handler.is_user_using_sessioned_command("1")

        self.assertTrue(actual)

    def test_update_session(self):
        self.session_handler.update_session("1")
        session = self.session_handler.get_session_obj()
        

        self.assertEqual(session[0]["phase"],2)

    def test_remove_user_session(self):
        self.session_handler.remove_user_session("1")
        session = self.session_handler.get_session_obj()
        
        self.assertEqual(0,len(session))
# if __name__ == '__main__':
#     unittest.main()