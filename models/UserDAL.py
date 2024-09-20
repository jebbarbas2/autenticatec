from models.User import User
from models.DAL import psql_execute_and_commit, psql_fetchone
import bcrypt
from datetime import datetime

class UserDAL:
    @classmethod
    def create(cls, email: str, password: str, first_name: str, last_name: str, username: str):
        new_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        current_user = 0

        psql_execute_and_commit(
            'INSERT INTO AUTH.USER(EMAIL, PASSWORD, FIRST_NAME, LAST_NAME, USERNAME, ACTIVE, CREATED_AT, CREATED_BY) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
            [
                email,
                new_password,
                first_name,
                last_name,
                username,
                True,
                datetime.now(),
                current_user
            ]
        )
        
        return cls.get_using_email_or_username(email)
    
    def __convert_row_to_user(row: tuple) -> User | None:
        if row is None: return None

        id, email, password, first_name, last_name, username, active, deleted_at, deleted_by, created_at, created_by, updated_at, updated_by = row
        user = User(id, email, password, first_name, last_name, username, active, deleted_at, deleted_by, created_at, created_by, updated_at, updated_by)
        
        return user

    @classmethod 
    def login_using_email_or_username(cls, email_or_username: str, password: str) -> User | None:
        user = cls.get_using_email_or_username(email_or_username)

        if user is None: return None
        if not bcrypt.checkpw(password.encode(), user.password.encode()): return None

        return user

    @classmethod
    def get_using_id(cls, id: int) -> User | None:
        row = psql_fetchone('SELECT ID, EMAIL, PASSWORD, FIRST_NAME, LAST_NAME, USERNAME, ACTIVE, DELETED_AT, DELETED_BY, CREATED_AT, CREATED_BY, UPDATED_AT, UPDATED_BY FROM AUTH.USER WHERE ID = %s', [id])
        return cls.__convert_row_to_user(row)
        

    @classmethod
    def get_using_email_or_username(cls, email_or_username: str) -> User | None:
        row = psql_fetchone('SELECT ID, EMAIL, PASSWORD, FIRST_NAME, LAST_NAME, USERNAME, ACTIVE, DELETED_AT, DELETED_BY, CREATED_AT, CREATED_BY, UPDATED_AT, UPDATED_BY FROM AUTH.USER WHERE EMAIL = %s OR USERNAME = %s', [email_or_username, email_or_username])
        return cls.__convert_row_to_user(row)
