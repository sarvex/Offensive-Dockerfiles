#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

# YaBB version detection
# Rev 1

import cmseekdb.basic as cmseek
import re

def start(source):
    regex = re.search(r'Powered by(.*?)YaBB (\d.*?)( |</a>)', source, re.DOTALL)
    if regex is None:
        regex = re.findall(r'<!-- YaBB (\d.*?) ', source)
        if regex != [] and regex[0] not in ['', ' ']:
            version = regex[0]
            cmseek.success(
                f'YaBB version {cmseek.bold}{cmseek.fgreen}{version}{cmseek.cln} detected'
            )
            return version

    else:
        try:
            version = regex[2]
            cmseek.success(
                f'YaBB version {cmseek.bold}{cmseek.fgreen}{version}{cmseek.cln} detected'
            )
            return version
        except Exception as e:
            regex = re.findall(r'<!-- YaBB (\d.*?) ', source)
            if regex != [] and regex[0] not in ['', ' ']:
                version = regex[0]
                cmseek.success(
                    f'YaBB version {cmseek.bold}{cmseek.fgreen}{version}{cmseek.cln} detected'
                )
                return version
    cmseek.error('Version detection failed!')
    return '0'
