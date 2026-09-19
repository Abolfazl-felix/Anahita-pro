from apscheduler.schedulers.asyncio import AsyncIOScheduler

from telegram import Bot

from config import BOT_TOKEN
from database import get_connection
from utils import days_left, build_message


bot = Bot(BOT_TOKEN)

scheduler = AsyncIOScheduler()


async def send_daily_messages():

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("""
        SELECT
            channels.telegram_id,
            events.title,
            events.event_date,
            events.emoji
        FROM events
        JOIN channels
        ON events.channel_id = channels.id
        WHERE channels.enabled = 1
    """)

    rows = cur.fetchall()

    conn.close()

    for channel_id, title, event_date, emoji in rows:

        days = days_left(event_date)

        if days > 30:
            continue

        text = build_message(
            emoji,
            title,
            days
        )

        try:

            await bot.send_message(
                chat_id=channel_id,
                text=text
            )

        except Exception as e:

            print(e)


def start_scheduler():

    scheduler.add_job(
        send_daily_messages,
        "cron",
        hour=9,
        minute=0
    )

    scheduler.start()