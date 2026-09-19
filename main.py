from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from config import BOT_TOKEN, ADMIN_ID
from storage import (
    add_event,
    list_events,
    delete_event,
    edit_event,
)


def admin_only(user_id):
    return user_id == ADMIN_ID


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not admin_only(update.effective_user.id):
        return

    await update.message.reply_text(
        "ربات روزشمار آماده است.\n\n"
        "/add نام 1405/09/30\n"
        "/list\n"
        "/delete شماره\n"
        "/edit شماره نام 1405/09/30"
    )


async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not admin_only(update.effective_user.id):
        return

    if len(context.args) != 2:
        await update.message.reply_text(
            "فرمت:\n/add نام 1405/09/30"
        )
        return

    name = context.args[0]
    date = context.args[1]

    add_event(name, date)

    await update.message.reply_text(
        f"✅ {name} ثبت شد."
    )


async def list_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not admin_only(update.effective_user.id):
        return

    events = list_events()

    if not events:
        await update.message.reply_text("لیست خالی است.")
        return

    text = ""

    for i, event in enumerate(events, start=1):

        text += (
            f"{i}. "
            f"{event['name']} - "
            f"{event['date']}\n"
        )

    await update.message.reply_text(text)


async def delete(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not admin_only(update.effective_user.id):
        return

    if len(context.args) != 1:
        return

    removed = delete_event(int(context.args[0]) - 1)

    if removed:

        await update.message.reply_text(
            f"🗑 {removed['name']} حذف شد."
        )


async def edit(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not admin_only(update.effective_user.id):
        return

    if len(context.args) != 3:
        return

    index = int(context.args[0]) - 1

    if edit_event(
        index,
        context.args[1],
        context.args[2],
    ):

        await update.message.reply_text("✅ ویرایش شد.")


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("add", add))
app.add_handler(CommandHandler("list", list_cmd))
app.add_handler(CommandHandler("delete", delete))
app.add_handler(CommandHandler("edit", edit))

app.run_polling()