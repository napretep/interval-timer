# -*- coding: utf-8 -*-
"""
__project_ = 'pomo-timer'
__file_name__ = 'sound.py'
__author__ = '十五'
__email__ = '564298339@qq.com'
__time__ = '2023/4/3 14:16'
"""

import json, os, pyttsx3

import azure.cognitiveservices.speech as azure_speechsdk

# 从 Azure 门户获取的订阅密钥和终结点
azure_endpoint = "https://eastasia.api.cognitive.microsoft.com/sts/v1.0/issuetoken"


class SoundSource:
    local = 0
    azure = 1


class Sound:
    config = "./lib/sound_config.json"

    def __init__(self, source=None):
        self.sound_source = source if source else self.get_source()
        self.engine: pyttsx3.DriverProxy | azure_speechsdk.SpeechSynthesizer = self.get_engine()

    def say(self, sentence):
        print(sentence)
        if self.sound_source == SoundSource.local:
            self.engine.say(sentence)
            self.engine.runAndWait()
        elif self.sound_source == SoundSource.azure:
            self.engine.speak_text(sentence)


    def get_engine(self):
        try:
            if self.sound_source == SoundSource.local:
                return pyttsx3.init()
            elif self.sound_source == SoundSource.azure:
                config = json.load(open(self.config,"r", encoding="utf-8"))
                key = config["azure_api"]["subscription_key"]
                speech_config = azure_speechsdk.SpeechConfig(subscription=key, endpoint=azure_endpoint)
                speech_config.speech_synthesis_language = "zh-CN"
                speech_config.speech_synthesis_voice_name = "zh-CN-XiaochenNeural"
                speech_synthesizer = azure_speechsdk.SpeechSynthesizer(speech_config=speech_config)
                return speech_synthesizer
        except IOError:
            print(f"找不到配置文件路径={self.config},选用本地音源")
            self.sound_source = SoundSource.local
            return pyttsx3.init()

    def get_source(self):
        try:
            config = json.load(open(self.config,"r", encoding="utf-8"))
            if "azure_api" in config:
                print("选用azure的音源")
                return SoundSource.azure
            else:
                return SoundSource.local
        except IOError:
            print(f"找不到配置文件路径={self.config},选用本地音源")
            return SoundSource.local
