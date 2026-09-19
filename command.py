from telegram import Update
from telegram.ext import ContextTypes
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from config import ADMIN_ID
from database import get_connection
from keyboards import main_menu
from utils import validate_jalali_date


user_states = {}
temp_data = {}


def is_admin(user_id):
    return user_id == ADMIN_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        return

    await update.message.reply_text(
        "🎂 پنل مدیریت مناسبت‌ها",
        reply_markup=main_menu()
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    data = query.data

    if data == "add":

        user_states[query.from_user.id] = "WAIT_TITLE"

        await query.message.reply_text(
            "نام مناسبت را وارد کنید."
        )

    elif data == "list":

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("""
            SELECT id,title,event_date
            FROM events
            ORDER BY event_date
        """)

        rows = cur.fetchall()

        conn.close()

        if not rows:

            await query.message.reply_text(
                "مناسبتی ثبت نشده است."
            )

            return

        text = ""

        for row in rows:

            text += (
                f"{row[0]}. "
                f"{row[1]} - "
                f"{row[2]}\n"
            )

        await query.message.reply_text(text)

    elif data == "channels":

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("""
            SELECT id,title
            FROM channels
        """)

        rows = cur.fetchall()

        conn.close()

        keyboard = []

        for channel in rows:

            keyboard.append([
                InlineKeyboardButton(
                    channel[1],
                    callback_data=f"channel_{channel[0]}"
                )
            ])

        await query.message.reply_text(
            "کانال مورد نظر را انتخاب کنید.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif data == "settings":

        await query.message.reply_text(
            "بخش تنظیمات در ادامه تکمیل می‌شود."
        )
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        return

    user_id = update.effective_user.id

    if user_id not in user_states:
        return

    state = user_states[user_id]

    if state == "WAIT_TITLE":

        temp_data[user_id] = {
            "title": update.message.text
        }

        user_states[user_id] = "WAIT_DATE"

        await update.message.reply_text(
            "تاریخ را به فرمت 1405/09/30 وارد کنید."
        )

        return

    if state == "WAIT_DATE":

        date = update.message.text.strip()

        if not validate_jalali_date(date):

            await update.message.reply_text(
                "❌ تاریخ وارد شده معتبر نیست."
            )

            return

        temp_data[user_id]["date"] = date

        conn = get_connection()

        cur = conn.cursor()

        cur.execute("""
            SELECT id,title
            FROM channels
            ORDER BY title
        """)

        channels = cur.fetchall()

        conn.close()

        if not channels:

            await update.message.reply_text(
                "❌ هیچ کانالی ثبت نشده است."
            )

            user_states.pop(user_id, None)
            temp_data.pop(user_id, None)

            return

        keyboard = []

        for channel in channels:

            keyboard.append([
                InlineKeyboardButton(
                    channel[1],
                    callback_data=f"save_{channel[0]}"
                )
            ])

        user_states[user_id] = "WAIT_CHANNEL"

        await update.message.reply_text(
            "کانال مقصد را انتخاب کنید.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        return


async def save_event(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if not query.data.startswith("save_"):
        return

    user_id = query.from_user.id

    if user_id not in temp_data:
        return

    channel_id = int(query.data.split("_")[1])

    title = temp_data[user_id]["title"]

    event_date = temp_data[user_id]["date"]

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO events
        (channel_id,title,event_date)
        VALUES(?,?,?)
        """,
        (
            channel_id,
            title,
            event_date
        )
    )

    conn.commit()

    conn.close()

    user_states.pop(user_id, None)
    temp_data.pop(user_id, None)

    await query.message.reply_text(
        "✅ مناسبت با موفقیت ثبت شد."
    )
async def select_channel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if not query.data.startswith("channel_"):
        return

    channel_id = int(query.data.split("_")[1])

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        SELECT title
        FROM channels
        WHERE id=?
        """,
        (channel_id,)
    )

    row = cur.fetchone()

    conn.close()

    if row is None:

        await query.message.reply_text(
            "❌ کانال پیدا نشد."
        )

        return

    temp_data[query.from_user.id] = {
        "selected_channel": channel_id
    }

    await query.message.reply_text(
        f"✅ کانال «{row[0]}» انتخاب شد."
    )


async def delete_event(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        return

    if len(context.args) != 1:

        await update.message.reply_text(
            "نمونه:\n/delete 3"
        )

        return

    try:

        event_id = int(context.args[0])

    except ValueError:

        await update.message.reply_text(
            "شناسه نامعتبر است."
        )

        return

    conn = get_connection()

    cur = conn.cursor()

    cur.execute(
        """
        DELETE FROM events
        WHERE id=?
        """,
        (event_id,)
    )

    conn.commit()

    deleted = cur.rowcount

    conn.close()

    if deleted:

        await update.message.reply_text(
            "✅ مناسبت حذف شد."
        )

    else:

        await update.message.reply_text(
            "❌ مناسبت پیدا نشد."
        )


async def test_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not is_admin(update.effective_user.id):
        return

    await update.message.reply_text(
        "🎂 این یک پیام تستی است.\n\n❤️ ربات به درستی کار می‌کند."
    )
from telegram.ext import (
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)


def register_handlers(application):

    application.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    application.add_handler(
        CommandHandler(
            "delete",
            delete_event
        )
    )

    application.add_handler(
        CommandHandler(
            "test",
            test_message
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            save_event,
            pattern=r"^save_"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            select_channel,
            pattern=r"^channel_"
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            button
        )
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            text_handler
        )
    )