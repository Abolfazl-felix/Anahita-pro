from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup
)


def main_menu():

    keyboard = [

        [
            InlineKeyboardButton(
                "➕ افزودن مناسبت",
                callback_data="add"
            )
        ],

        [
            InlineKeyboardButton(
                "📋 لیست مناسبت‌ها",
                callback_data="list"
            )
        ],

        [
            InlineKeyboardButton(
                "📢 کانال‌ها",
                callback_data="channels"
            )
        ],

        [
            InlineKeyboardButton(
                "⚙️ تنظیمات",
                callback_data="settings"
            )
        ],

    ]

    return InlineKeyboardMarkup(keyboard)