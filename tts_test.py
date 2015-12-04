# -*- coding: utf-8 -*-
import pyttsx
engine = pyttsx.init()
engine.setProperty('rate', 100)
engine.say(u'请拦截，死肥仔')
#engine.say('The quick brown fox jumped over the lazy dog.')
engine.runAndWait()
