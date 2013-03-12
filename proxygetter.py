#/usr/bin/env python
#-*- coding:utf-8 -*-
from __future__ import absolute_import
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import time
import logging

#定时任务，获取最新可用代理
from mylogger import loginit
loginit("log/proxygetter.log", debug=True)
_logger = logging.getLogger("main")
import proxy_utils

def ProxyValidation():
    begin_time = time.time()
    try:
        proxy_utils.get_lastest_proxies()
        proxy_utils.validate_proxies()
        _logger.info("ProxyValidation Finished[use_time:%f] " % (time.time() - begin_time))
    except Exception, e:
        _logger.exception("ProxyValidation Exception [exception:%s][use_time:%f]" % (str(e), time.time() - begin_time))
        
if __name__ =='__main__':
    ProxyValidation()