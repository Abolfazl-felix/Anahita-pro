import json
import os
from config import DATA_FILE


def load_events():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_events(events):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(events, f, ensure_ascii=False, indent=4)


def add_event(name, date):
    events = load_events()

    events.append(
        {
            "name": name,
            "date": date
        }
    )

    save_events(events)


def delete_event(index):
    events = load_events()

    if index < 0 or index >= len(events):
        return None

    removed = events.pop(index)

    save_events(events)

    return removed


def list_events():
    return load_events()


def edit_event(index, name, date):

    events = load_events()

    if index < 0 or index >= len(events):
        return False

    events[index]["name"] = name
    events[index]["date"] = date

    save_events(events)

    return True