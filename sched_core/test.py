#########################################################################
#
#   Astronomy Club Event Generator
#   file: sched_core/test.py
#
#   Copyright (C) 2017  Teruo Utsumi, San Jose Astronomical Association
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   Contributors:
#       2016-05-25  Teruo Utsumi, initial code
#
#########################################################################

import pdb
from   enum                       import Enum, unique


EMAIL_ON = False
EMAIL_ON = True

#testmodes = set()

TEST = 0


@unique
class TestModes(Enum):
    # index 1 is default
    Fake_Save        =  'Fake save'
    Email_To_Console =  'Email to console'
    Email_To_Tester  =  'Email to tester'
