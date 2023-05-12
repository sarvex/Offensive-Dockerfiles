#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

import urllib.request
from http.cookiejar import CookieJar

def getrawsource(url, ua):
    if url == "": # Empty freakin shit
        return ['0','Empty URL Provided','', '']
    try:
        ckreq = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': ua,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            #'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        )
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        with opener.open(ckreq, timeout=8) as response:
            scode = response.read().decode("utf-8", 'ignore')
            headers = str(response.info())
            rurl = response.geturl()
            return ['1', scode, headers, rurl]
    except Exception as e:
        ef = str(e)
        try:
            ecode = str(e.code)
            ehed = str(e.info())
            return ['2', ef, ecode, ehed]
        except Exception as f:
            return ['2', ef, '', '']
