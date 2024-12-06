import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_base import User, Chat, Base, chat_user
from functions import show_commands, call_dasha_func, add_chat_to_db_func, add_users_to_valid_list, delete_users_from_valid_list
from unittest.mock import MagicMock, patch


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        self.app = MagicMock()
        self.client = MagicMock()
        self.message = MagicMock()
        self.message.chat.id = 1
        self.message.chat.title = "Test Chat"
        self.client.id = 12345
        self.client.username = "Cat"



    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_add_user_to_chat(self):
        user = User(name="Alica", id=123)
        chat = Chat(title="Test Chat", id=1)
        chat.add_user(user)

        self.assertEqual(len(chat.users), 1)
        self.assertEqual(chat.users[0].name, "Alica")
        Base.metadata.drop_all(self.engine)

    def test_add_valid_user(self):
        user = User(name="Alica", id=123)
        chat = Chat(title="Test Chat", id=1)
        chat.add_user(user, valid=True)
        self.assertEqual(chat.valid_users, ["Alica"])
        Base.metadata.drop_all(self.engine)

    def test_delete_from_valid_users(self):
        user = User(name="Alica", id=123)
        chat = Chat(title="Test Chat", id=1)

        chat.add_user(user, valid=True)
        chat.delete_from_valid_users("Alica")
        self.assertEqual(chat.valid_users, [])
        Base.metadata.drop_all(self.engine)

    def test_commit_users(self):
        user = User(name="Alica", id=123)
        chat = Chat(title="Test Chat", id=1)

        chat.add_user(user, valid=True)

        chat.commit_users(self.session)
        result = self.session.query(chat_user).filter_by(chat_id=chat.id, user_id=user.id).first()
        self.assertIsNotNone(result)
        self.assertTrue(result.valid)
        self.assertTrue(len(result) == 3)

    def test_show_commands(self):
        show_commands(self.client, self.message, self.session)

        expected_message = (
            "**Commands:**\n\n"
            "🔹 Firstly Run /add_chat to add this chat to my database.\n"
            "🔹 Run /valid {usernames} to add these usernames to the valid list.\n"
            "🔹 Run /not_valid {usernames} to delete these usernames from the valid list.\n"
            "🔹 Run /call_dasha to kick chat members who are not from the valid list and have no administrator status."
        )
        self.message.reply_text.assert_called_once_with(expected_message)
    def test_add_chat(self):
        user1 = MagicMock()
        user1.id = 11
        user1.username = "Alica"
        user2 = MagicMock()
        user2.id = 12
        user2.username = "Bob"

        self.client.get_chat_members.return_value = [MagicMock(user=user1), MagicMock(user=user2)]
        add_chat_to_db_func(self.client, self.message, self.session)
        chats = self.session.query(Chat).filter_by(id=self.message.chat.id).all()
        self.assertEqual(len(chats), 1)
        chat = chats[0]
        self.assertEqual(chat.title, self.message.chat.title)

        users = self.session.query(User).all()
        print(users)
        self.assertEqual(len(users), 2)
        self.assertEqual([users[0].id, users[0].name], [user1.id, user1.username])
        self.assertEqual([users[1].id, users[1].name], [user2.id, user2.username])
        self.message.reply_text.assert_called_once_with("Done. Ready to kick.")

    def test_valid_no_chat(self):
        self.message.text = "/add_users Alica Bob"
        add_users_to_valid_list(self.client, self.message, self.session, self.app)
        self.message.reply_text.assert_called_once_with("Please run /add_chat first.")
    def test_valid_empty_list(self):
        user1 = MagicMock()
        user1.id = 11
        user1.username = "Alica"
        user2 = MagicMock()
        user2.id = 12
        user2.username = "Bob"
        self.client.get_chat_members.return_value = [MagicMock(user=user1), MagicMock(user=user2)]
        add_chat_to_db_func(self.client, self.message, self.session)
        self.app.get_chat_member(self.message.chat.id, self.client.id).status.OWNER = self.app.get_chat_member(self.message.chat.id, self.client.id).status
        self.message.text = "/add_users"
        add_users_to_valid_list(self.client, self.message, self.session, self.app)
        self.message.reply_text.assert_any_call("No one is added, the list sent is empty.")
    def test_valid_one_user(self):
        user1 = MagicMock()
        user1.id = 11
        user1.username = "Alica"
        user2 = MagicMock()
        user2.id = 12
        user2.username = "Bob"

        self.client.get_chat_members.return_value = [MagicMock(user=user1), MagicMock(user=user2)]
        add_chat_to_db_func(self.client, self.message, self.session)
        self.app.get_chat_member(self.message.chat.id, self.client.id).status.OWNER = self.app.get_chat_member(
            self.message.chat.id, self.client.id).status
        self.message.text = "/add_users Alica"
        add_users_to_valid_list(self.client, self.message, self.session, self.app)
        self.message.reply_text.assert_any_call("Alica is added to valid list.")
    def test_valid_simple(self):
        user1 = MagicMock()
        user1.id = 11
        user1.username = "Alica"
        user2 = MagicMock()
        user2.id = 12
        user2.username = "Bob"

        self.client.get_chat_members.return_value = [MagicMock(user=user1), MagicMock(user=user2)]
        add_chat_to_db_func(self.client, self.message, self.session)
        self.app.get_chat_member(self.message.chat.id, self.client.id).status.OWNER = self.app.get_chat_member(
            self.message.chat.id, self.client.id).status
        self.message.text = "/add_users Alica Bob"
        add_users_to_valid_list(self.client, self.message, self.session, self.app)
        assert self.message.reply_text.any_call("Alica, Bob are added to valid list.") or self.message.reply_text.any_call("Bob, Alica are added to valid list.")


    def test_valid_not_admin(self):
        user1 = MagicMock()
        user1.id = 11
        user1.username = "Alica"
        user2 = MagicMock()
        user2.id = 12
        user2.username = "Bob"

        self.client.get_chat_members.return_value = [MagicMock(user=user1), MagicMock(user=user2)]
        add_chat_to_db_func(self.client, self.message, self.session)
        self.message.text = "/add_users Alica"
        add_users_to_valid_list(self.client, self.message, self.session, self.app)
        self.message.reply_text.assert_any_call(f"You have no rights here, @{self.app.get_chat_member(self.message.chat.id, self.client.id).user.username} 😘🥇")


