# -*- coding: utf-8 -*-
"""
__project_ = 'clocker'
__file_name__ = 'timer.py'
__author__ = '十五'
__email__ = '564298339@qq.com'
__time__ = '2023/4/4 12:51 AM'
"""
from .common_import import *
from .sound import *
from .utils import *

def get_config(indx=0):
    c = json.load(open("./timer_config.json","r",encoding="utf-8"))["info_list"][indx]

    return c

def timer(
        # total_time: str, interval_time: str,
        #   title:str="",
        #   end_text: str = "计时结束",
        #   interval_text: str | list[str] = "",
        #   need_consume_report: bool = True, need_clock_report=True,
        #   need_remain_report: bool = True, need_random_interval_text=False,
        #   sound_source=None,
        idx=0
          ) -> None:
    """

    """
    print(intro)
    config = get_config(idx)


    local_vars = locals()

    # 遍历并打印局部变量（即参数及其值）
    for var_name, value in local_vars.items():
        print(f"{var_name} = {value}")

    sound = Sound(get_config(idx)['sound_source'])

    begin_text = get_config(idx)['title']+"  计时开始"
    start_at_timestamp = int(time.time())


    remain_key_point = []
    consume_key_point = []

    last_second = int(time.time())
    sound.say(begin_text)
    while True:
        now = int(time.time())
        if last_second != now:

            config = get_config(idx)
            total_timestamp = component(get_config(idx)['total_time'].lower(), str_time_to_tuple_time, tuple_time_to_int_time)
            interval_timestamp = component(get_config(idx)['interval_time'].lower(), str_time_to_tuple_time, tuple_time_to_int_time)
            end_timestamp = start_at_timestamp + total_timestamp
            consume_timestamp = now - start_at_timestamp
            remain_timestamp = end_timestamp - now
            last_second = now
            print(f"\r{seconds_to_str(consume_timestamp)}", end='', flush=True)
            remain_key_point = [str_time_to_timestamp(key_point_dict["value"]) for key_point_dict in config['key_point'] if key_point_dict["type"]=="remain"]
            consume_key_point = [str_time_to_timestamp(key_point_dict["value"])for key_point_dict in config['key_point'] if key_point_dict["type"] == "consume"]

            if now > end_timestamp:
                break




            if abs(consume_timestamp) % interval_timestamp == 0:
                print("")

                # print(f"\n{now - start_at_timestamp}")
                now_clock = time.localtime()
                text = config['title']+"\n"


                for report_name in config["text_sequence"]:
                    if report_name == 'interval_text':
                        text += config[report_name] \
                            if type(config['interval_text']) == str else "\n".join(
                                config['interval_text']) if not config['need_random_interval_text'] else random.choice(config["interval_text"])
                        text +="\n"
                    elif report_name == "clock_report":
                        if config['need_clock_report']:
                            text += f"现在是:{time.strftime('%H点%M分%S秒')}.\n"
                    elif report_name =="consume_report":
                        hour, minute, second = seconds_to_HMStriple(now - start_at_timestamp)
                        if hour + minute + second > 0:
                            if config['need_consume_report']:
                                text += f"已经过去{f'{hour}小时' if hour else ''}{f'{minute}分钟' if minute else ''}{f'{second}秒' if second else ''}了,\n"
                        else:
                            text += begin_text + ".\n"
                    elif report_name == "remain_report":
                        hour, minute, second = seconds_to_HMStriple(end_timestamp - now)
                        if hour + minute + second > 0:
                            if config['need_remain_report']:
                                text += f"还剩{f'{hour}小时' if hour else ''}{f'{minute}分钟' if minute else ''}{f'{second}秒' if second else ''}.\n"
                        else:
                            text += config["end_text"] + ".\n"

                sound.say(text)

            if remain_timestamp in remain_key_point:
                key_points = config["key_point"]
                for key_point in key_points:
                    if remain_timestamp == str_time_to_timestamp(key_point["value"]):
                        text = ""
                        for report_name in key_point["text_sequence"]:
                            if report_name == 'clock_report' and key_point["need_clock_report"]:
                                text += f"现在是:{time.strftime('%H点%M分%S秒')}.\n"
                            elif report_name == 'key_point_report' and key_point["need_key_point_report"]:
                                hour, minute, second = seconds_to_HMStriple(remain_timestamp)
                                text += f"还剩{f'{hour}小时' if hour else ''}{f'{minute}分钟' if minute else ''}{f'{second}秒' if second else ''}.\n"
                            elif report_name == 'text':
                                text += key_point["text"] + "\n"
                        sound.say(text)

                pass
            if consume_timestamp in consume_key_point:
                key_points = config["key_point"]
                for key_point in key_points:
                    if consume_timestamp == str_time_to_timestamp(key_point["value"]):
                        text = ""
                        for report_name in key_point["text_sequence"]:
                            if report_name == 'clock_report' and key_point["need_clock_report"]:
                                text += f"现在是:{time.strftime('%H点%M分%S秒')}.\n"
                            elif report_name == 'key_point_report' and key_point["need_key_point_report"]:
                                hour, minute, second = seconds_to_HMStriple(consume_timestamp)
                                text += f"已经过去{f'{hour}小时' if hour else ''}{f'{minute}分钟' if minute else ''}{f'{second}秒' if second else ''}.\n"
                            elif report_name == 'text':
                                text += key_point["text"] + "\n"
                        sound.say(text)
        time.sleep(0.4)
    print(config["end_text"])
