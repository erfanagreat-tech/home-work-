[app]
title = Homework Reminder
package.name = homeworkreminder
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,ttf,json
version = 1.2
requirements = python3,kivy==2.3.0,plyer,pyjnius,android
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/icon.png

# background service that posts the daily notification in the phone's top bar
services = Reminder:service.py:foreground

android.permissions = POST_NOTIFICATIONS,FOREGROUND_SERVICE,RECEIVE_BOOT_COMPLETED,WAKE_LOCK
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
android.ndk = 25b

# pin python-for-android to a stable release (the newest one pulls Python 3.14, which Kivy 2.3.0 cannot build)
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1
