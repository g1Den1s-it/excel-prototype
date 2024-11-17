from sqlalchemy import Column, Integer, String

from src.database import Base
from src.auth.utils import PasswordHax


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(48), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    _password = Column("password",String, nullable=False)
    first_name = Column(String(28), nullable=True)
    surname = Column(String(28), nullable=True)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = PasswordHax.create_password_hash(value)

    def __repr__(self):
        return f"id: {self.id}, username: {self.username}"
