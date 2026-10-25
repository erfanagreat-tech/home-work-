# -*- coding: utf-8 -*-
"""Background service: puts reminders in the phone's top bar.
 - homework: once a day (after 08:00) while unfinished tasks are due within 2 days / overdue
 - study:    once a day (after the study hour, 20:00) for courses scheduled today and not answered yet
"""
import json
import os
import time
from datetime import date, datetime

import core

CHECK_SECONDS = 5 * 60
REMIND_HOUR = 8
STATE = os.path.join(os.path.dirname(core.data_path()), "reminder_state.json")


def load_state():
    try:
        with open(STATE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def save_state(state):
    try:
        with open(STATE, "w", encoding="utf-8") as f:
            json.dump(state, f)
    except OSError:
        pass


def notify(title, message):
    try:
        from plyer import notification
        notification.notify(title=title, message=message, app_name="Homework", timeout=20)
    except Exception:
        pass


while True:
    try:
        now = datetime.now()
        today = date.today()
        iso = today.isoformat()
        state = load_state()
        data = None

        if now.hour >= REMIND_HOUR and state.get("hw") != iso:
            data = core.load_data()
            lang = data.get("lang", "fa")
            pend = core.pending_reminders(data, today)
            if pend:
                lines = []
                for t in pend:
                    key, n, _ = core.status_key(t, today)
                    lines.append(f"{t['title']} - {core.T[lang][key].format(d=n)}")
                notify(core.T[lang]["rem_title"], "\n".join(lines))
                state["hw"] = iso

        if now.hour >= core.STUDY_ASK_HOUR and state.get("study") != iso:
            data = data or core.load_data()
            lang = data.get("lang", "fa")
            pend = core.pending_study(data, today)
            if pend:
                notify(core.T[lang]["study_ask"], "\n".join(c["name"] for c in pend))
                state["study"] = iso

        save_state(state)
    except Exception:
        pass
    time.sleep(CHECK_SECONDS)
