import re

intro = """
time must be a string like "1h20m30s" or "20m" or "70s" which h is hours, m is minutes, s is seconds,
The minimum interval for 'interval' is 30 seconds.
"""

def component(args,*funcs):
    result = funcs[0](args)
    for func in funcs[1:]:
        result = func(result)
    return result


def str_time_to_tuple_time(str_time: str):
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


def tuple_time_to_int_time(_t):
    return _t[0] * 60 * 60 + _t[1] * 60 + _t[2]

def str_time_to_timestamp(str_time: str):
    return component(str_time, str_time_to_tuple_time,tuple_time_to_int_time)

def seconds_to_HMStriple(seconds: int):
    hour = seconds // 3600
    minute = seconds % 3600 // 60
    second = seconds % 3600 % 60
    return hour, minute, second


def HMStriple_to_str(triple):
    return f"{triple[0]}小时{triple[1]}分钟{triple[2]}秒钟"


def seconds_to_str(seconds):
    return component(seconds, seconds_to_HMStriple, HMStriple_to_str)


