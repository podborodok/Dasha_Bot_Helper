from data_base import User, Chat, Base, chat_user

def show_commands(client, message, session):
    message.reply_text(
        "**Commands:**\n\n"
        "🔹 Firstly Run /add_chat to add this chat to my database.\n"
        "🔹 Run /valid {usernames} to add these usernames to the valid list.\n"
        "🔹 Run /not_valid {usernames} to delete these usernames from the valid list.\n"
        "🔹 Run /call_dasha to kick chat members who are not from the valid list and have no administrator status."
    )
def call_dasha_func(client, message, session, app):
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat_member_status = app.get_chat_member(chat_id, user_id).status
    current_chat = session.query(Chat).filter_by(id=chat_id).first()
    if not current_chat:
        message.reply_text("Please run /add_chat first.")
        return
    valid_users = current_chat.valid_users
    if len(valid_users) == 0:
        message.reply_text(f"Valid list is empty.")
    else:
        message.reply_text(f"Valid users are: {', '.join(valid_users)}")
    if (chat_member_status == app.get_chat_member(chat_id, user_id).status.OWNER or chat_member_status == app.get_chat_member(chat_id, user_id).status.ADMINISTRATOR):
        count_kick = 0
        for member in app.get_chat_members(chat_id):
            member_username = member.user.username
            member_status = app.get_chat_member(chat_id, member.user.id).status
            if member_username not in valid_users and member.user.id != app.get_me().id and (member_status != app.get_chat_member(chat_id, member.user.id).status.OWNER and member_status != app.get_chat_member(chat_id, member.user.id).status.ADMINISTRATOR):
                app.ban_chat_member(chat_id, member.user.id)
                count_kick += 1
        if (count_kick > 0):
            message.reply_text(f"Haha -{count_kick}😜")
        else:
            message.reply_text("All members stayed in chat.")
    else:
        message.reply_text(f"You have no rights here, @{app.get_chat_member(chat_id, user_id).user.username} 😘🥇")


def add_chat_to_db_func(client, message, session):
    chat_id = message.chat.id
    current_chat = session.query(Chat).filter_by(id=chat_id).first()
    if not current_chat:
        current_chat = Chat(id=chat_id, title=message.chat.title)
        session.add(current_chat)
        session.commit()

    current_chat_users = client.get_chat_members(chat_id)
    for current_chat_user in current_chat_users:
        user = current_chat_user.user
        current_user = session.query(User).filter_by(id=user.id).first()
        if not current_user:
            current_user = User(id=user.id, name=user.username)
            session.add(current_user)
            session.commit()
        current_chat.add_user(current_user, valid=False)

    session.commit()
    message.reply_text("Done. Ready to kick.")


def add_users_to_valid_list(client, message, session, app):
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat_member_status = app.get_chat_member(chat_id, user_id).status

    command_parts = message.text.split()
    valid_users = list(set(command_parts[1:]))
    current_chat = session.query(Chat).filter_by(id=chat_id).first()
    if not current_chat:
        message.reply_text("Please run /add_chat first.")
        return
    if not (chat_member_status == app.get_chat_member(chat_id,user_id).status.OWNER or chat_member_status == app.get_chat_member(chat_id, user_id).status.ADMINISTRATOR):
        message.reply_text(f"You have no rights here, @{app.get_chat_member(chat_id, user_id).user.username} 😘🥇")
        return
    if len(valid_users) == 0:
        message.reply_text("No one is added, the list sent is empty.")
        return
    for valid_user in valid_users:
        current_chat.add_valid_user(valid_user)
    current_chat.commit_users(session)
    session.commit()
    if len(valid_users) == 1:
        message.reply_text(f"{', '.join(valid_users)} is added to valid list.")
    else:
        message.reply_text(f"{', '.join(valid_users)} are added to valid list.")

def delete_users_from_valid_list(client, message, session, app):
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat_member_status = app.get_chat_member(chat_id, user_id).status
    command_parts = message.text.split()
    not_valid_users = list(set(command_parts[1:]))
    current_chat = session.query(Chat).filter_by(id=chat_id).first()
    if not current_chat:
        message.reply_text("Please run /add_chat first")
        return
    if not (chat_member_status == app.get_chat_member(chat_id,user_id).status.OWNER or chat_member_status == app.get_chat_member(chat_id, user_id).status.ADMINISTRATOR):
        message.reply_text(f"You have no rights here, @{app.get_chat_member(chat_id, user_id).user.username} 😘🥇")
        return
    for not_valid_user in not_valid_users:
        current_chat.delete_from_valid_users(not_valid_user)
    current_chat.commit_users(session)
    session.commit()
    if len(not_valid_users) == 1:
        message.reply_text(f"{', '.join(not_valid_users)} is deleted from valid list.")
    else:
        message.reply_text(f"{', '.join(not_valid_users)} are deleted from valid list.")


