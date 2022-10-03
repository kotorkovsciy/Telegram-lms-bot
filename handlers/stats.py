from aiogram.dispatcher.filters import Text
from aiogram import Dispatcher, types
from create_bot import db
from keyboards import kb_client
from scripts import LMS
from asyncio import sleep
from datetime import datetime as dt


async def cmd_schedule(message: types.Message):
    if not await db.userExsist(message.from_user.id):
        await message.answer(
            f"❗ Вы не авторизованны",
            reply_markup=await kb_client(await db.userExsist(message.from_id)),
        )
    else:
        msg = await message.answer("⌛ Идёт загрузка ⌛")
        info = await db.userInfo(message.from_user.id)
        schedule = await LMS.get_schedule(info["email"], info["password"])
        await msg.edit_text(f"Ваше расписание")
        for x, i in enumerate(schedule):
            if x == 0:
                if not i[0][:-6] in dt.today().strftime("%d.%m.%Y"):
                    await msg.answer("Сегодня у вас нет пар")
                    break
                await message.answer(
                    i[0], reply_markup=await kb_client(await db.userExsist(message.from_id))
                )
                for x in i[1]:
                    await message.answer(
                        f"{x[0]}",
                        reply_markup=await kb_client(await db.userExsist(message.from_id)),
                    )
                    await sleep(0.5)


async def cmd_info(message: types.Message):
    if not await db.userExsist(message.from_user.id):
        await message.answer(
            f"❗ Вы не авторизованны",
            reply_markup=await kb_client(await db.userExsist(message.from_id)),
        )
    else:
        msg = await message.answer("⌛ Идёт загрузка ⌛")
        info = await db.userInfo(message.from_user.id)
        info = await LMS.get_soup_info(info["email"], info["password"])
        await msg.edit_text(
            f"👤 Ваша информация\nВас зовут  {info['name']}\n\n📩 Сообщений: {info['message']}\n\n🔔 Уведомлений: {info['notify']}"
        )


def register_handlers_stats(dp: Dispatcher):
    dp.register_message_handler(cmd_schedule, Text(equals="Расписание на сегодня"))
    dp.register_message_handler(cmd_info, Text(equals="Информация"))
