from environs import Env
from telegram import (ReplyKeyboardMarkup,InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler,CallbackQueryHandler)
import redis
from main import get_token,get_all_product,get_product,add_product_cart
import sys


_database = None



def start(bot, update):
    serialize_products = get_all_product()
    keyboard = []
    for i in serialize_products['data']:
        keyboard.append(
            [InlineKeyboardButton(i['name'], callback_data=i['id'])]
        )
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    return "HANDLE_MENU"


def handle_menu(bot,update):
    query = update.callback_query
    print(query.data)
    keyboard = [[InlineKeyboardButton("1 кг", callback_data=f'{query.data}*1'),
                 InlineKeyboardButton("5 кг", callback_data=f'{query.data}*5'),
                 InlineKeyboardButton("10 кг", callback_data=f'{query.data}*10')],
                [InlineKeyboardButton("Назад к рыбам", callback_data='back')]]

    #keyboard = [[InlineKeyboardButton("Назад к рыбам", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    serializer_product = get_product(query.data)
    id_file_product = serializer_product['data']['relationships']['files']['data'][0]['id']
    bot.send_photo(chat_id=query.message.chat_id, photo=open(f'fish/{id_file_product}.jpg','rb'),
    caption=f"{serializer_product['data']['name']}\n"
            f"{serializer_product['data']['description']}\n"
            f"{serializer_product['data']['price'][0]['amount']/10}$ - за хвост",
                   reply_markup=reply_markup)
    bot.delete_message(chat_id=query.message.chat_id,
                       message_id=update.callback_query.message.message_id,)

    return 'HANDLE_DESCRIPTION'


def handle_description(bot,update):
    query = update.callback_query
    query_data = query.data
    if query.data == 'back':
        serialize_products = get_all_product()
        keyboard = []
        for i in serialize_products['data']:
            keyboard.append(
                [InlineKeyboardButton(i['name'], callback_data=i['id'])]
            )
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(text="Selected option:",
                              chat_id=query.message.chat_id,
                              message_id=query.message.message_id,
                         reply_markup=reply_markup)
        return "HANDLE_MENU"
    else:
        product,quantity = query_data.split('*')
        add_product_cart(product,int(quantity))
       
    # if query.data == '1':





def echo(bot, update):
    users_reply = update.message.text
    update.message.reply_text(users_reply)
    return "ECHO"


def handle_users_reply(bot,update):
    db = get_database_connection()
    if update.message:
        user_reply = update.message.text
        chat_id = update.message.chat_id
    elif update.callback_query:
        #print(update.callback_query.data)
        user_reply = update.callback_query.data
        chat_id = update.callback_query.message.chat_id
    else:
        return
    if user_reply == '/start':
        user_state = 'START'
    else:
        user_state = db.get(chat_id).decode("utf-8")
    states_functions = {
        'START': start,
        'ECHO': echo,
        'HANDLE_MENU':handle_menu,
        'HANDLE_DESCRIPTION':handle_description,
    }
    state_handler = states_functions[user_state]
    try:
        next_state = state_handler(bot, update)
        db.set(chat_id, next_state)
    except Exception as err:
        print(err)


def get_database_connection():
    global _database
    if _database is None:
        database_password = env('REDIS_PASSWORD')
        database_host = env('REDIS_HOST')
        database_port = env('REDIS_PORT')
        _database = redis.StrictRedis(host=database_host,
                                      port=database_port,
                                      password=database_password,
                                      charset="utf-8",
                                        )
    return _database


if __name__ == '__main__':
    env = Env()
    env.read_env()
    token = env("TG_TOKEN")
    client_id = env('CLIENT_ID')
    client_secret = env('CLIENT_SECRET')
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CallbackQueryHandler(handle_users_reply))
    dispatcher.add_handler(MessageHandler(Filters.text, handle_users_reply))
    dispatcher.add_handler(CommandHandler('start', handle_users_reply))

    updater.start_polling()

