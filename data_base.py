from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)

class ValidUser(Base):
    __tablename__ = 'valid_users'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="valid_users")

class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

class UserInChat(Base):
    __tablename__ = 'user_in_chat'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    chat_id = Column(Integer, ForeignKey('chats.id'), nullable=False)
    is_valid = Column(Boolean, default=False)

    user = relationship("User", back_populates="chats")
    chat = relationship("Chat", back_populates="users")

# Связи
User.valid_users = relationship("ValidUser", order_by=ValidUser.id, back_populates="user")
User.chats = relationship("UserInChat", order_by=UserInChat.id, back_populates="user")

Chat.users = relationship("UserInChat", order_by=UserInChat.id, back_populates="chat")

# Создание базы данных
engine = create_engine('sqlite:///chat_db.db')
Base.metadata.create_all(engine)

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# # Пример использования
# # Создание пользователя
# user1 = User(username="user1")
# session.add(user1)
# session.commit()
#
# # Создание валидного пользователя
# valid_user1 = ValidUser(user=user1)
# session.add(valid_user1)
# session.commit()
#
# # Создание чата
# chat1 = Chat(name="chat1")
# session.add(chat1)
# session.commit()
#
# # Добавление пользователя в чат
# user_in_chat1 = UserInChat(user=user1, chat=chat1, is_valid=True)
# session.add(user_in_chat1)
# session.commit()
#
# # Получение всех пользователей в чате
# chat_users = session.query(UserInChat).filter_by(chat_id=chat1.id).all()
# for user_in_chat in chat_users:
#     print(f"User: {user_in_chat.user.username}, Valid: {user_in_chat.is_valid}")