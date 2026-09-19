from datetime import date
from persiantools.jdatetime import JalaliDate
from telegram import Bot

from config import BOT_TOKEN, CHANNEL_ID
from storage import list_events


bot = Bot(BOT_TOKEN)


def days_left(date_str):

    year, month, day = map(int, date_str.split("/"))

    birthday = JalaliDate(year, month, day).to_gregorian()

    return (birthday - date.today()).days


async def send_daily_messages():

    events = list_events()

    if not events:
        return

    for event in events:

        days = days_left(event["date"])

        if days > 0:

            text = (
                f"🎂 تا تولد {event['name']} "
                f"{days} روز مونده ❤️"
            )

        elif days == 0:

            text = (
                f"🎉 امروز تولد "
                f"{event['name']} هست ❤️"
            )

        else:

            continue

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=text
        )