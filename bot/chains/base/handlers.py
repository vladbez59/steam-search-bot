from aiogram.types import Message, ContentType

from bot.config import *

from bot.__main__ import bot, dp, steamfunc

import bot.chains.queue.queuefunc as queuefunc

async def init(dp):
    await bot.send_message(chat_id=ADMIN_ID, text = 'Bot started!')

@dp.message_handler(commands=['результат'])
async def search(message: Message):

    await queuefunc.sendResult(message.chat.id)

    return

@dp.message_handler(commands=['помощь'])
async def search(message: Message):
    if queuefunc.checkUser(message.chat.id) == False:
        queuefunc.addUser(message.chat.id)

    answer = 'Команды:\n'

    answer += '/статус - сколько найдено аккаунтов\n'
    answer += '/найстройки - Ваши настройки\n'
    answer += '/результат - получить файл с найденными аккаунтами, если они есть\n'

    await bot.send_message(chat_id=message.from_user.id, text=answer)

    return

@dp.message_handler(commands=['настроить'])
async def search(message: Message):

    #цена инвентаря

    command = message.text.replace('/настроить ', '')

    await bot.send_message(chat_id=message.from_user.id, text=queuefunc.changeSettings(message.chat.id, command))

    return

@dp.message_handler(commands=['статус'])
async def search(message: Message):
    if queuefunc.checkUser(message.chat.id) == False:
        queuefunc.addUser(message.chat.id)

    if queuefunc.settings[str(message.chat.id)]["stop"] == 'False':
        ans_w = 'да'
    else:
        ans_w = 'нет'

    answer = f'Бот работает: {ans_w}\n'
    answer += f'Найдено профилей: {len(queuefunc.results[str(message.chat.id)])}'

    await bot.send_message(chat_id=message.from_user.id, text=answer)

@dp.message_handler(commands=['настройки'])
async def search(message: Message):
    if queuefunc.checkUser(message.chat.id) == False:
        queuefunc.addUser(message.chat.id)

    await bot.send_message(chat_id=message.from_user.id, text=queuefunc.getSettings(message.chat.id))

@dp.message_handler(content_types = ContentType.TEXT)
async def search(message: Message):

    if queuefunc.checkUser(message.chat.id) == False:
        queuefunc.addUser(message.chat.id)

    flag = False

    lines = []
    lines = message.text.split('\n')

    for link in lines:
        if 'forcedrop.io/user/' in link:
            url = steamfunc.getSteam(link)

            if url != None:


                flag = True

                queuefunc.addLink(url, link, message.chat.id)
    if flag:
        await bot.send_message(chat_id=message.from_user.id, text='Профили добавлены')



