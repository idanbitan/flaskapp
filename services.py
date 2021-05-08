from abc import ABCMeta, abstractmethod
from collections import defaultdict
import requests


class ServiceBase(metaclass=ABCMeta):
    def __init__(self, db):
        self._db = db
        self._db_id = 0

    def get(self, key):
        return self._db[key] if key in self._db else None

    @abstractmethod
    def save(self, key):
        pass

    def fetch(self, key):
        value = self.get(key)
        return value if value is not None else self.save(key)


class PlatformService(ServiceBase):
    def __init__(self):
        super().__init__(defaultdict(int))
        self._db_id = 0

    def save(self, key):
        self._db_id += 1
        print(self._db_id)
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

    def save(self, key, plat_id, dev_bio):
        self._db_id += 1
        self._db[key] = self._db_id
        self._app_db[key] = (plat_id, dev_bio)
        return self._db_id

    def fetch(self, key, plat_id, dev_bio):
        value = self.get(key)
        return value if value is not None else self.save(key, plat_id, dev_bio)

    def get_platform(self, key):
        return self._app_db[key][0]

    def get_developer_bio(self, key):
        return self._app_db[key][1]

    @property
    def get_all(self):
        return self._db.items()


p_service = PlatformService()
d_service = DeveloperService()
a_service = AppService()
