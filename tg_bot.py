import asyncio
from aiogram import Dispatcher
import os

from app.heandlers import router, bot


# async def loop(id_user_list, bot):
#     while True:
#         for user_id in id_user_list:
#             url = users_dict[user_id]
#             await send_massage(f'last_options_{user_id}.pkl', url, bot, user_id)
#             # await bot.send_message(chat_id=user_id, text='Проверка')
#         await asyncio.sleep(120)


async def main():
    dp = Dispatcher()
    dp.include_router(router)

    # id_user_list = await get_user_list()

    await asyncio.gather(dp.start_polling(bot))


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
