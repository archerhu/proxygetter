#!/usr/bin/python
# coding: utf-8
#
#   此文件是此代理程序的配置文件，用于设置获取代理所访问的
#   url地址，测试代理是否可用所访问的地址，验证代理开辟线程
#   的个数，超时时间等参数
#
from proxy_getter import get_dynamic_urls
#用于获取静态页面中代理的url及匹配模式
STATIC_PROXY_SOURCES = [
    { 
        'blog.sina.com.cn': [
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+",
            r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<port>\d+)",
        ],
        'urls': [
            'http://blog.sina.com.cn/s/blog_5519064d0100y8nz.html'
        ]
    },
    { 
        'proxy.ipcn.org': [
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+",
            r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<port>\d+)",
        ],
        'urls': [
            'http://proxy.ipcn.org/proxylist.html'
        ]
    },
    {
        'www.sooip.cn': [
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+",
            r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<port>\d+)",
        ],
        'urls': [
            'http://www.sooip.cn/zuixindaili/2012-05-15/2807.html'
        ]
    },
]
COUNTRIES = [
    'ar', 'br', 'ca', 'cl', 'co', 'ec', 'mx', 'pe', 'us', 've', 'bg', 'cz',
    'fr', 'de', 'hu', 'it', 'kz', 'lv', 'tr', 'pl', 'ro', 'ru', 'es', 'se',
    'mo', 'nl', 'no', 'ua', 'gb', 'au', 'bd', 'cn', 'hk', 'id', 'in', 'my',
    'ph', 'kr', 'sg', 'tw', 'th', 'vn',
]
PAGES = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
COUNTRY_PAGES = [(x, y) for x in COUNTRIES for y in PAGES]

'''
    {
        'www.proxynova.com': [
             r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s+\r\n\s+\d+",
             r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+\r\n\s+(?P<port>\d+)",
        ],
        'urls': [
                'http://www.proxynova.com/proxy-server-list/country-%s/?p=%d' % 
                (country, page) for (country, page) in COUNTRY_PAGES
        ]
    },
    
'''
DYNAMIC_PROXY_SOURCES = [
    {
        'www.proxycn.cn': [
             r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+",
             r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<port>\d+)",
        ],
        'urls': [
                 'http://www.proxycn.cn/html_proxy/country%s-1.html' %
                country.upper() for country in COUNTRIES
        ]
    },
    {
        'www.freeproxy.ch': [
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+",
            r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(?P<port>\d+)",

        ],
        'urls': [
            'http://www.freeproxy.ch/country-CN.htm'
        ]
    },
    {
        'www.xroxy.com': [
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\n\n\n\t\d+",
            r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\n\n\n\t(?P<port>\d+)"
        ],
        'urls': [
            'http://www.xroxy.com/proxylist.php?port=&type=\
All_http&ssl=&country=CN&latency=&reliability=&\
sort=reliability&desc=true&pnum=%d#table' %
            page for page in xrange(23)
        ]
    },
    {
        'proxy.berry0123.cn': [
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\s\r\n\s{4}\d+",
            r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s\r\n\s{4}(?P<port>\d+)"
        ],
        'urls': [
            'http://proxy.berry0123.cn/index.php'
        ]
    },
    {
        'www.sooip.cn': [
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3} \d+",
            r"(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) (?P<port>\d+)",
        ],
        'urls': get_dynamic_urls('http://www.sooip.cn/guoneidaili/')
    }
]

SOURCE_LIST = [DYNAMIC_PROXY_SOURCES, STATIC_PROXY_SOURCES]



#验证代理是否有效所访问的URL
TARGET_URLS = {
#    'http://itunes.apple.com/cn/genre/ios/id36?mt=8',
'foreign' : [
             'http://www.amazon.com',
             'http://www.google.com/intl/en/about/'
             ],
               
'domestic' : [
              'http://www.baidu.com',
              'http://www.sina.com.cn'
              ]
}

CONTENT_CHECK = {
#    'http://itunes.apple.com/cn/genre/ios/id36?mt=8' : 'get iTunes now',
    'http://www.amazon.com' : '1996-2013, Amazon.com, Inc. or its affiliates',
    'http://www.google.com/intl/en/about/' : 'About Google',
    'http://www.bing.com' : '2013 Microsoft',
    'http://www.baidu.com' : '030173',
    'http://www.sina.com.cn' : '110000000016',
}

#超时时间
VALIDATE_TIME_OUT = 30

#获取代理的线程个数
FETCH_THREAD_NUM = 10 

#验证代理是否有效的线程个数
VALID_THREAD_NUM = 100

#每次验证代理的个数,None表示全部代理个数
VALID_PROXY_NUM = None

#每次获取代理时的URL个数，None表示全部URL
URL_NUM = None
