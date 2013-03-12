#!/usr/bin/python
# coding:utf-8
#
#   本文件用于验证代理是否可用
#
import urllib2
import httplib
import time
from math import ceil
import threading
from httplib import BadStatusLine
import socket
import json
import requests
import lxml
import os

import logging
_logger = logging.getLogger('proxy_util.proxy_validation')


USEFUL_PROXY_DICT = {}

def store_ranked_proxy(proxies_dict, url):
    store_proxies = []
    max_time = 0
        
    for key in sorted(proxies_dict):
        if key > max_time:
            max_time = key
        proxies = proxies_dict[key]
        store_proxies.extend(proxies)
        
    _logger.info("get and validated proxy[size:%d][max_use_time:%s]", len(store_proxies), str(max_time))
    
    with open("proxy.list", "w") as f:
        for p in store_proxies:
            f.write("%s\n" %p)

class ProxyValidation(threading.Thread):
    '''
    本类用于验证代理是否可用
    '''
    def __init__(self, px_lst, url, time_out, tid, keyword):
        threading.Thread.__init__(self)
        self.px_lst = px_lst
        self.url = url
        self.timeout = time_out
        self.tid = tid
        self.keyword = keyword

    def validate(self, url, proxy, t_out, keyword):
        try:
            
            begin = time.time()
            #用代理打开链接
            headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
                       'Accept-Language' : 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
                       }
            proxies = { "http": proxy }
            r = requests.get(url, timeout=t_out, proxies=proxies, headers=headers, cookies=dict())
            #_logger.debug("requests [url:%s][proxy:%s]", url, str(headers) )
            the_page = r.text
            
            '''
            httplib.HTTPConnection.debuglevel = 1
            opener = urllib2.build_opener(
                                          urllib2.ProxyHandler({'http': proxy}))
            opener.addheaders = [('User-agent', 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)'), 
                                 ('Accept-Language', 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4')]
            begin = time.time()
            res = opener.open(urllib2.Request(url), timeout=t_out)
            the_page = res.read()
            
            msg = res.info()
            if msg is not None:
                the_charset = msg.getparam('charset')
                _logger.debug("charset is :" + the_charset)
                the_page = the_page.decode(the_charset).encode("utf8")
                
            '''
            
            if keyword in the_page:
                end = time.time()
                _logger.debug("Validate Pass:[proxy:%s][url:%s]", proxy , url)
                return { int(ceil(end - begin)): proxy}
            else :
                _logger.debug("Validate Fail:[proxy:%s][url:%s][page_content:%s]", proxy ,url, the_page)
        except urllib2.HTTPError,e:
            _logger.exception("validate HTTPError[errmsg:%s][url:%s][proxy:%s]", str(e), url, proxy)
            return 
        except urllib2.URLError,e:
            _logger.exception("validate URLError[errmsg:%s][url:%s][proxy:%s]", str(e), url, proxy)
            return 
        except requests.ConnectionError,e:
            _logger.exception("validate ConnectionError[errmsg:%s][url:%s][proxy:%s]", str(e), url, proxy)
            return 
        except requests.HTTPError ,e:
            _logger.exception("validate HTTPError[errmsg:%s][url:%s][proxy:%s]", str(e), url, proxy)
            return 
        except requests.Timeout ,e:
            _logger.exception("validate requests.Timeout[errmsg:%s][url:%s][proxy:%s]", str(e), url, proxy)
            return 
        except socket.timeout ,e:
            _logger.exception("validate socket.timeout[errmsg:%s][url:%s][proxy:%s]", str(e), url, proxy)
            return 
        except requests.TooManyRedirects ,e:
            _logger.exception("validate TooManyRedirects[errmsg:%s][url:%s][proxy:%s]", str(e), url, proxy)
            return 
        except lxml.etree.XMLSyntaxError,e:
            _logger.exception("validate XMLSyntaxError[errmsg:%s][url:%s][proxy:%s]", str(e), url, proxy)
            return 
        except httplib.IncompleteRead:
            _logger.exception("validate httplib.IncompleteRead exception[url:%s][proxy:%s]", url, proxy)
            return 
        except Exception,e:
            _logger.exception("validate[errmsg:unknown exception][msg:%s][url:%s]", str(e), url)
            return 
        
        return

    def run(self):
        available_proxies = []
        for cur_prxy in self.px_lst:
            vp = self.validate(self.url, cur_prxy, self.timeout, self.keyword)
            if vp:
                available_proxies.append(vp)
            else:
                continue 
        for proxy in available_proxies:
            for timestamp, ip in proxy.items():
                if ip not in USEFUL_PROXY_DICT.get(timestamp, []):
                    USEFUL_PROXY_DICT.setdefault(
                        timestamp,
                        []
                    ).append(ip)
                else:
                    continue
