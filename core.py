# -*- coding: utf-8 -*-
"""Shared logic for the Android app: texts, Jalali dates, Persian shaping, storage, stats, study plan."""
import json
import os
from datetime import date, datetime, timedelta

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "homework_data.json")
REMIND_DAYS_BEFORE = 2
WEEK_START = 5
WEEK_END_WEEKDAY = 4
IS_ANDROID = True

# ---------------------------- Texts ----------------------------
T = {
    "fa": {
        "app": "یادآور تکالیف",
        "add": "تکلیف جدید",
        "done": "انجام شد",
        "delete": "حذف",
        "report": "گزارش هفته",
        "lang_btn": "English",
        "rtl_btn": "⇄ راست‌چین",
        "today": "امروز: {j}  |  {g}",
        "col_title": "تکلیف",
        "col_j": "شمسی",
        "col_g": "میلادی",
        "col_status": "وضعیت",
        "progress": "پیشرفت این هفته: {p}٪  ({d} از {t})",
        "select_first": "اول یک تکلیف را از لیست انتخاب کن.",
        "select_title": "انتخاب",
        "new_task": "تکلیف جدید",
        "task_title": "عنوان تکلیف:",
        "due_prompt": "تاریخ تحویل (شمسی یا میلادی)\nمثال: 1405/08/10 یا 2026-11-01",
        "bad_date": "تاریخ درست نیست.\nمثال: 1405/08/10 یا 2026-11-01",
        "error": "خطا",
        "praise": "آفرین!",
        "task_done_msg": "«{t}» انجام شد\nتکلیف و یادآورش حذف شد.",
        "del_title": "حذف",
        "del_ask": "«{t}» حذف شود؟",
        "report_title": "گزارش هفته",
        "no_tasks": "این هفته تکلیفی با موعد تحویل ثبت نشده.",
        "report_body": "هفته {w}\nشمسی: {js} تا {je}\nمیلادی: {gs} تا {ge}\n\nانجام‌شده: {d} از {t}\nدرصد: {p} از ۱۰۰",
        "r100": "\n\nعالی! همه تکالیف را انجام دادی.",
        "r70": "\n\nخوب بود، هفته بعد کامل‌تر.",
        "rlow": "\n\nهفته بعد بهتر می‌شود.",
        "s_past": "{d} روز گذشته",
        "s_today": "امروز",
        "s_soon": "{d} روز مانده",
        "s_later": "{d} روز مانده",
        "rem_title": "یادآوری تکالیف",
        "rem_head": "این تکالیف هنوز انجام نشده‌اند:",
        "rem_ok": "انجام شد",
        "rem_later": "بعداً",
        "save": "ذخیره",
        "confirm": "تایید",
        "new_week": "هفته جدید",
        "week_label": "هفته {n}",
        "newweek_q": "هفته {n} تمام شود و هفته {m} شروع شود؟\n\nانجام‌شده: {d} از {t} ({p}٪)\n{c} تکلیف انجام‌نشده به هفته جدید می‌رود.",
        "newweek_done": "هفته {m} شروع شد.\n{c} تکلیف از هفته قبل منتقل شد.",
        "carried": "منتقل‌شده از هفته {n}",
        "study_btn": "برنامه مطالعه",
        "back": "بازگشت",
        "study_title": "برنامه مطالعه",
        "add_course": "درس جدید",
        "course_name": "نام درس:",
        "course_hours": "ساعت مطالعه روزانه (مثلاً 2 یا 1.5):",
        "days_label": "روزهای مطالعه:",
        "bad_hours": "ساعت مطالعه درست نیست.\nعددی مثل 2 یا 1.5 بنویس.",
        "no_days": "حداقل یک روز را انتخاب کن.",
        "yes_btn": "مطالعه کردم",
        "no_btn": "مطالعه نکردم",
        "del_course": "حذف درس",
        "study_report_btn": "گزارش مطالعه",
        "study_ask": "آیا مطالعه کردید؟",
        "yes": "بله",
        "no": "خیر",
        "c_daily": "روزانه {h} ساعت",
        "c_wait": "امروز: منتظر پاسخ تو",
        "c_yes": "امروز: مطالعه کردی",
        "c_no": "امروز: مطالعه نکردی",
        "c_off": "امروز روز مطالعه این درس نیست.",
        "c_week": "این هفته: {sd} از {pd} روز  |  {sh} از {ph} ساعت  ({p}٪)",
        "study_empty": "هنوز درسی ثبت نشده.\nبا «درس جدید» شروع کن.",
        "study_report_title": "گزارش مطالعه هفته {w}",
        "study_report_line": "{name}: {sh} از {ph} ساعت ({p}٪)  |  {sd} از {pd} روز",
        "study_report_total": "کل: {sh} از {ph} ساعت  -  {p} از ۱۰۰",
        "study_none": "این هفته هنوز روز مطالعه‌ای ثبت نشده.",
        "continue_q": "آیا طبق هفته گذشته ادامه دهم؟\n(همین درس‌ها و ساعت‌ها)\n\nاگر «خیر» بزنی، اطلاعات صفحه مطالعه\nپاک می‌شود و از اول شروع می‌کنی.",
        "continued": "برنامه مطالعه همین‌طور ادامه پیدا کرد.",
        "cleared": "اطلاعات مطالعه پاک شد.\nدرس‌ها را از اول وارد کن.",
        "study_del_ask": "درس «{t}» حذف شود؟",
        "cancel": "انصراف",
        "close": "بستن",
    },
    "en": {
        "app": "Homework Reminder",
        "add": "New task",
        "done": "Done",
        "delete": "Delete",
        "report": "Weekly report",
        "lang_btn": "فارسی",
        "rtl_btn": "⇄ RTL fix",
        "today": "Today: {j}  |  {g}",
        "col_title": "Task",
        "col_j": "Jalali",
        "col_g": "Gregorian",
        "col_status": "Status",
        "progress": "This week's progress: {p}%  ({d} of {t})",
        "select_first": "Select a task from the list first.",
        "select_title": "Select",
        "new_task": "New task",
        "task_title": "Task title:",
        "due_prompt": "Due date (Jalali or Gregorian)\nExample: 1405/08/10 or 2026-11-01",
        "bad_date": "Invalid date.\nExample: 1405/08/10 or 2026-11-01",
        "error": "Error",
        "praise": "Well done!",
        "task_done_msg": "\"{t}\" is done\nThe task and its reminder were removed.",
        "del_title": "Delete",
        "del_ask": "Delete \"{t}\"?",
        "report_title": "Weekly report",
        "no_tasks": "No tasks are due this week.",
        "report_body": "Week {w}\nJalali: {js} to {je}\nGregorian: {gs} to {ge}\n\nCompleted: {d} of {t}\nScore: {p} out of 100",
        "r100": "\n\nExcellent! You finished every task.",
        "r70": "\n\nGood job, aim for 100% next week.",
        "rlow": "\n\nNext week will be better.",
        "s_past": "{d} day(s) overdue",
        "s_today": "Today",
        "s_soon": "{d} day(s) left",
        "s_later": "{d} day(s) left",
        "rem_title": "Homework reminder",
        "rem_head": "These tasks are still not done:",
        "rem_ok": "Done",
        "rem_later": "Later",
        "save": "Save",
        "confirm": "Confirm",
        "new_week": "New week",
        "week_label": "Week {n}",
        "newweek_q": "End week {n} and start week {m}?\n\nCompleted: {d} of {t} ({p}%)\n{c} unfinished task(s) will move to the new week.",
        "newweek_done": "Week {m} started.\n{c} task(s) carried over from last week.",
        "carried": "carried over from week {n}",
        "study_btn": "Study plan",
        "back": "Back",
        "study_title": "Study plan",
        "add_course": "New course",
        "course_name": "Course name:",
        "course_hours": "Daily study hours (e.g. 2 or 1.5):",
        "days_label": "Study days:",
        "bad_hours": "Invalid study hours.\nEnter a number like 2 or 1.5.",
        "no_days": "Select at least one day.",
        "yes_btn": "I studied",
        "no_btn": "I didn't",
        "del_course": "Delete course",
        "study_report_btn": "Study report",
        "study_ask": "Did you study?",
        "yes": "Yes",
        "no": "No",
        "c_daily": "{h} hour(s) per day",
        "c_wait": "Today: waiting for your answer",
        "c_yes": "Today: you studied",
        "c_no": "Today: you did not study",
        "c_off": "Today is not a study day for this course.",
        "c_week": "This week: {sd} of {pd} days  |  {sh} of {ph} hours  ({p}%)",
        "study_empty": "No courses yet.\nStart with \"New course\".",
        "study_report_title": "Study report - week {w}",
        "study_report_line": "{name}: {sh} of {ph} hours ({p}%)  |  {sd} of {pd} days",
        "study_report_total": "Total: {sh} of {ph} hours  -  {p} out of 100",
        "study_none": "No study days recorded this week yet.",
        "continue_q": "Continue the same as last week?\n(same courses and hours)\n\nIf you press \"No\", the study page data\nis erased and you start from scratch.",
        "continued": "The study plan continues as it was.",
        "cleared": "Study data erased.\nEnter your courses again from scratch.",
        "study_del_ask": "Delete the course \"{t}\"?",
        "cancel": "Cancel",
        "close": "Close",
    },
}

FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
TO_ASCII = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")

STUDY_ASK_HOUR = 20                 # the daily "did you study?" question appears from this hour
DAY_ORDER = [5, 6, 0, 1, 2, 3, 4]   # Saturday first (python weekday numbers)
DAY_SHORT = {"fa": {5: "ش", 6: "ی", 0: "د", 1: "س", 2: "چ", 3: "پ", 4: "ج"},
             "en": {5: "Sat", 6: "Sun", 0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu", 4: "Fri"}}
DAY_FULL = {"fa": {5: "شنبه", 6: "یکشنبه", 0: "دوشنبه", 1: "سه‌شنبه", 2: "چهارشنبه", 3: "پنج‌شنبه", 4: "جمعه"},
            "en": {5: "Saturday", 6: "Sunday", 0: "Monday", 1: "Tuesday", 2: "Wednesday",
                   3: "Thursday", 4: "Friday"}}


# ---------------------------- Jalali conversion ----------------------------
def g2j(gy, gm, gd):
    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    gy2 = gy + 1 if gm > 2 else gy
    days = (355666 + 365 * gy + (gy2 + 3) // 4 - (gy2 + 99) // 100
            + (gy2 + 399) // 400 + gd + g_d_m[gm - 1])
    jy = -1595 + 33 * (days // 12053)
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm = 1 + days // 31
        jd = 1 + days % 31
    else:
        jm = 7 + (days - 186) // 30
        jd = 1 + (days - 186) % 30
    return jy, jm, jd


def j2g(jy, jm, jd):
    jy += 1595
    days = -355668 + 365 * jy + (jy // 33) * 8 + ((jy % 33) + 3) // 4 + jd
    days += (jm - 1) * 31 if jm < 7 else (jm - 7) * 30 + 186
    gy = 400 * (days // 146097)
    days %= 146097
    if days > 36524:
        days -= 1
        gy += 100 * (days // 36524)
        days %= 36524
        if days >= 365:
            days += 1
    gy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        gy += (days - 1) // 365
        days = (days - 1) % 365
    gd = days + 1
    leap = (gy % 4 == 0 and gy % 100 != 0) or gy % 400 == 0
    sal_a = [0, 31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    while gm < 13 and gd > sal_a[gm]:
        gd -= sal_a[gm]
        gm += 1
    return gy, gm, gd


def date_to_jalali_str(d):
    y, m, dd = g2j(d.year, d.month, d.day)
    return f"{y:04d}/{m:02d}/{dd:02d}"


def parse_any_date(text):
    """Accepts Jalali or Gregorian, English or Persian digits. Returns a date (Gregorian)."""
    s = text.strip().translate(TO_ASCII).replace("/", "-").replace(".", "-")
    parts = s.split("-")
    if len(parts) != 3:
        raise ValueError("format")
    y, m, d = (int(p) for p in parts)
    if y < 1700:                      # Jalali year
        if not (1 <= m <= 12 and 1 <= d <= 31):
            raise ValueError("range")
        gy, gm, gd = j2g(y, m, d)
        result = date(gy, gm, gd)
        if g2j(result.year, result.month, result.day) != (y, m, d):
            raise ValueError("invalid jalali date")
        return result
    return date(y, m, d)              # Gregorian (raises ValueError if invalid)



# ---------------------------- Persian text shaping (display only) ----------------------------
# letter: (isolated, final, initial, medial)  -> 2-tuple = does not join to the next letter
_FORMS = {
    "ء": (0xFE80,), "آ": (0xFE81, 0xFE82), "أ": (0xFE83, 0xFE84), "ؤ": (0xFE85, 0xFE86),
    "إ": (0xFE87, 0xFE88), "ئ": (0xFE89, 0xFE8A, 0xFE8B, 0xFE8C), "ا": (0xFE8D, 0xFE8E),
    "ب": (0xFE8F, 0xFE90, 0xFE91, 0xFE92), "ة": (0xFE93, 0xFE94),
    "ت": (0xFE95, 0xFE96, 0xFE97, 0xFE98), "ث": (0xFE99, 0xFE9A, 0xFE9B, 0xFE9C),
    "ج": (0xFE9D, 0xFE9E, 0xFE9F, 0xFEA0), "ح": (0xFEA1, 0xFEA2, 0xFEA3, 0xFEA4),
    "خ": (0xFEA5, 0xFEA6, 0xFEA7, 0xFEA8), "د": (0xFEA9, 0xFEAA), "ذ": (0xFEAB, 0xFEAC),
    "ر": (0xFEAD, 0xFEAE), "ز": (0xFEAF, 0xFEB0),
    "س": (0xFEB1, 0xFEB2, 0xFEB3, 0xFEB4), "ش": (0xFEB5, 0xFEB6, 0xFEB7, 0xFEB8),
    "ص": (0xFEB9, 0xFEBA, 0xFEBB, 0xFEBC), "ض": (0xFEBD, 0xFEBE, 0xFEBF, 0xFEC0),
    "ط": (0xFEC1, 0xFEC2, 0xFEC3, 0xFEC4), "ظ": (0xFEC5, 0xFEC6, 0xFEC7, 0xFEC8),
    "ع": (0xFEC9, 0xFECA, 0xFECB, 0xFECC), "غ": (0xFECD, 0xFECE, 0xFECF, 0xFED0),
    "ف": (0xFED1, 0xFED2, 0xFED3, 0xFED4), "ق": (0xFED5, 0xFED6, 0xFED7, 0xFED8),
    "ك": (0xFED9, 0xFEDA, 0xFEDB, 0xFEDC), "ل": (0xFEDD, 0xFEDE, 0xFEDF, 0xFEE0),
    "م": (0xFEE1, 0xFEE2, 0xFEE3, 0xFEE4), "ن": (0xFEE5, 0xFEE6, 0xFEE7, 0xFEE8),
    "ه": (0xFEE9, 0xFEEA, 0xFEEB, 0xFEEC), "و": (0xFEED, 0xFEEE),
    "ى": (0xFEEF, 0xFEF0), "ي": (0xFEF1, 0xFEF2, 0xFEF3, 0xFEF4),
    # Persian-specific letters
    "پ": (0xFB56, 0xFB57, 0xFB58, 0xFB59), "چ": (0xFB7A, 0xFB7B, 0xFB7C, 0xFB7D),
    "ژ": (0xFB8A, 0xFB8B), "ک": (0xFB8E, 0xFB8F, 0xFB90, 0xFB91),
    "گ": (0xFB92, 0xFB93, 0xFB94, 0xFB95), "ی": (0xFBFC, 0xFBFD, 0xFBFE, 0xFBFF),
}
_LAMALEF = {"ا": (0xFEFB, 0xFEFC), "آ": (0xFEF5, 0xFEF6), "أ": (0xFEF7, 0xFEF8), "إ": (0xFEF9, 0xFEFA)}
_MIRROR = str.maketrans("()[]{}<>«»", ")(][}{><»«")


def shape_persian(text):
    """Replace letters by their joined (initial/medial/final) presentation forms."""
    n, out, i, prev_joins = len(text), [], 0, False
    while i < n:
        c = text[i]
        if c == "‌":                       # ZWNJ: breaks joining, not drawn
            prev_joins = False
            i += 1
            continue
        if c not in _FORMS:
            out.append(c)
            prev_joins = False
            i += 1
            continue
        if c == "ل" and i + 1 < n and text[i + 1] in _LAMALEF:
            iso, fin = _LAMALEF[text[i + 1]]
            out.append(chr(fin if prev_joins else iso))
            prev_joins = False
            i += 2
            continue
        f = _FORMS[c]
        nxt = text[i + 1] if i + 1 < n else ""
        next_joins = len(f) == 4 and nxt in _FORMS
        if len(f) == 4:
            idx = 3 if (prev_joins and next_joins) else 1 if prev_joins else 2 if next_joins else 0
        elif len(f) == 2:
            idx = 1 if prev_joins else 0
        else:
            idx = 0
        out.append(chr(f[idx]))
        prev_joins = next_joins
        i += 1
    return "".join(out)


def _cls(c):
    o = ord(c)
    if (0x06F0 <= o <= 0x06F9) or (0x0660 <= o <= 0x0669):
        return "L"                                   # digits keep left-to-right order
    if 0x0600 <= o <= 0x06FF or 0xFB50 <= o <= 0xFDFF or 0xFE70 <= o <= 0xFEFF:
        return "R"
    if c.isalnum():
        return "L"
    return "N"


def _visual_line(line):
    """Very small bidi: right-to-left paragraph, digits/Latin runs stay left-to-right."""
    classes = [_cls(c) for c in line]
    n = len(classes)
    for i in range(n):
        if classes[i] != "N":
            continue
        left = next((classes[j] for j in range(i - 1, -1, -1) if classes[j] != "N"), None)
        right = next((classes[j] for j in range(i + 1, n) if classes[j] != "N"), None)
        classes[i] = "N_L" if (left == "L" and right == "L") else "N_R"
    classes = ["L" if c in ("L", "N_L") else "R" for c in classes]
    runs, start = [], 0
    for i in range(1, n + 1):
        if i == n or classes[i] != classes[start]:
            runs.append((classes[start], line[start:i]))
            start = i
    out = []
    for kind, s in reversed(runs):
        out.append(s[::-1].translate(_MIRROR) if kind == "R" else s)
    return "".join(out)


def persian_visual(text):
    """Logical Persian string -> string that displays correctly on renderers without bidi/shaping."""
    if not any(_cls(c) == "R" for c in text):
        return text
    return "\n".join(_visual_line(shape_persian(line)) for line in text.split("\n"))


# ---------------------------- Storage ----------------------------
def data_path():
    try:
        from android.storage import app_storage_path  # type: ignore
        return os.path.join(app_storage_path(), "homework_data.json")
    except Exception:
        return DATA_FILE


def load_data():
    default = {"tasks": [], "history": [], "next_id": 1, "last_reminded": "",
               "last_report_week": "", "lang": "fa", "rtl_fix": IS_ANDROID,
               "week_number": 1, "week_start": "", "weeks_log": [], "study": new_study()}
    if os.path.exists(data_path()):
        try:
            with open(data_path(), "r", encoding="utf-8") as f:
                data = json.load(f)
            for k, v in default.items():
                data.setdefault(k, v)
            if not data["week_start"]:
                data["week_start"] = week_range(date.today())[0].isoformat()
            for k, v in new_study().items():
                data["study"].setdefault(k, v)
            for h in data["history"]:
                h.setdefault("week", 1)       # old entries belong to the first week, not to every week
            return data
        except (json.JSONDecodeError, OSError):
            pass
    default["week_start"] = week_range(date.today())[0].isoformat()
    return default


def save_data(data):
    with open(data_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ---------------------------- Logic ----------------------------
def parse_date(s):
    return datetime.strptime(s, "%Y-%m-%d").date()


def week_range(today):
    start = today - timedelta(days=(today.weekday() - WEEK_START) % 7)
    return start, start + timedelta(days=6)


def days_left(task, today):
    return (parse_date(task["due"]) - today).days


def current_week(data):
    return data.get("week_number", 1)


def week_start_date(data, today):
    s = data.get("week_start")
    return parse_date(s) if s else week_range(today)[0]


def weekly_stats(data, today):
    """Stats of the current (manual) week. Done tasks are in history, unfinished ones in tasks."""
    n = current_week(data)
    active = [t for t in data["tasks"] if t.get("week", n) == n]
    finished = [h for h in data["history"] if h.get("week", n) == n]
    done, total = len(finished), len(finished) + len(active)
    percent = round(done / total * 100) if total else 0
    return week_start_date(data, today), today, done, total, percent


def start_new_week(data, today):
    """Close the current week; every unfinished task moves into the new week."""
    n = current_week(data)
    start, _, done, total, percent = weekly_stats(data, today)
    data.setdefault("weeks_log", []).append({
        "week": n, "start": start.isoformat(), "end": today.isoformat(),
        "done": done, "total": total, "percent": percent})
    m = n + 1
    for t in data["tasks"]:
        t["week"] = m
        t["from_week"] = n
    data["week_number"] = m
    data["week_start"] = today.isoformat()
    save_data(data)
    return n, m, len(data["tasks"])


def new_study():
    return {"courses": [], "log": [], "next_id": 1, "last_asked": "", "last_report_week": ""}


def parse_hours(text):
    s = text.strip().translate(TO_ASCII).replace("٫", ".").replace(",", ".").replace("،", ".")
    h = float(s)
    if not (0.1 <= h <= 24):
        raise ValueError("hours")
    return h


def fmt_hours(x):
    return f"{x:g}"


def study_entry(data, cid, day):
    iso = day.isoformat()
    return next((e for e in data["study"]["log"] if e["c"] == cid and e["date"] == iso), None)


def pending_study(data, today):
    """Courses scheduled for today that have not been answered yet."""
    return [c for c in data["study"]["courses"]
            if today.weekday() in c["days"] and parse_date(c["start"]) <= today
            and study_entry(data, c["id"], today) is None]


def answer_study(data, cid, day, studied):
    e = study_entry(data, cid, day)
    if e is None:
        e = {"c": cid, "date": day.isoformat(), "done": bool(studied)}
        data["study"]["log"].append(e)
    e["done"] = bool(studied)
    save_data(data)


def course_week_stats(data, course, today):
    """(planned_days, studied_days, planned_hours, studied_hours, percent) for the current week.
    Past days with no answer count as 'not studied'; today counts only once answered."""
    start = week_start_date(data, today)
    end = min(today, start + timedelta(days=6))
    day = max(start, parse_date(course["start"]))
    planned = studied = 0
    while day <= end:
        if day.weekday() in course["days"]:
            e = study_entry(data, course["id"], day)
            if not (day == today and e is None):
                planned += 1
                if e and e["done"]:
                    studied += 1
        day += timedelta(days=1)
    ph, sh = planned * course["hours"], studied * course["hours"]
    return planned, studied, ph, sh, (round(sh / ph * 100) if ph else 0)


def study_week_report(data, today):
    rows = [(c, course_week_stats(data, c, today)) for c in data["study"]["courses"]]
    ph = sum(r[1][2] for r in rows)
    sh = sum(r[1][3] for r in rows)
    return rows, sh, ph, (round(sh / ph * 100) if ph else 0)


def clear_study(data):
    data["study"] = new_study()
    save_data(data)


def status_key(task, today):
    d = days_left(task, today)
    if d < 0:
        return "s_past", abs(d), "over"
    if d == 0:
        return "s_today", 0, "over"
    if d <= REMIND_DAYS_BEFORE:
        return "s_soon", d, "soon"
    return "s_later", d, "later"




def pending_reminders(data, today):
    return [t for t in data["tasks"] if days_left(t, today) <= REMIND_DAYS_BEFORE]


def complete_task(data, t):
    """Done = remove the task (and its reminder) but keep it in history for the weekly score."""
    if t in data["tasks"]:
        data["tasks"].remove(t)
    data["history"].append({"id": t["id"], "title": t["title"], "due": t["due"],
                            "week": t.get("week", current_week(data)),
                            "done_at": datetime.now().isoformat(timespec="seconds")})
    save_data(data)
