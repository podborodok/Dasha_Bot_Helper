from Dasha_Bot_Helper import data_base
from Dasha_Bot_Helper.data_base import User, Chat, Base, chat_user
import asyncio
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import os
from pyrogram import Client
from pyrogram import filters
from functions import show_commands, call_dasha_func, add_chat_to_db_func, add_users_to_valid_list, delete_users_from_valid_list, get_chat_id_func, get_valid_func
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

API_ID = 'API_ID'
API_HASH = 'API_HASH'
BOT_TOKEN = 'BOT_TOKEN'

def build():
    global session
    if os.path.exists('chat_db.db'):
        os.remove('chat_db.db')
    engine = create_engine('sqlite:///chat_db.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

build()
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.group & filters.command('commands'))
def commands(client, message):
    show_commands(client, message, session)

@app.on_message(filters.group & filters.command('get_chat_id'))
def get_chat_id(client, message):
    get_chat_id_func(client, message, session)

@app.on_message(filters.group & filters.command('get_valid'))
def get_valid(client, message):
    get_valid_func(client, message, session)
@app.on_message(filters.group & filters.command('call_dasha'))
def call_dasha(client, message):
    call_dasha_func(client, message, session, app)
@app.on_message(filters.group & filters.command("add_chat"))
def add_chat_to_db(client, message):
    add_chat_to_db_func(client, message, session)

@app.on_message(filters.group & filters.command('valid'))
def valid(client, message):
    add_users_to_valid_list(client, message, session, app)
@app.on_message(filters.group & filters.command('not_valid'))
def not_valid(client, message):
    delete_users_from_valid_list(client, message, session, app)

@app.on_message(filters.private & filters.command('call_dasha'))
def call_dasha(client, message):
    call_dasha_func(client, message, session, app, True)

@app.on_message(filters.command('valid') & filters.private)
def valid(client, message):
    add_users_to_valid_list(client, message, session, app, True)
@app.on_message(filters.command('not_valid') & filters.private)
def not_valid(client, message):
    delete_users_from_valid_list(client, message, session, app, True)

app.run()
