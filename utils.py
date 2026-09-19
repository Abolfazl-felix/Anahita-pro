from datetime import date

from persiantools.jdatetime import JalaliDate


def validate_jalali_date(date_str: str):

    try:

        year, month, day = map(int, date_str.split("/"))

        JalaliDate(year, month, day)

        return True

    except Exception:

        return False


def days_left(date_str: str):

    year, month, day = map(int, date_str.split("/"))

    today = JalaliDate.today()

    target = JalaliDate(year, month, day)

    target = JalaliDate(
        today.year,
        target.month,
        target.day
    )

    if target < today:

        target = JalaliDate(
            today.year + 1,
            target.month,
            target.day
        )

    target_g = target.to_gregorian()

    today_g = date.today()

    return (target_g - today_g).days


def is_today(date_str):

    year, month, day = map(int, date_str.split("/"))

    today = JalaliDate.today()

    return (
        today.month == month
        and
        today.day == day
    )


def build_message(
    emoji,
    title,
    days
):

    if days == 0:

        return (
            "━━━━━━━━━━━━━━\n\n"
            f"{emoji} امروز {title} است ❤️\n\n"
            "🎉 مبارک باشه\n\n"
            "━━━━━━━━━━━━━━"
        )

    return (

        "━━━━━━━━━━━━━━\n\n"

        f"{emoji} تا {title}\n\n"

        f"❤️ فقط {days} روز باقی مانده\n\n"

        "━━━━━━━━━━━━━━"

    )