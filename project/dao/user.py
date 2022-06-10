from project.dao.base import BaseMixinDAO
from project.dao.models import User


class UserDAO(BaseMixinDAO):

    def get_user_by_email(self, email: str) -> object:
        try:
            user = self.session.query(User).filter(User.email == email).one()

            return user

        except Exception as e:

            return print(e)

    def create_user(self, user_data: dict) -> object:
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        self.session.close()
        return user

    def update_user_by_email(self, user_data: dict, email: str) -> "":
        user = self.session.query(User).filter(User.email == email)
        user.update(user_data)
        self.session.commit()
        self.session.close()
        return "", 201
