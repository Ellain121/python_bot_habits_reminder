import my_token_unsecure
from aiogram import Bot, Dispatcher, F, Router
import asyncio
from datetime import datetime
import os
import logging
from tasks import DatabaseManager as DB
import my_user_id
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import time

# ========= INIT ==============#
script_dir = os.path.dirname(os.path.realpath(__file__))
filename = script_dir + str("/logs/") + \
    datetime.now().strftime("%d_%b_%Y_%A_logs.txt")

logging.basicConfig(format='---> (%(asctime)s, %(name)s, %(levelname)s): %(message)s', level=logging.INFO, handlers=[
    logging.FileHandler(filename=filename, mode="a"),
    logging.StreamHandler()
])
logging.basicConfig(level=logging.INFO)

bot = Bot(token=my_token_unsecure.Token)
dp = Dispatcher()
router = Router()

db = DB()

morning_H = 8
evening_H = 22
after_evening_H = 23
#####################################

### Utility functions ###


def get_time_H():
    return int(datetime.now().strftime("%H"))

##########################


async def start_day():
    habits_list: str = db.get_habits_str()
    habits_list = "`**Tasks for today:**\n\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\n`" + habits_list
    await bot.send_message(my_user_id.user_id, habits_list, parse_mode='MarkdownV2')


async def end_of_day_notify():
    await bot.send_message(my_user_id.user_id, "`**Please synchronize database. Bot will end the day at 23:00.**`", parse_mode="MarkdownV2")


async def end_of_day():
    habits_list: str = db.get_habits_full_str()
    habits_list = "`**Today results:**\n\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\=\n`" + habits_list
    await bot.send_message(my_user_id.user_id, habits_list, parse_mode='MarkdownV2')


async def task_starter():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(start_day, trigger='cron',
                      minute=30, hour=7, jitter=600)
    scheduler.add_job(end_of_day_notify, trigger='cron',
                      minute=0, hour=22, jitter=360)
    scheduler.add_job(end_of_day, trigger='cron',
                      minute=0, hour=23, jitter=180)
    scheduler.start()


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

loop = asyncio.get_event_loop()
sub_task = loop.create_task(task_starter())
main_task = loop.create_task(main())
loop.run_until_complete(main_task)

pending = asyncio.all_tasks(loop=loop)

for task in pending:
    task.cancel()

group = asyncio.gather(*pending, return_exceptions=True)
loop.run_until_complete(group)
loop.close()
