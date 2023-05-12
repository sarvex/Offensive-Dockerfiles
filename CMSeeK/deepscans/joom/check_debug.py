#!/usr/bin/python3
# -*- coding: utf-8 -*-
# This is a part of CMSeeK, check the LICENSE file for more information
# Copyright (c) 2018 Tuhinshubhra

import cmseekdb.basic as cmseek
# I know there is no reason at all to create a separate module for this.. there's something that's going to be added here so.. trust me!
def start(source):
    if (
        'Joomla! Debug Console' not in source
        and 'xdebug.org/docs/all_settings' not in source
    ):
        return '0'
    cmseek.success('Debug mode on!')
    return '1'
