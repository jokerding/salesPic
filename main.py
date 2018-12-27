#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : main.py
# @Author: joker
# @Date  : 2018/12/25
# @Desc  :

from src.ui.UI_Mian import *

import sys

if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    plugin_path = os.path.join(dirname, 'plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

    app = QApplication(sys.argv)

    mainWindows = UI_Mian()

    mainWindows.show()

    sys.exit(app.exec_())