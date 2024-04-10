from . import user_session

class SessionHandler(object):
    def __init__(self):
        pass
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SessionHandler, cls).__new__(cls)
        return cls.instance
    
    def init_user_session(self,user_id:str,command_name):
        session_item = {
            "user_id":user_id,
            "phase":1,
            "command_name": command_name
        }
        user_session.append(session_item)
    
    def remove_user_session(self,user_id:str):
        for session_item in user_session:
            if (user_id == session_item["user_id"]):
                idx = user_session.index(session_item)

                user_session.pop(idx)
                break

    def is_user_using_sessioned_command(self,user_id:str):
        for session_item in user_session:
            if (user_id == session_item["user_id"]):
                return True
            
        return False
    
    def update_session(self,user_id:str):
        session = {}
        idx = 0
        for session_item in user_session:
            if (user_id == session_item["user_id"]):
                session = session_item
                idx = user_session.index(session_item)

        session["phase"] += 1
        session_item[idx] = session

    def get_session_obj(self):
        return user_session