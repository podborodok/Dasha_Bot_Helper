from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Table, Text
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import os

Base = declarative_base()

chat_user = Table(
    'chat_user',
    Base.metadata,
    Column('chat_id', ForeignKey('chat.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('valid', Boolean, default=False),
    extend_existing=True,
)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

class Chat(Base):
    __tablename__ = 'chat'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    users = relationship('User', secondary=chat_user, backref='chats')
    valid_users_str = Column(Text)  # Используем Text для хранения строки

    @property
    def valid_users(self):
        if self.valid_users_str:
            return self.valid_users_str.split(',')
        return []

    @valid_users.setter
    def valid_users(self, value):
        self.valid_users_str = ','.join(value)
    def add_user(self, user, valid=False):
        self.users.append(user)
        if valid:
            self.valid_users = self.valid_users + [user.name]
    def add_valid_user(self, username):
        self.valid_users = self.valid_users + [username]

    def delete_from_valid_users(self, username):
        if username in self.valid_users:
            self.valid_users = [name for name in self.valid_users if name != username]

    def commit_users(self, session):
        for user in self.users:
            is_valid = user.name in self.valid_users
            existing_entry = session.query(chat_user).filter_by(chat_id=self.id, user_id=user.id).first()
            if not existing_entry:
                session.execute(chat_user.insert().values(chat_id=self.id, user_id=user.id, valid=is_valid))
            else:
                session.execute(chat_user.update().where(chat_user.c.chat_id == self.id).where(
                    chat_user.c.user_id == user.id).values(valid=is_valid))
        session.commit()
