#!/usr/bin/env python
#-*- coding:utf-8 -*-
import random
import sys

from .proxy_getter import ProxyGetter, get_urls, ALL_PROXIES_DICT
from .proxy_validation import ProxyValidation,store_ranked_proxy, USEFUL_PROXY_DICT
from .proxy_getter_config import SOURCE_LIST, TARGET_URLS, VALIDATE_TIME_OUT, VALID_THREAD_NUM, VALID_PROXY_NUM, URL_NUM, FETCH_THREAD_NUM, CONTENT_CHECK

import logging
_logger = logging.getLogger('proxy_util')


def _fetch_mutlithread(sources):
    urls = get_urls(sources)[:URL_NUM]
    workers = []
    for i in xrange(FETCH_THREAD_NUM):
        pg = ProxyGetter(urls[i:len(urls):FETCH_THREAD_NUM], i, sources) 
        pg.setDaemon(True)
        pg.start()
        workers.append(pg)
    for worker in workers:
        worker.join()

        
def _validation_single_target(url, proxies):
    workers = []
    length = len(proxies)
    for i in xrange(VALID_THREAD_NUM):
        vd = ProxyValidation(
            proxies[i:length:VALID_THREAD_NUM],
            url,
            VALIDATE_TIME_OUT,
            i,
            CONTENT_CHECK[url]
        )
        vd.setDaemon(True)
        vd.start()
        workers.append(vd)
    for each in workers:
        each.join()
        

def validate_proxies():
    all_prxies = ALL_PROXIES_DICT.keys()
    for region in TARGET_URLS:
        sets = []
        for url in TARGET_URLS[region]:
            _validation_single_target(url, all_prxies)
            theproxies = []
            for key in sorted(USEFUL_PROXY_DICT[url]):
                theproxies.extend(USEFUL_PROXY_DICT[url][key])
                if VALID_PROXY_NUM and len(theproxies) > VALID_PROXY_NUM:
                    break
            
            sets.append( set(theproxies) )
        proxies = set.intersection( *sets )
        store_ranked_proxy(proxies, region)

#从指定网站上获取最新的代理IP
def get_lastest_proxies():
    for source in SOURCE_LIST:
        _fetch_mutlithread(source)

