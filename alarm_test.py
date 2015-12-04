# -*- coding: utf-8 -*-
import time
import json
import threading
import winsound

import requests
import pyttsx
import serial
from selenium import webdriver

class AlarmSys(object):
    def __init__(self):
        self.BrowserObj_dirver = webdriver.Firefox()
        self.BrowserObj_dirver.get('http://10.44.249.227')
        # 文件转声音
        self.engine = pyttsx.init()
        # 跟踪ID
        self.flag_id = 0
        self.kakou_status = False
        self.kkdd_id = '441323013'
        self.fxbh = ''

    def __del__(self):
        pass

    def power_on(self):
        ser = serial.Serial(0)
        o_str_hex = '\xfe\x05\x00\x03\xff\x00\x68\x35'
        c_str_hex = '\xfe\x05\x00\x03\x00\x00\x29\xc5'
        ser.write(o_str_hex)
        time.sleep(8)
        ser.write(c_str_hex)
        ser.close()

    def text2speech(self, text):
        """文字转声音"""
        self.engine = pyttsx.init()
        self.engine.setProperty('rate', 100)
        self.engine.say(text)
        self.engine.runAndWait()

    def alarm_sound(self, wav= u'sounds/BUZZ4.wav', rounds=4):
        """报警声"""
        for i in range(rounds)
            winsound.PlaySound(wav, winsound.SND_NODEFAULT)

    def start_alarm(self, hphm):
        text = u'请拦截, %s' % hphm
        self.text2speech(text)
        self.alarm_sound()
    
    
    def get_maxid(self):
        url = 'http://10.44.249.227:8060/rest_kakou/index.php/v1/cltx/cltxmaxid'
        headers = {'content-type': 'application/json'}
        try:
            r = requests.get(url, headers)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.kakou_status = False
            raise

    def get_cltxs(self, id_, last_id):
        #last_id = self.id_flag + self.step
        url = 'http://10.44.249.227:8060/rest_kakou/index.php/v1/cltx//cltxs/%s/%s' % (
            id_, last_id)
        try:
            r = requests.get(url)
            if r.status_code == 200:
                return json.loads(r.text)
            else:
                self.kakou_status = False
                raise Exception('url: %s, status: %s, %s' % (
                    url, r.status_code, r.text))
        except Exception as e:
            self.kakou_status = False
            raise

    def view_info(self, id_):
        self.BrowserObj_dirver.get('http://10.44.249.227:83/index.php/cpbk/test?id=%s' % id_)

    def fetch_data(self):
        """获取卡口车辆信息"""
        step = 20
        maxid = self.get_maxid()['maxid']
        #print 'maxid: %s' % maxid
        if maxid <= self.flag_id:
            # 没有新的数据 返回
            time.sleep(0.25)
            return
        # 获取车辆信息
        carinfo = self.get_cltxs(self.flag_id, maxid)
        self.flag_id = maxid
        if carinfo['total_count'] == 0:
            return

        # 遍历列表并比对是否报警
        for i in carinfo['items']:
            if i['kkdd_id'] == self.kkdd_id:
                t = threading.Thread(target=self.view_info, args=(i['id'],))
                t.start()
                t.join()
                if i['clbj'] == 'B' or i['clbj'] == 'L':
                    t2 = threading.Thread(target=self.power_on)
                    t3 = threading.Thread(target=self.start_alarm)
                    t2.start()
                    t3.start()
                    t2.join()
                    t3.join()
                    time.sleep(180)
        
    def main_loop(self):
        # 加载初始化数据
        init_flag = False
        while 1:
            #print 'loop'
            if not init_flag:
                try:
                    # 获取黄标车数据
                    self.flag_id = self.get_maxid()['maxid']
                    self.kakou_status = True

                    init_flag = True
                    print 'Init Finish'
                except Exception as e:
                    logger.error(e)
                    time.sleep(1)
            elif self.kakou_status:
                try:
                    self.fetch_data()
                except Exception as e:
                    logger.error(e)
                    time.sleep(1)
            else:
                try:
                    if not self.kakou_status:
                        self.flag_id = self.get_maxid()['maxid']
                        self.kakou_status = True
                except Exception as e:
                    print (e)
                    time.sleep(1)


if __name__ == "__main__":
    alarm = AlarmSys()
    alarm.main_loop()
    #print alarm.get_cltxs(214765208, 214765211)
    del alarm
