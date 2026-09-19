import json
import os

from config import DATA_FILE


def _default_data():
    return {
        "selected_channels": {},
        "events": []
    }


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(_default_data())

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        data = _default_data()
        save_data(data)
        return data


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(
            data,
            f,
            ensure_ascii=False,
            indent=4
        )


def set_selected_channel(user_id, channel_id, channel_name):

    data = load_data()

    data["selected_channels"][str(user_id)] = {
        "channel_id": channel_id,
        "channel_name": channel_name
    }

    save_data(data)


def get_selected_channel(user_id):

    data = load_data()

    return data["selected_channels"].get(str(user_id))


def add_event(
    channel_id,
    channel_name,
    name,
    date
):

    data = load_data()

    data["events"].append({
        "channel_id": channel_id,
        "channel_name": channel_name,
        "name": name,
        "date": date
    })

    save_data(data)


def get_events(channel_id=None):

    data = load_data()

    if channel_id is None:
        return data["events"]

    return [
        e
        for e in data["events"]
        if e["channel_id"] == channel_id
    ]


def delete_event(channel_id, index):

    events = get_events(channel_id)

    if index < 0 or index >= len(events):
        return None

    target = events[index]

    data = load_data()

    data["events"].remove(target)

    save_data(data)

    return target


def edit_event(
    channel_id,
    index,
    new_name,
    new_date
):

    events = get_events(channel_id)

    if index < 0 or index >= len(events):
        return False

    target = events[index]

    data = load_data()

    for item in data["events"]:

        if item == target:

            item["name"] = new_name
            item["date"] = new_date

            break

    save_data(data)

    return True