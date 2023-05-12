#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

# AEF version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(source):
    regex = re.findall(r'Powered By AEF (\d.*?)</a>', source)
    if regex != [] and regex[0] not in ['', ' ']:
        version = regex[0]
        cmseek.success(
            f'AEF version {cmseek.bold}{cmseek.fgreen}{version}{cmseek.cln} detected'
        )
        return version

    cmseek.error('Version detection failed!')
    return '0'
