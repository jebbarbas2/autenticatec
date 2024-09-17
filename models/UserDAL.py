from models.User import User
from models.DAL import DAL
import bcrypt
from datetime import datetime

class UserDAL(DAL):
    def __init__(self):
        super().__init__()

    def create(self, user: User):
        new_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
        current_user = 0

        self._psql_execute_and_commit(
            'INSERT INTO AUTH.USER(EMAIL, PASSWORD, FIRST_NAME, LAST_NAME, USERNAME, ACTIVE, CREATED_AT, CREATED_BY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            [
                user.email,
                new_password,
                user.first_name,
                user.last_name,
                user.username,
                True,
                datetime.now(),
                current_user
            ]
        )

        row = self._psql_fetchone('SELECT * FROM AUTH.USER WHERE EMAIL = %s', [user.email])
        return row