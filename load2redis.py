#/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import time
import logging
import redis
import random

r = redis.StrictRedis(host='localhost', port=6379, db=1)

def get_one_proxy_from_redis(origin):
    p_len = r.llen(origin)
    if p_len < 1:
        print('proxy is null for origin:%s' % (origin))
        return
    i = random.randrange(0, p_len)
    return r.lindex(origin, i).strip()


def get_proxies_from_file(origin):
    filename = 'proxy-' + origin + ".list"
    proxies = []
    try:
        with open(filename) as f:
            for line in f:
                proxies.append(line.strip())
    except IOError as e:
        _logger.warn("load2redis error, file not exists[filename:%s]", filename)
    return proxies

from proxy_utils.proxy_getter_config import TARGET_URLS
def load2redis():
    for origin in TARGET_URLS:
        proxies = get_proxies_from_file(origin)
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
    #定时任务，获取最新可用代理
    from mylogger import loginit
    loginit("log/proxygetter.log", debug=True)
    _logger = logging.getLogger("main")
    load2redis()