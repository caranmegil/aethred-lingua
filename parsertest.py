#    parsertest.py - tester of the parser
#    Copyright (C) 2020  William R. Moore <caranmegil@gmail.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program.  If not, see <https://www.gnu.org/licenses/>.
import lingua, time

aethred = lingua.Brain('aethred.xml')
aethred.is_running = True
aethred.start()

while not aethred.get_brain():
    time.sleep(5)

print(aethred.get_brain().get_response('blah'))

aethred.stop_running()
