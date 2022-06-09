from .base import BaseMixinDAO
from .models import User


class UserDAO(BaseMixinDAO):

    def get_user_by_email(self, email):
        try:
            user = self.session.query(User).filter(User.email == email).one()

            return user

        except Exception as e:

            return print(e)

    def create_user(self, user_data):
        user = User(**user_data)
        self.session.add(user)
        self.session.commit()
        self.session.close()
        return user

    def update_user_by_email(self, user_data, email):
        find_user = self.get_user_by_email(email)
        updated_user = find_user.update(user_data)
        self.session.commit()
        self.session.close()
        return "", 200
