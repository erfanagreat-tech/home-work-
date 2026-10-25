# -*- coding: utf-8 -*-
"""Homework + Study Reminder (Android, Kivy) - offline, Persian/English, Jalali+Gregorian, gray/orange."""
import os
from datetime import date, datetime, timedelta

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp, sp
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex as hx

import core
from core import T, FA_DIGITS, persian_visual

Window.softinput_mode = "pan"      # keep the input box visible above the keyboard

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = os.path.join(HERE, "font.ttf")          # DejaVu Sans: has Persian glyph forms
if not os.path.exists(FONT):
    FONT = "Roboto"

BG, PANEL, PANEL_2 = hx("#2b2b2b"), hx("#363636"), hx("#4a4a4a")
ROW_A, ROW_B = hx("#333333"), hx("#3b3b3b")
TEXT, MUTED, DARK = hx("#f2f2f2"), hx("#a8a8a8"), hx("#1c1c1c")
ORANGE, ORANGE_SOFT = hx("#ff8c1a"), hx("#ffb866")


class Panel(BoxLayout):
    """BoxLayout with a solid background colour."""

    def __init__(self, bg, **kw):
        super().__init__(**kw)
        with self.canvas.before:
            Color(*bg)
            self._rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._upd, size=self._upd)

    def _upd(self, *_):
        self._rect.pos, self._rect.size = self.pos, self.size


class Bar(Widget):
    """Orange progress bar (0-100)."""
    value = NumericProperty(0)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.bind(pos=self._draw, size=self._draw, value=self._draw)

    def _draw(self, *_):
        self.canvas.clear()
        with self.canvas:
            Color(*PANEL_2)
            Rectangle(pos=self.pos, size=self.size)
            Color(*ORANGE)
            Rectangle(pos=self.pos, size=(self.width * max(0, min(100, self.value)) / 100, self.height))


def make_label(text="", size=14, color=TEXT, height=None, bold=False, **kw):
    lb = Label(text=text, font_name=FONT, font_size=sp(size), color=color, bold=bold, **kw)
    if height:
        lb.size_hint_y = None
        lb.height = dp(height)
    lb.bind(size=lambda w, v: setattr(w, "text_size", (v[0], None)))
    return lb


class HomeworkApp(App):
    def build(self):
        self.title = "Homework Reminder"
        self.data = core.load_data()
        self.selected_id = None
        self.study_selected = None
        self.btns = []
        Window.clearcolor = BG
        Window.bind(on_keyboard=self.on_key)

        self.container = BoxLayout()
        self.home = self._build_home()
        self.study_page = self._build_study()
        self.container.add_widget(self.home)

        self.apply_language()
        self.start_service()
        Clock.schedule_once(lambda dt: self.tick(), 1)
        Clock.schedule_interval(lambda dt: self.tick(), 60)
        return self.container

    # ---------- helpers ----------
    @property
    def lang(self):
        return self.data.get("lang", "fa")

    def tr(self, key, **kw):
        s = T[self.lang][key]
        return s.format(**kw) if kw else s

    def num(self, s):
        s = str(s)
        return s.translate(FA_DIGITS) if self.lang == "fa" else s

    def d(self, text):
        return persian_visual(text)

    def mkbtn(self, key, cb, primary):
        b = Button(font_name=FONT, font_size=sp(16), bold=primary, background_normal="",
                   background_down="", background_color=ORANGE if primary else PANEL_2,
                   color=DARK if primary else TEXT)
        b.bind(on_release=lambda *_: cb())
        self.btns.append((b, key))
        return b

    def text_input(self, text=""):
        return TextInput(text=text, multiline=False, size_hint_y=None, height=dp(46), font_name=FONT,
                         font_size=sp(16), background_color=DARK, foreground_color=TEXT,
                         cursor_color=ORANGE, padding=(dp(10), dp(12)))

    def popup(self, title, content, height):
        p = Popup(title=self.d(title), content=content, size_hint=(0.94, None), height=dp(height),
                  pos_hint={"center_x": 0.5, "top": 0.97}, auto_dismiss=False,
                  title_font=FONT, title_color=ORANGE, title_size=sp(18), title_align="center",
                  separator_color=ORANGE, background="", background_color=PANEL)
        p.open()
        return p

    def dlg_button(self, key, cb, primary=True):
        b = Button(text=self.d(self.tr(key)), font_name=FONT, font_size=sp(16), bold=primary,
                   background_normal="", background_down="",
                   background_color=ORANGE if primary else PANEL_2, color=DARK if primary else TEXT)
        b.bind(on_release=lambda *_: cb())
        return b

    def msg(self, title, text, height=300):
        box = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        lb = Label(text=self.d(text), font_name=FONT, font_size=sp(15), color=TEXT,
                   halign="center", valign="middle")
        lb.bind(size=lambda w, v: setattr(w, "text_size", v))
        box.add_widget(lb)
        p = self.popup(title, box, height)
        btn = self.dlg_button("close", p.dismiss)
        btn.size_hint_y = None
        btn.height = dp(48)
        box.add_widget(btn)
        return p

    def confirm(self, title, text, yes_key, no_key, on_yes, on_no=None, height=300):
        """Popup with two buttons."""
        box = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        lb = Label(text=self.d(text), font_name=FONT, font_size=sp(15), color=TEXT,
                   halign="center", valign="middle")
        lb.bind(size=lambda w, v: setattr(w, "text_size", v))
        box.add_widget(lb)
        row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        p = self.popup(title, box, height)

        def yes():
            p.dismiss()
            on_yes()

        def no():
            p.dismiss()
            if on_no:
                on_no()

        row.add_widget(self.dlg_button(yes_key, yes))
        row.add_widget(self.dlg_button(no_key, no, False))
        box.add_widget(row)
        return p

    def on_key(self, window, key, *args):
        if key == 27 and self.study_page.parent is not None:   # Android back button
            self.hide_study()
            return True
        return False

    # ================= HOME PAGE =================
    def _build_home(self):
        root = BoxLayout(orientation="vertical", spacing=dp(6))
        head = Panel(DARK, orientation="vertical", size_hint_y=None, height=dp(120), padding=dp(6))
        self.title_label = make_label(size=26, color=ORANGE, bold=True, halign="center")
        self.week_label = make_label(size=18, color=ORANGE_SOFT, height=30, bold=True, halign="center")
        self.today_label = make_label(size=13, color=MUTED, height=24, halign="center")
        head.add_widget(self.title_label)
        head.add_widget(self.week_label)
        head.add_widget(self.today_label)
        root.add_widget(head)

        pad = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(6))
        lang_btn = self.mkbtn("lang_btn", self.toggle_language, False)
        lang_btn.size_hint_y = None
        lang_btn.height = dp(44)
        pad.add_widget(lang_btn)

        self.scroll = ScrollView(do_scroll_x=False, bar_color=ORANGE, bar_width=dp(4))
        self.list_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(6))
        self.list_box.bind(minimum_height=self.list_box.setter("height"))
        self.scroll.add_widget(self.list_box)
        pad.add_widget(self.scroll)

        self.progress_label = make_label(size=14, height=28, halign="center")
        pad.add_widget(self.progress_label)
        self.bar = Bar(size_hint_y=None, height=dp(14))
        pad.add_widget(self.bar)

        for specs, h in (([("add", self.add_task, True), ("done", self.mark_done, True)], 54),
                         ([("delete", self.delete_task, False), ("report", self.show_report, False)], 48),
                         ([("new_week", self.new_week, False)], 48),
                         ([("study_btn", self.show_study, True)], 52)):
            row = BoxLayout(size_hint_y=None, height=dp(h), spacing=dp(6))
            for key, cb, primary in specs:
                row.add_widget(self.mkbtn(key, cb, primary))
            pad.add_widget(row)
        root.add_widget(pad)
        return root

    def apply_language(self):
        self.title_label.text = self.d(self.tr("app"))
        self.study_title.text = self.d(self.tr("study_title"))
        for b, key in self.btns:
            b.text = self.d(self.tr(key))
        self.refresh()
        self.refresh_study()

    def toggle_language(self):
        self.data["lang"] = "en" if self.lang == "fa" else "fa"
        core.save_data(self.data)
        self.apply_language()

    def refresh(self):
        today = date.today()
        self.week_label.text = self.d(self.num(self.tr("week_label", n=core.current_week(self.data))))
        self.today_label.text = self.d(self.num(self.tr(
            "today", j=core.date_to_jalali_str(today), g=today.isoformat())))
        self.list_box.clear_widgets()
        tasks = sorted(self.data["tasks"], key=lambda t: t["due"])
        if self.selected_id not in [t["id"] for t in tasks]:
            self.selected_id = None
        for i, t in enumerate(tasks):
            dd = core.parse_date(t["due"])
            key, n, tag = core.status_key(t, today)
            sel = t["id"] == self.selected_id
            st_color = {"over": "ff8c1a", "soon": "ffb866", "later": "a8a8a8"}[tag]
            if sel:
                st_color = "1c1c1c"
            title = t["title"].replace("[", "(").replace("]", ")")
            dates = self.num(f"{self.tr('col_j')}: {core.date_to_jalali_str(dd)}    "
                             f"{self.tr('col_g')}: {dd.isoformat()}")
            status = self.num(self.tr(key, d=n))
            sub = "1c1c1c" if sel else "a8a8a8"
            carried = ""
            if t.get("from_week"):
                carried = (f"\n[size={int(sp(12))}][color={sub}]"
                           f"{self.d(self.num(self.tr('carried', n=t['from_week'])))}[/color][/size]")
            text = (f"[b]{self.d(title)}[/b]\n[size={int(sp(13))}][color={sub}]{self.d(dates)}[/color][/size]\n"
                    f"[size={int(sp(13))}][color={st_color}]{self.d(status)}[/color][/size]" + carried)
            card = Button(text=text, markup=True, font_name=FONT, font_size=sp(16),
                          size_hint_y=None, height=dp(120 if t.get("from_week") else 96),
                          halign="center", valign="middle",
                          background_normal="", background_down="",
                          background_color=ORANGE if sel else (ROW_A if i % 2 == 0 else ROW_B),
                          color=DARK if sel else TEXT)
            card.bind(size=lambda w, v: setattr(w, "text_size", (v[0] - dp(12), v[1])))
            card.bind(on_release=lambda b, tid=t["id"]: self.select(tid))
            self.list_box.add_widget(card)
        _, _, done, total, percent = core.weekly_stats(self.data, today)
        self.bar.value = percent
        self.progress_label.text = self.d(self.num(self.tr("progress", p=percent, d=done, t=total)))

    def select(self, tid):
        self.selected_id = tid
        self.refresh()

    def selected_task(self):
        t = next((x for x in self.data["tasks"] if x["id"] == self.selected_id), None)
        if t is None:
            self.msg(self.tr("select_title"), self.tr("select_first"), 230)
        return t

    # ---------- homework actions ----------
    def add_task(self):
        box = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(6))
        box.add_widget(make_label(self.d(self.tr("task_title")), 14, MUTED, 26, halign="center"))
        title_in = self.text_input()
        box.add_widget(title_in)
        # the box shows separate letters; this line shows the joined text live
        preview = make_label("", 20, ORANGE, 40, bold=True, halign="center")
        title_in.bind(text=lambda w, v: setattr(preview, "text", self.d(v)))
        box.add_widget(preview)
        box.add_widget(make_label(self.d(self.tr("due_prompt")), 13, MUTED, 48, halign="center"))
        default_d = date.today() + timedelta(days=3)
        default = core.date_to_jalali_str(default_d) if self.lang == "fa" else default_d.isoformat()
        date_in = self.text_input(self.num(default))
        date_in.halign = "center"
        box.add_widget(date_in)
        row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        p = self.popup(self.tr("new_task"), box, 400)

        def save():
            title = title_in.text.strip()
            if not title:
                return
            try:
                due = core.parse_any_date(date_in.text)
            except (ValueError, OverflowError):
                self.msg(self.tr("error"), self.tr("bad_date"), 240)
                return
            self.data["tasks"].append({"id": self.data["next_id"], "title": title,
                                       "due": due.isoformat(), "week": core.current_week(self.data),
                                       "created_at": date.today().isoformat()})
            self.data["next_id"] += 1
            core.save_data(self.data)
            p.dismiss()
            self.refresh()

        row.add_widget(self.dlg_button("save", save))
        row.add_widget(self.dlg_button("cancel", p.dismiss, False))
        box.add_widget(row)

    def mark_done(self):
        t = self.selected_task()
        if t is None:
            return
        core.complete_task(self.data, t)       # removes the task and its reminder
        self.selected_id = None
        self.refresh()
        self.msg(self.tr("praise"), self.tr("task_done_msg", t=t["title"]), 280)

    def delete_task(self):
        t = self.selected_task()
        if t is None:
            return

        def yes():
            self.data["tasks"].remove(t)
            self.selected_id = None
            core.save_data(self.data)
            self.refresh()

        self.confirm(self.tr("del_title"), self.tr("del_ask", t=t["title"]), "delete", "cancel", yes, height=230)

    def show_report(self):
        start, end, done, total, percent = core.weekly_stats(self.data, date.today())
        if total == 0:
            text = self.tr("no_tasks")
        else:
            text = self.tr("report_body", w=core.current_week(self.data),
                           js=core.date_to_jalali_str(start), je=core.date_to_jalali_str(end),
                           gs=start.isoformat(), ge=end.isoformat(), d=done, t=total, p=percent)
            text += self.tr("r100" if percent == 100 else "r70" if percent >= 70 else "rlow")
            text = self.num(text)
        self.msg(self.tr("report_title"), text, 420)

    def new_week(self):
        today = date.today()
        _, _, done, total, percent = core.weekly_stats(self.data, today)
        n = core.current_week(self.data)
        text = self.num(self.tr("newweek_q", n=n, m=n + 1, d=done, t=total, p=percent,
                                c=len(self.data["tasks"])))

        def go():
            _, m, carried = core.start_new_week(self.data, today)
            self.selected_id = None
            self.refresh()
            self.msg(self.tr("praise"), self.num(self.tr("newweek_done", m=m, c=carried)), 260)
            self.ask_continue_study()

        self.confirm(self.tr("new_week"), text, "confirm", "cancel", go, height=360)

    def ask_continue_study(self):
        """Every new week: continue the study plan as last week, or erase it and start again."""
        if not self.data["study"]["courses"]:
            return

        def keep():
            self.msg(self.tr("study_title"), self.tr("continued"), 230)

        def wipe():
            core.clear_study(self.data)
            self.study_selected = None
            self.refresh_study()
            self.msg(self.tr("study_title"), self.tr("cleared"), 250)

        self.confirm(self.tr("study_title"), self.tr("continue_q"), "yes", "no", keep, wipe, height=380)

    # ================= STUDY PAGE =================
    def _build_study(self):
        page = BoxLayout(orientation="vertical", spacing=dp(6))
        head = Panel(DARK, orientation="vertical", size_hint_y=None, height=dp(92), padding=dp(6))
        self.study_title = make_label(size=24, color=ORANGE, bold=True, halign="center")
        self.study_sub = make_label(size=13, color=MUTED, height=24, halign="center")
        head.add_widget(self.study_title)
        head.add_widget(self.study_sub)
        page.add_widget(head)

        pad = BoxLayout(orientation="vertical", padding=dp(8), spacing=dp(6))
        sv = ScrollView(do_scroll_x=False, bar_color=ORANGE, bar_width=dp(4))
        self.study_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(6))
        self.study_box.bind(minimum_height=self.study_box.setter("height"))
        sv.add_widget(self.study_box)
        pad.add_widget(sv)
        for specs in ([("yes_btn", lambda: self.answer_selected(True), True),
                       ("no_btn", lambda: self.answer_selected(False), False)],
                      [("add_course", self.add_course, True), ("del_course", self.delete_course, False)],
                      [("study_report_btn", self.show_study_report, False), ("back", self.hide_study, False)]):
            row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))
            for key, cb, primary in specs:
                row.add_widget(self.mkbtn(key, cb, primary))
            pad.add_widget(row)
        page.add_widget(pad)
        return page

    def show_study(self):
        self.container.clear_widgets()
        self.container.add_widget(self.study_page)
        self.refresh_study()

    def hide_study(self):
        self.container.clear_widgets()
        self.container.add_widget(self.home)
        self.refresh()

    def day_names(self, course):
        names = [core.DAY_FULL[self.lang][wd] for wd in core.DAY_ORDER if wd in course["days"]]
        if len(names) == 7:
            return "هر روز" if self.lang == "fa" else "Every day"
        sep = "، " if self.lang == "fa" else ", "
        return "\n".join(sep.join(names[i:i + 3]) for i in range(0, len(names), 3))

    def refresh_study(self):
        today = date.today()
        self.study_sub.text = self.d(self.num(self.tr(
            "today", j=core.date_to_jalali_str(today), g=today.isoformat())))
        self.study_box.clear_widgets()
        courses = self.data["study"]["courses"]
        if self.study_selected not in [c["id"] for c in courses]:
            self.study_selected = None
        if not courses:
            self.study_box.add_widget(make_label(self.d(self.tr("study_empty")), 15, MUTED, 140,
                                                 halign="center", valign="middle"))
        for i, c in enumerate(courses):
            sel = c["id"] == self.study_selected
            e = core.study_entry(self.data, c["id"], today)
            if today.weekday() not in c["days"] or core.parse_date(c["start"]) > today:
                state, color = self.tr("c_off"), "a8a8a8"
            elif e is None:
                state, color = self.tr("c_wait"), "ffb866"
            elif e["done"]:
                state, color = self.tr("c_yes"), "ff8c1a"
            else:
                state, color = self.tr("c_no"), "a8a8a8"
            pd, sd, ph, sh, pc = core.course_week_stats(self.data, c, today)
            names = self.day_names(c)
            sub = "1c1c1c" if sel else "a8a8a8"
            st_color = "1c1c1c" if sel else color
            size = int(sp(13))
            text = (f"[b]{self.d(c['name'].replace('[', '(').replace(']', ')'))}[/b]\n"
                    f"[size={size}][color={sub}]{self.d(self.num(self.tr('c_daily', h=core.fmt_hours(c['hours']))))}[/color][/size]\n"
                    f"[size={size}][color={sub}]{self.d(names)}[/color][/size]\n"
                    f"[size={size}][color={st_color}]{self.d(self.num(state))}[/color][/size]\n"
                    f"[size={size}][color={sub}]"
                    f"{self.d(self.num(self.tr('c_week', sd=sd, pd=pd, sh=core.fmt_hours(sh), ph=core.fmt_hours(ph), p=pc)))}"
                    f"[/color][/size]")
            lines = 4 + names.count("\n") + 1
            card = Button(text=text, markup=True, font_name=FONT, font_size=sp(16),
                          size_hint_y=None, height=dp(24 * lines + 24), halign="center", valign="middle",
                          background_normal="", background_down="",
                          background_color=ORANGE if sel else (ROW_A if i % 2 == 0 else ROW_B),
                          color=DARK if sel else TEXT)
            card.bind(size=lambda w, v: setattr(w, "text_size", (v[0] - dp(12), v[1])))
            card.bind(on_release=lambda b, cid=c["id"]: self.select_course(cid))
            self.study_box.add_widget(card)

    def select_course(self, cid):
        self.study_selected = cid
        self.refresh_study()

    def selected_course(self):
        c = next((x for x in self.data["study"]["courses"] if x["id"] == self.study_selected), None)
        if c is None:
            self.msg(self.tr("select_title"), self.tr("select_first"), 230)
        return c

    def answer_selected(self, studied):
        c = self.selected_course()
        if c is None:
            return
        today = date.today()
        if today.weekday() not in c["days"]:
            self.msg(self.tr("study_title"), self.tr("c_off"), 230)
            return
        core.answer_study(self.data, c["id"], today, studied)
        self.refresh_study()

    def add_course(self):
        box = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(6))
        box.add_widget(make_label(self.d(self.tr("course_name")), 14, MUTED, 24, halign="center"))
        name_in = self.text_input()
        box.add_widget(name_in)
        preview = make_label("", 20, ORANGE, 36, bold=True, halign="center")
        name_in.bind(text=lambda w, v: setattr(preview, "text", self.d(v)))
        box.add_widget(preview)
        box.add_widget(make_label(self.d(self.tr("course_hours")), 13, MUTED, 40, halign="center"))
        hours_in = self.text_input(self.num("2"))
        hours_in.halign = "center"
        box.add_widget(hours_in)
        box.add_widget(make_label(self.d(self.tr("days_label")), 13, MUTED, 28, halign="center"))
        dayrow = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(3))
        order = list(core.DAY_ORDER)
        if self.lang == "fa":
            order.reverse()                      # Saturday on the right
        toggles = []
        for wd in order:
            tb = ToggleButton(text=self.d(core.DAY_SHORT[self.lang][wd]), font_name=FONT, font_size=sp(14),
                              background_normal="", background_down="", background_color=PANEL_2, color=TEXT)
            tb.bind(state=lambda w, st: setattr(w, "background_color", ORANGE if st == "down" else PANEL_2))
            dayrow.add_widget(tb)
            toggles.append((wd, tb))
        box.add_widget(dayrow)
        row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        p = self.popup(self.tr("add_course"), box, 520)

        def save():
            name = name_in.text.strip()
            if not name:
                return
            try:
                hours = core.parse_hours(hours_in.text)
            except ValueError:
                self.msg(self.tr("error"), self.tr("bad_hours"), 250)
                return
            days = [wd for wd, tb in toggles if tb.state == "down"]
            if not days:
                self.msg(self.tr("error"), self.tr("no_days"), 230)
                return
            st = self.data["study"]
            st["courses"].append({"id": st["next_id"], "name": name, "hours": hours, "days": days,
                                  "start": date.today().isoformat()})
            st["next_id"] += 1
            core.save_data(self.data)
            p.dismiss()
            self.refresh_study()

        row.add_widget(self.dlg_button("save", save))
        row.add_widget(self.dlg_button("cancel", p.dismiss, False))
        box.add_widget(row)

    def delete_course(self):
        c = self.selected_course()
        if c is None:
            return

        def yes():
            st = self.data["study"]
            st["courses"].remove(c)
            st["log"] = [e for e in st["log"] if e["c"] != c["id"]]
            self.study_selected = None
            core.save_data(self.data)
            self.refresh_study()

        self.confirm(self.tr("del_title"), self.tr("study_del_ask", t=c["name"]), "delete", "cancel", yes,
                     height=240)

    def study_report_text(self, today):
        rows, sh, ph, pc = core.study_week_report(self.data, today)
        if not rows or ph == 0:
            return self.tr("study_none")
        lines = [self.tr("study_report_line", name=c["name"], sh=core.fmt_hours(s[3]),
                         ph=core.fmt_hours(s[2]), p=s[4], sd=s[1], pd=s[0]) for c, s in rows]
        lines += ["", self.tr("study_report_total", sh=core.fmt_hours(sh), ph=core.fmt_hours(ph), p=pc)]
        return self.num("\n".join(lines))

    def show_study_report(self):
        text = self.study_report_text(date.today())
        self.msg(self.num(self.tr("study_report_title", w=core.current_week(self.data))), text,
                 min(620, 220 + 32 * (text.count("\n") + 1)))

    def show_study_ask(self, pending, today, on_close=None):
        """Daily question: Did you study? One row per course scheduled for today."""
        box = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        box.add_widget(make_label(self.d(self.tr("study_ask")), 18, TEXT, 34, bold=True, halign="center"))
        rows = BoxLayout(orientation="vertical", spacing=dp(6))
        box.add_widget(rows)
        p = self.popup(self.tr("study_ask"), box, 150 + 70 * len(pending) + 56)

        def answer(c, studied, row):
            core.answer_study(self.data, c["id"], today, studied)
            rows.remove_widget(row)
            self.refresh_study()
            if not rows.children:
                p.dismiss()

        for c in pending:
            row = Panel(ROW_A, size_hint_y=None, height=dp(62), spacing=dp(6), padding=dp(6))
            lb = Label(text=self.d(c["name"]), font_name=FONT, font_size=sp(15), color=TEXT,
                       halign="center", valign="middle")
            lb.bind(size=lambda w, v: setattr(w, "text_size", v))
            row.add_widget(lb)
            yes = self.dlg_button("yes", lambda c=c, r=row: answer(c, True, r))
            no = self.dlg_button("no", lambda c=c, r=row: answer(c, False, r), False)
            yes.size_hint_x = no.size_hint_x = 0.28
            row.add_widget(yes)
            row.add_widget(no)
            rows.add_widget(row)
        later = self.dlg_button("rem_later", p.dismiss, False)
        later.size_hint_y = None
        later.height = dp(46)
        box.add_widget(later)
        if on_close:
            p.bind(on_dismiss=lambda *_: on_close())

    # ================= reminders while the app is open =================
    def tick(self):
        today = date.today()
        if self.data.get("last_reminded") != today.isoformat():
            pending = core.pending_reminders(self.data, today)
            if pending:
                self.data["last_reminded"] = today.isoformat()
                core.save_data(self.data)
                self.show_reminder(pending, today)
        wk = str(core.current_week(self.data))
        if today.weekday() == core.WEEK_END_WEEKDAY and self.data.get("last_report_week") != wk:
            self.data["last_report_week"] = wk
            core.save_data(self.data)
            self.show_report()
        self.study_tick(today)
        self.refresh()
        self.refresh_study()

    def study_tick(self, today):
        st = self.data["study"]
        if not st["courses"] or datetime.now().hour < core.STUDY_ASK_HOUR:
            return
        iso = today.isoformat()

        def friday_report():
            wk = str(core.current_week(self.data))
            if today.weekday() == core.WEEK_END_WEEKDAY and st["last_report_week"] != wk:
                st["last_report_week"] = wk
                core.save_data(self.data)
                self.show_study_report()

        if st["last_asked"] != iso:
            st["last_asked"] = iso
            core.save_data(self.data)
            pend = core.pending_study(self.data, today)
            if pend:
                self.show_study_ask(pend, today, friday_report)
                return
        friday_report()

    def show_reminder(self, pending, today):
        box = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        box.add_widget(make_label(self.d(self.tr("rem_head")), 15, TEXT, 30, halign="center"))
        rows = BoxLayout(orientation="vertical", spacing=dp(6))
        box.add_widget(rows)
        p = self.popup(self.tr("rem_title"), box, 120 + 70 * len(pending) + 60)

        def add_row(t):
            key, n, _ = core.status_key(t, today)
            row = Panel(ROW_A, size_hint_y=None, height=dp(62), spacing=dp(6), padding=dp(6))
            lb = Label(text=self.d(f"{t['title']}\n{self.num(self.tr(key, d=n))}"), font_name=FONT,
                       font_size=sp(14), color=TEXT, halign="center", valign="middle")
            lb.bind(size=lambda w, v: setattr(w, "text_size", v))
            row.add_widget(lb)
            b = self.dlg_button("rem_ok", lambda: finish(t, row))
            b.size_hint_x = 0.4
            row.add_widget(b)
            rows.add_widget(row)

        def finish(t, row):
            core.complete_task(self.data, t)
            rows.remove_widget(row)
            self.refresh()
            if not rows.children:
                p.dismiss()

        for t in pending:
            add_row(t)
        btn = self.dlg_button("rem_later", p.dismiss, False)
        btn.size_hint_y = None
        btn.height = dp(46)
        box.add_widget(btn)

    def on_resume(self):
        self.data = core.load_data()
        self.refresh()
        self.refresh_study()
        Clock.schedule_once(lambda dt: self.tick(), 0.5)   # e.g. opened from a notification

    def on_pause(self):
        return True

    # ---------- background service (Android) ----------
    def start_service(self):
        try:
            from android.permissions import request_permissions  # type: ignore
            request_permissions(["android.permission.POST_NOTIFICATIONS"])
        except Exception:
            pass
        try:
            from android import AndroidService  # type: ignore
            self._svc = AndroidService("Homework reminder", "running")
            self._svc.start("start")
        except Exception:
            pass          # not on Android (desktop testing)


if __name__ == "__main__":
    HomeworkApp().run()
