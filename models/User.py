from flask_login import UserMixin
from datetime import datetime

class User(UserMixin):
    def __init__(
        self, 
        id: int = None, 
        email: str = None, 
        password: str = None, 
        first_name: str = None, 
        last_name: str = None, 
        username: str = None, 
        active: bool = None, 
        deleted_at: datetime = None, 
        deleted_by: int = None,
        created_at: datetime = None, 
        created_by: int = None,
        updated_at: datetime = None, 
        updated_by: int = None
    ):
        self.id = id
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.active = active
        self.deleted_at = deleted_at
        self.deleted_by = deleted_by
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by