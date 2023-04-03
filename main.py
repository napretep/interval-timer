import sys
import time, re

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTimeEdit, \
    QLineEdit, QTreeWidget, QTreeWidgetItem
from PySide6.QtCore import QTimer, Qt
import pyttsx3

intro = """
time must be a string like "1h20m30s" or "20m" or "70s" which h is hours, m is minutes, s is seconds,
The minimum interval for 'interval' is 30 seconds.
"""


def str_time_to_int_time(str_time: str):
    hour, minute, second = 0, 0, 0
    is_legal = re.match(r"^(hms|hm|hs|ms|h|m|s)$", re.sub(r'\d+', "", str_time))
    if not is_legal:
        raise ValueError(intro)
    has_hour = re.search(r'(?P<hour>\d+)[Hh]', str_time)
    has_minute = re.search(r'(?P<minute>\d+)[mM]', str_time)
    has_second = re.search(r'(?P<second>\d+)[sS]', str_time)
    if has_hour:
        hour = int(has_hour.group("hour"))
    if has_minute:
        minute = int(has_minute.group("minute"))
    if has_second:
        second = int(has_second.group("second"))

    return hour, minute, second


def timer(total_time: str, interval_time: str, end_text: str = "", interval_text: str = "",
          need_consume_report: bool = True, need_clock_report=True,
          need_remain_report: bool = True,
          ) -> None:
    """
    :param need_remain_report:
    :param need_clock_report:
    :param total_time: "1h" or "1h20m" or "1h20m30s"
    :param interval_time: "1h" or "1h20m" or "1h20m30s"
    :param interval_text:
    :param end_text:
    :param need_consume_report:
    :rtype: None
    """
    triple_time_maker = lambda _t: _t[0] * 60 * 60 + _t[1] * 60 + _t[2]
    sound: pyttsx3.Engine = pyttsx3.init()

    print("计时开始")
    start_at_timestamp = int(time.time())
    total_timestamp = triple_time_maker(str_time_to_int_time(total_time))
    interval_timestamp = triple_time_maker(str_time_to_int_time(interval_time))
    end_timestamp = start_at_timestamp + total_timestamp
    sound.runAndWait()
    last_second = int(time.time())
    while True:
        now = int(time.time())
        if last_second!=now:
            last_second = now
            print(now)
        if now > end_timestamp:
            break
        elif abs(now-start_at_timestamp) % interval_timestamp ==0:
            print(now-start_at_timestamp)
            now_clock = time.localtime()
            if need_clock_report:
                text = f"现在时间是:{time.strftime('%H点%M分%S秒')}"
                sound.say(text)
                print(text)

            if need_consume_report:
                time_fly = now - start_at_timestamp
                hour = time_fly // 3600
                minute = time_fly % 3600 // 60
                second = time_fly % 3600 % 60
                text = f"距离开始计时已经过去{f'{hour}小时' if hour else ''}{f'{minute}分钟' if minute else ''}{f'{second}秒' if second else ''}了,"
                sound.say(text)
                print(text)

            if need_remain_report:
                time_fly = end_timestamp - now
                hour = time_fly // 3600
                minute = time_fly % 3600 // 60
                second = time_fly % 3600 % 60
                if hour+minute+second>0:
                    text = f"距离结束计时还剩{f'{hour}小时' if hour else ''}{f'{minute}分钟' if minute else ''}{f'{second}秒' if second else ''}"
                    sound.say(text)
                    print(text)

            sound.say(interval_text)
            print(interval_text)
        sound.runAndWait()
    sound.say(end_text)
    print(end_text)
    sound.runAndWait()

if __name__ == '__main__':
    # str_time_to_int_time("45s32h")

    timer("1m", "20s", "计时结束", "黄集攀,你什么时候准备睡觉")
    pass
