from abc import ABC, abstractmethod
from collections import defaultdict
import requests

class ServiceBase(object):
    def __init__(self, db):
        self._db = db
        self._db_id = 0
    
    def get(self, key):
        return self._db[key]
        
    @abstractmethod
    def save(self, key):
        pass

    def fetch(self, key):
        return self.get(key) if key in self._db else self.save(key)

class PlatformService(ServiceBase):
    def __init__(self):
        super().__init__(defaultdict(int))
        self._db_id = 0

    def save(self, key):
        self._db_id+=1
        self._db[key] = self._db_id
        return self._db_id
        
class DeveloperService(ServiceBase):
    def __init__(self):
        super().__init__(defaultdict(str))

    def save(self, key):
        # Didnt Use GraphQL because I didn't want to put my token
        response = requests.get('https://api.github.com/users/{developer_name}'.format(developer_name=key))
        bio = response.json()['bio']
        bio = bio if bio is not None else "Bio Is Empty"
        self._db[key] = bio
        return bio

class AppService(ServiceBase):
    def __init__(self):
        super().__init__(defaultdict(int))
        self._db_id = 0
        self._app_db = {}

    def save(self, key, plat_name, dev_bio):
        self._db_id+=1
        self._db[key] = self._db_id
        self._app_db[key] = (plat_name, dev_bio)
        return self._db_id

    def fetch(self, key, plat_name, dev_bio):
        return self.get(key) if key in self._db else self.save(key, plat_name, dev_bio)

    def get_platform(self, key):
        return self._app_db[key][0]

    def get_developer_bio(self, key):
        return self._app_db[key][1]

p_service = PlatformService()
d_service = DeveloperService()
a_service = AppService()