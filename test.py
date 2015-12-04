# -*- coding: utf-8 -*-
import os
import time
import json

import requests

from ini_conf import MyIni
import bs


class AlarmClient(object):

    def __init__(self):
        self.myini = MyIni()
        self.kakou_ini = {'host': '10.47.187.165', 'port': 80}
        #ID标记
        self.id_flag = 0
        #self.step = self.hbc_conf['step']
        self.kkbh = 'hdk01'
        self.fxbh = u'进城'        

        self.kakou_status = False


    def get_cltxs(self, _id, last_id):
        """根据id范围获取过车信息"""
        url = 'http://%s:%s/rest_kakou/index.php/v1/cltx/cltxs/%s/%s' % (
            self.kakou_ini['host'], self.kakou_ini['port'], _id, last_id)
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

    def get_cltxmaxid(self):
        """获取cltx最大ID值"""
        url = 'http://%s:%s/rest_kakou/index.php/v1/cltx/cltxmaxid' % (
            self.kakou_ini['host'], self.kakou_ini['port'])
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

    def show_info(self, _id):
        print 'alarm'

    def start_alarm(self):
        pass

    def get_alarm_info(self):
        maxid = self.get_cltxmaxid()['maxid']
        if maxid <= self.id_flag:
            # 没有新的数据 返回1
            time.sleep(0.1)
            return 1
        cltxs = self.get_cltxs(self.id_flag, maxid)
        self.id_flag = maxid
        if cltxs['total_count'] > 0:
            for i in cltxs['items']:
                if i['clbj'] == 'B' or i['clbj'] == 'L':
                    if i['kkbh'] == self.kkbh and i['fxbh'] == self.fxbh:
                        self.set_alarm(i['id'])
        else:
            time.sleep(0.1)

    def main_loop(self):
        # 加载初始化数据
        init_flag = True
        while 1:
            if not init_flag:
                try:
                    pass
                except Exception as e:
                    logger.error(e)
                    time.sleep(1)
            elif self.kakou_status:
                try:
                    self.get_alarm_info()
                except Exception as e:
                    logger.error(e)
                    time.sleep(1)
            else:
                try:
                    if not self.kakou_status:
                        self.get_cltxmaxid()
                        self.kakou_status = True
                except Exception as e:
                    #print (e)
                    time.sleep(1)
        #del hbc


if __name__ == "__main__":
    ac = AlarmClient()
##    hbc = HbcCompare()
##    #hbc.main_loop()
##    url = 'http://localhost/kakou/images/test2.jpg'
##    path = 'imgs'
##    name = 'test2'
##    text = u'Linsir.vi5i0n@hotmail.com'
##    hbc.get_img_by_url(url, path, name, text)
##    del hbc
