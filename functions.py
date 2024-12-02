# from data_base import Chats, Users, ChatUser, UsersInChat, GoodUsers
import asyncio

import os

from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

API_ID = 'API_ID'
API_HASH = 'API_HASH'
BOT_TOKEN = 'BOT_TOKEN'

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command('call_dasha'))
def call_dasha(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    chat_member_status = app.get_chat_member(chat_id, user_id).status
    if (chat_member_status == app.get_chat_member(chat_id, user_id).status.OWNER or chat_member_status == app.get_chat_member(chat_id, user_id).status.ADMINISTRATOR):
        count_kick = 0
        for member in app.get_chat_members(chat_id):
            user_username = member.user.username
            if user_username not in valid_users and member.user.id != app.get_me().id:
                app.ban_chat_member(chat_id, member.user.id)
                count_kick += 1
        if (count_kick > 0):
            message.reply_text(f"Haha -{count_kick}😜")
    else:
        message.reply_text(f"You have no rights here, @{app.get_chat_member(chat_id, user_id).user.username} 😘🥇")

@app.on_message(filters.command("creat_list"))
def creat_list(client, message):
    global valid_users, chat_link
    command_parts = message.text.split()
    users_list = command_parts[1:-1]
    message.reply_text(users_list)
    chat_link = command_parts[-1]
    valid_users = [username for username in users_list]

app.run()

# class Dasha1984():
#     def __init__(self):
#         self.valid_list: list[GoodUsers] = []
#         self.real_list: list[UsersInChat] = []
#     def creat_list(self):
#         #создать список валидных пользователей
#         pass
#     def change_all_list(self):
#         #полностью поменять старый список валидных пользователей на новый
#         pass
#     def add_person_to_list(self):
#         #добавить в валидный список пользователя
#         pass
#     def del_person_from_list(self):
#         #удалить из валидного списка пользователя
#         pass
#     def del_person_from_chat(self):
#         #удалить пользователя из группы
#         pass
#     def check_person(self):
#         #проверить пользователя на нахождение в списке
#         pass
#     def check_group(self):
#         #проверяет каждого пользователя из валидного списка на нахождение в текущем чате
#         pass
#     def order_in_group(self):
#         #удаляет каждого участика не из валидного списка из группы
#         pass




