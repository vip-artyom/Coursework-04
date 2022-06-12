from typing import List

from flask import current_app
from sqlalchemy import desc
from sqlalchemy.orm.scoping import scoped_session


class BaseMixinDAO:

    def __init__(self, session: scoped_session, model):
        self.session = session
        self.model = model

    def get_one(self, eid: int) -> object:

        return self.session.query(self.model).get(eid)

    def get_all(self, filters: dict) -> List[dict]:

        entity = self.session.query(self.model)

        if filters["status"] == "new":
            entity = entity.order_by(desc(self.model.year))

        if filters["page"] is not None:
            entity = entity.limit(current_app.config.get('ITEMS_PER_PAGE')).\
                offset(int(filters["page"]) * current_app.config.get('ITEMS_PER_PAGE')
                       - current_app.config.get('ITEMS_PER_PAGE'))

        return entity.all()
