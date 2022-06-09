from sqlalchemy import desc
from sqlalchemy.orm.scoping import scoped_session

from project import BaseConfig


class BaseMixinDAO:

    def __init__(self, session: scoped_session, model):
        self.session = session
        self.model = model

    def get_one(self, eid):

        return self.session.query(self.model).get(eid)

    def get_all(self, filters):

        entity = self.session.query(self.model)

        if filters["status"] == "new":
            entity = entity.order_by(desc(self.model.year))

        if filters["page"] is not None:
            entity = entity.limit(BaseConfig.ITEMS_PER_PAGE).\
                offset(int(filters["page"]) * BaseConfig.ITEMS_PER_PAGE - BaseConfig.ITEMS_PER_PAGE)
        else:
            entity = self.session.query(self.model)
        return entity.all()
