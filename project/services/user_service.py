from project.exceptions import IncorrectPassword, ItemNotFound
from project.services.base import BaseMixinService
from project.tools import hash_password, compare_passwords


class UserService(BaseMixinService):

    def get_user_by_email(self, email):

        user = self.dao.get_user_by_email(email)

        if not user:
            raise ItemNotFound
        return user

    def create(self, user_data):

        user = self.dao.get_user_by_email(user_data.get('email'))

        if user:
            raise Exception("This Username Already Exists")

        user_data['password'] = hash_password(user_data.get('password'))
        user = self.dao.create_user(user_data)

        return user

    def update_password(self, data, email):

        user = self.get_user_by_email(email)
        old_password = data.get('password_old')
        new_password = data.get('password_new')

        if None in [old_password, new_password]:
            raise ItemNotFound

        if not compare_passwords(user.password, old_password):
            raise IncorrectPassword

        data = {
            'password': hash_password(new_password)
        }
        self.dao.update_user_by_email(data, email)

    def update_data(self, data, email):
        try:
            if self.get_user_by_email(email):
                if 'email' in data.keys():
                    self.dao.update_user_by_email(data, email)
            else:
                raise ItemNotFound

        except Exception as e:
            print(e)
