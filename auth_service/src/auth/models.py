from sqlalchemy import Column, Integer, String

from auth_service.src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(48), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String(28), nullable=True)
    surname = Column(String(28), nullable=True)

    def __repr__(self):
        return f"id: {self.id}, username: {self.username}"
