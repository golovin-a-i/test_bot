import pandas as pd
import logging
import random
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
from telegram.ext import MessageHandler, Filters, InlineQueryHandler

TOKEN = '5540462908:AAGmh0-xWLtPdvYwFOjyy1CyDfMk_s4_LUU'
updater = Updater(token=TOKEN)
dispatcher_bot = updater.dispatcher

# /start
# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text='Hi, it\'s start')

# def registration(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text='You\'r name?')
#     context.bot.send_message(chat_id=update.effective_chat.id, text='You\'r name?')
#     context.bot.send_message(chat_id=update.effective_chat.id, text='You\'r name?')



# def echo(update, context):
#     text = f'ECHO {update.message.text}'
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text)

# def unknown(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text='Sorry, can\'t understand you')

# start_handler = CommandHandler('start', start)
# dispatcher_bot.add_handler(start_handler)
# registration_handler = CommandHandler('reg', registration)
# dispatcher_bot.add_handler(registration_handler)
# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
# dispatcher_bot.add_handler(echo_handler)
# unlnown_handler = MessageHandler(Filters.command, unknown)
# dispatcher_bot.add_handler(unlnown_handler)



# def start(update, _):
#     keyboard = [
#         [
#             InlineKeyboardButton("Option 1", callback_data='1'),
#             InlineKeyboardButton("Option 2", callback_data='2'),
#         ],
#         [InlineKeyboardButton("Option 3", callback_data='Adventure')],
#     ]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text('Пожалуйста, выберите:', reply_markup=reply_markup)


# def button(update, _):
#     query = update.callback_query
#     variant = query.data

#     # `CallbackQueries` требует ответа, даже если 
#     # уведомление для пользователя не требуется, в противном
#     #  случае у некоторых клиентов могут возникнуть проблемы. 
#     # смотри https://core.telegram.org/bots/api#callbackquery.
#     query.answer()
#     # редактируем сообщение, тем самым кнопки 
#     # в чате заменятся на этот ответ.
#     query.edit_message_text(text=f"Выбранный вариант: {variant}")

# def help_command(update, _):
#     update.message.reply_text("Используйте `/start` для тестирования.")

# updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CallbackQueryHandler(button))
# updater.dispatcher.add_handler(CommandHandler('help', help_command))



logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)
# Этапы/состояния разговора
FIRST, SECOND = range(2)
# Данные обратного вызова
ONE, TWO, THREE, FOUR = range(4)


def start(update, _):
    """Вызывается по команде `/start`."""
    # Получаем пользователя, который запустил команду `/start`
    user = update.message.from_user
    logger.info("Пользователь %s начал разговор", user.first_name)
    # Создаем `InlineKeyboard`, где каждая кнопка имеет 
    # отображаемый текст и строку `callback_data`
    # Клавиатура - это список строк кнопок, где каждая строка, 
    # в свою очередь, является списком `[[...]]`
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем сообщение с текстом и добавленной клавиатурой `reply_markup`
    update.message.reply_text(
        text="Запустите обработчик, выберите маршрут", reply_markup=reply_markup
    )
    # Сообщаем `ConversationHandler`, что сейчас состояние `FIRST`
    return FIRST


def start_over(update, _):
    """Тот же текст и клавиатура, что и при `/start`, но не как новое сообщение"""
    # Получаем `CallbackQuery` из обновления `update`
    query = update.callback_query
    # На запросы обратного вызова необходимо ответить, 
    # даже если уведомление для пользователя не требуется.
    # В противном случае у некоторых клиентов могут возникнуть проблемы.
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("2", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
   # Отредактируем сообщение, вызвавшее обратный вызов.
   # Это создает ощущение интерактивного меню.
    query.edit_message_text(
        text="Выберите маршрут", reply_markup=reply_markup
    )
    # Сообщаем `ConversationHandler`, что сейчас находимся в состоянии `FIRST`
    return FIRST


def one(update, _):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("3", callback_data=str(THREE)),
            InlineKeyboardButton("4", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Вызов `CallbackQueryHandler`, выберите маршрут", reply_markup=reply_markup
    )
    return FIRST


def two(update, _):
    """Показ нового выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("1", callback_data=str(ONE)),
            InlineKeyboardButton("3", callback_data=str(THREE)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Второй CallbackQueryHandler", reply_markup=reply_markup
    )
    return FIRST


def three(update, _):
    """Показ выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Да, сделаем это снова!", callback_data=str(ONE)),
            InlineKeyboardButton("Нет, с меня хватит ...", callback_data=str(TWO)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Третий CallbackQueryHandler. Начать сначала?", reply_markup=reply_markup
    )
    # Переход в состояние разговора `SECOND`
    return SECOND


def four(update, _):
    """Показ выбора кнопок"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("2", callback_data=str(TWO)),
            InlineKeyboardButton("4", callback_data=str(FOUR)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Четвертый CallbackQueryHandler, выберите маршрут", reply_markup=reply_markup
    )
    return FIRST


def end(update, _):
    """Возвращает `ConversationHandler.END`, который говорит 
    `ConversationHandler` что разговор окончен"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


dispatcher = updater.dispatcher

# Настройка обработчика разговоров с состояниями `FIRST` и `SECOND`
# Используем параметр `pattern` для передачи `CallbackQueries` с
# определенным шаблоном данных соответствующим обработчикам
# ^ - означает "начало строки"
# $ - означает "конец строки"
# Таким образом, паттерн `^ABC$` будет ловить только 'ABC'
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={ # словарь состояний разговора, возвращаемых callback функциями
        FIRST: [
            CallbackQueryHandler(one, pattern='^' + str(ONE) + '$'),
            CallbackQueryHandler(two, pattern='^' + str(TWO) + '$'),
            CallbackQueryHandler(three, pattern='^' + str(THREE) + '$'),
            CallbackQueryHandler(four, pattern='^' + str(FOUR) + '$'),
        ],
        SECOND: [
            CallbackQueryHandler(start_over, pattern='^' + str(ONE) + '$'),
            CallbackQueryHandler(end, pattern='^' + str(TWO) + '$'),
        ],
    },
    fallbacks=[CommandHandler('start', start)],
)

# Добавляем `ConversationHandler` в диспетчер, который
# будет использоваться для обработки обновлений
dispatcher.add_handler(conv_handler)



# Запуск бота
updater.start_polling()

