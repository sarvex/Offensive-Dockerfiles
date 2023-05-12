#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

import cmseekdb.basic as cmseek

def start(url,ua):
    reg_url = f'{url}/index.php?option=com_users&view=registration'
    reg_source = cmseek.getsource(reg_url, ua)
    if reg_source[0] != '1':
        return ['0', '']
    if (
        'registration.register' not in reg_source[1]
        and 'jform_password2' not in reg_source[1]
        and 'jform_email2' not in reg_source[1]
    ):
        return ['0', '']
    cmseek.success(f'User registration open, {cmseek.bold}{reg_url}{cmseek.cln}')
    return ['1', reg_url]
