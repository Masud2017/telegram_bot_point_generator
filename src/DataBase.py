import redis

class DataBase:
    def __init__(self,url):
        self.db = redis.from_url(url)
        
