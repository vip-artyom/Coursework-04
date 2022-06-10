from typing import List

from project.exceptions import ItemNotFound


class BaseMixinService:
    def __init__(self, dao):
        self.dao = dao

    def get_one(self, eid: int) -> object:
        entity = self.dao.get_one(eid)
        if not entity:
            raise ItemNotFound
        return entity

    def get_all(self, filters: dict) -> List[dict]:
        entity = self.dao.get_all(filters)
        if not entity:
            raise ItemNotFound
        return entity
