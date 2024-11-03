from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from sqlalchemy import func

Base = declarative_base()

class Chat(Base):
    __tablename__ = 'Chat'
    ChatId = Column(Integer, primary_key=True)
    Name = Column(String)
    UserInChat = relationship('UserInChat', secondary='ChatUserConnection', back_populates='Chat',
                               primaryjoin='Chat.ChatId == ChatUserConnection.ChatId',
                               secondaryjoin='ChatUserConnection.UserId == UserInChat.UserId')
    GoodUser = relationship('GoodUser', secondary='ChatUserConnection', back_populates='Chat',
                             primaryjoin='Chat.ChatId == ChatUserConnection.ChatId',
                             secondaryjoin='ChatUserConnection.UserId == GoodUser.UserId')

class User(Base):
    __tablename__ = 'Chat'
    UserId = Column(Integer, primary_key=True)
    Name = Column(String)

class ChatUserConnection(Base):
    __tablename__ = 'ChatUserConnection'
    ChatId = Column(Integer, ForeignKey('Chat.ChatId'), primary_key=True)
    UserId = Column(Integer, ForeignKey('UserInChat.UserId'), primary_key=True)

class UserInChat(User):
    __tablename__ = 'UserInChat'
    Chats = relationship('Chat', secondary='ChatUserConnection', back_populates='UserInChat',
                         primaryjoin='UserInChat.UserId == ChatUserConnection.UserId',
                         secondaryjoin='ChatUserConnection.ChatId == Chat.ChatId')

class GoodUser(User):
    __tablename__ = 'GoodUser'
    Chats = relationship('Chat', secondary='ChatUserConnection', back_populates='GoodUser',
                         primaryjoin='GoodUser.UserId == ChatUserConnection.UserId',
                         secondaryjoin='ChatUserConnection.ChatId == Chat.ChatId')

engine = create_engine('sqlite:///chinook.db')
Base.metadata.create_all(engine)

# chat = Chat(Name='General Chat')
# user = UserInChat(Name='John Doe')
# good_user = GoodUser(Name='Jane Doe')

# chat.UsersInChat.append(user)
# chat.GoodUsers.append(good_user)

# Session = sessionmaker(bind=engine)
# session = Session()


# chats_counts_q = session.query(
#     Chat.Name, func.count(ChatUserConnection.UserId)
# ).select_from(Chat).join(ChatUserConnection).group_by(Chat.Name)

# chats_counts = chats_counts_q.all()
# for chat, count in chats_counts:
#     print(f"list = {chat}, count = {count}")
