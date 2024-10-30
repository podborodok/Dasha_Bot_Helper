from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import func

Base = declarative_base()

class Chats(Base):
    __tablename__ = 'Chats'
    ChatId = Column(Integer, primary_key=True)
    Name = Column(String)
    UsersInChat = relationship('UsersInChat', secondary='ChatUser', back_populates='Chats',
                               primaryjoin='Chats.ChatId == ChatUser.ChatId',
                               secondaryjoin='ChatUser.UserId == UsersInChat.UserId')
    GoodUsers = relationship('GoodUsers', secondary='ChatUser', back_populates='Chats',
                             primaryjoin='Chats.ChatId == ChatUser.ChatId',
                             secondaryjoin='ChatUser.UserId == GoodUsers.UserId')

class Users(Base):
    __abstract__ = True
    UserId = Column(Integer, primary_key=True)
    Name = Column(String)

class ChatUser(Base):
    __tablename__ = 'ChatUser'
    ChatId = Column(Integer, ForeignKey('Chats.ChatId'), primary_key=True)
    UserId = Column(Integer, ForeignKey('UsersInChat.UserId'), primary_key=True)

class UsersInChat(Users):
    __tablename__ = 'UsersInChat'
    Chats = relationship('Chats', secondary='ChatUser', back_populates='UsersInChat',
                         primaryjoin='UsersInChat.UserId == ChatUser.UserId',
                         secondaryjoin='ChatUser.ChatId == Chats.ChatId')

class GoodUsers(Users):
    __tablename__ = 'GoodUsers'
    Chats = relationship('Chats', secondary='ChatUser', back_populates='GoodUsers',
                         primaryjoin='GoodUsers.UserId == ChatUser.UserId',
                         secondaryjoin='ChatUser.ChatId == Chats.ChatId')

engine = create_engine('sqlite:///chinook.db')
Base.metadata.create_all(engine)

chat = Chats(Name='General Chat')
user = UsersInChat(Name='John Doe')
good_user = GoodUsers(Name='Jane Doe')

chat.UsersInChat.append(user)
chat.GoodUsers.append(good_user)

Session = sessionmaker(bind=engine)
session = Session()


chats_counts_q = session.query(
    Chats.Name, func.count(ChatUser.UserId)
).select_from(Chats).join(ChatUser).group_by(Chats.Name)

chats_counts = chats_counts_q.all()
for chat, count in chats_counts:
    print(f"list = {chat}, count = {count}")
