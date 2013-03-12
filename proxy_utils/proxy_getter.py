#!/usr/bin/python
# coding:utf-8
#
#   This file used to get a proxy list.
#
import urllib2
import re
from time import sleep
from threading import Thread
import requests
from lxml import html
import lxml
import socket

import logging
_logger = logging.getLogger('proxy_util.proxy_getter')

'''
engine = create_engine('sqlite:///C:\\proxy-database.db')
metadata = MetaData()
metadata.bind = engine
'''

ALL_PROXIES_DICT = dict()

def get_urls(proxy_sources):
    urls = []
    for source in proxy_sources:
        urls.extend(source['urls'])
    return urls

def get_patterns(url, proxy_sources):
    for source in proxy_sources:
        if source.get(re.split('/', url)[2]):
            return source[re.split('/', url)[2]]

def get_source(url):
    for i in xrange(3):
        try:
            r = requests.get(url, timeout=30)
            if r.status_code ==200:
                return r.text
        except requests.exceptions.RequestException:
            sleep(2)
            continue
    return
           
def get_dynamic_urls(url):
    urls = []
    url_parts = url.split('/')
    host = ("%s//%s") % (url_parts[0], url_parts[2])
    src = get_source(url)
    if src:
        tree = html.fromstring(src)
        for link in tree.xpath(".//table[@class='box']//li//a"):
            urls.append(("%s%s") % (host, link.get('href')))
        return urls
    else:
        return []

class ProxyGetter(Thread):
    '''
    本类用于获取代理
    '''
    def __init__(self, urls, tid, proxy_sources):
        Thread.__init__(self)
        self.urls = urls
        self.tid = tid
        self.proxy_sources = proxy_sources

    def get_release_site_proxy(self, url, patterns):
        try:
            search_pattern, group_pattern = patterns
            src = get_source(url)
            if src: 
                doc = html.document_fromstring(src)
                for match_text in re.findall(
                    search_pattern,
                    ''.join(doc.xpath("/*//text()"))
                ):
                    match = re.match(group_pattern, match_text)
                    _logger.debug("find one:%s", match.group('ip')+ ":" + match.group('port'))
                    '''
                    db.proxy.update(
                        {'dt': str(date.today())},
                        {'$addToSet':
                            {
                                'px':{
                                    'ad': match.group('ip'),
                                    'pt': match.group('port'),
                                    'tp': 'http',
                                }
                            }
                        },
                        upsert=True,
                    )
                    '''
                    ALL_PROXIES_DICT[match.group('ip')+":"+match.group('port')] = True
            else:
                _logger.warn("get_release_site_proxy[errmsg:htmlcontent is empty][url:%s]" %(url))
        except urllib2.HTTPError,e:
            _logger.exception("get_release_site_proxy HTTPError[reason:%s][url:%s]", e.reason, url)
        except urllib2.URLError,e:
            _logger.exception("get_release_site_proxy URLError[reason:%s][url:%s]", e.reason, url)
        except requests.ConnectionError,e:
            _logger.exception("get_release_site_proxy ConnectionError[errmsg:%s][url:%s]", str(e), url)
        except requests.HTTPError ,e:
            _logger.exception("get_release_site_proxy HTTPError[errmsg:%s][url:%s]", str(e), url)
        except requests.Timeout ,e:
            _logger.exception("get_release_site_proxy requests.Timeout[errmsg:%s][url:%s]", str(e), url)
        except socket.timeout, e:
            _logger.exception("get_release_site_proxy socket.timeout[errmsg:%s][url:%s]", str(e), url)
        except requests.TooManyRedirects ,e:
            _logger.exception("get_release_site_proxy TooManyRedirects[errmsg:%s][url:%s]", str(e), url)
        except lxml.etree.XMLSyntaxError,e:
            _logger.exception("get_release_site_proxy XMLSyntaxError[errmsg:%s][url:%s]", str(e), url)
        except Exception,e:
            _logger.exception("get_release_site_proxy[errmsg:unknown exception, discard this website][msg:%s][url:%s]", str(e), url)

    def run(self):
        for cur_url in self.urls: 
            #_logger.debug( 'TID:%d, URL:%s' % (self.tid, cur_url))
            self.get_release_site_proxy(
                cur_url,
                get_patterns(cur_url, self.proxy_sources)
            )
