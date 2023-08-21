"""
TODO interval_text 改成 begin_interval_text 和 end_interval_text 两部分
TODO 加UI
TODO 改成从json文件读取全部信息,因为有时候可能会想要更新
TODO 改成树形结构
"""
from lib.sound import Sound
from lib.timer import timer, get_config

if __name__ == '__main__':
    # sound = Sound(get_config()['sound_source'])
    # sound.say("你好,我是你的语音提醒助手,以后由我来提醒你好好工作,抓紧时间,保证效率,申请到心仪的博士项目")
    timer(1)
    pass
