#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

# UBB.threads version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(source, ga_content):
    regex = re.findall(r'UBB.threads (\d.*)', ga_content)
    if regex != [] and regex[0] not in ['', ' ']:
        version = regex[0].replace(' ', '')
        cmseek.success(
            f'UBB.threads version {cmseek.bold}{cmseek.fgreen}{version}{cmseek.cln} detected'
        )
        return version

    regex2 = re.search(r'Powered by UBB.threads(.*?)Forum Software (\d.*?)</a>', source)
    if regex2 != None:
        try:
            version = regex2[2]
            cmseek.success(
                f'UBB.threads version {cmseek.bold}{cmseek.fgreen}{version}{cmseek.cln} detected'
            )
            return version
        except Exception as e:
            cmseek.error('Version detection failed!')
            return '0'

    cmseek.error('Version detection failed!')
    return '0'
