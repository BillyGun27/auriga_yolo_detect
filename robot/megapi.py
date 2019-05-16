# -*- coding: utf-8 -*
#sudo rfcomm bind 0 00:1B:10:31:39:E7
import sys

if sys.version > '3':
    PY3 = True
    print("\r\nVersion:" + sys.version)
    from robot.megapi_python3 import *
else:
    PY3 = False
    print("\r\nVersion:" + sys.version)
    from robot.megapi_python2 import *