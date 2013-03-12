#/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import time
import logging
import redis

#定时任务，获取最新可用代理
from mylogger import loginit
loginit("log/proxygetter.log", debug=True)
_logger = logging.getLogger("main")

def get_proxies(origin):
    filename = 'proxy-' + origin + ".list"
    proxies = []
    try:
        with open(filename) as f:
            for line in f:
                proxies.append(line)
    except IOError as e:
        _logger.warn("load2redis error, file not exists[filename:%s]", filename)
    return proxies

def load2redis():
    r = redis.StrictRedis(host='localhost', port=6379, db=1)
    for origin in ['foreign', 'domestic']:
        proxies = get_proxies(origin)
        pip = r.pipeline()
        tmp_key = '__' + origin
        pip.delete(tmp_key)
        #_logger.debug('get proxy num:%d' % (len(proxies)))
        for p in proxies:
            pip.rpush(tmp_key, p)
        pip.rename(tmp_key, origin)
        #_logger.debug("load proxy size: " + str(len(proxies)) + "url:" + url)
        pip.execute()
        
if __name__ =='__main__':
    load2redis()