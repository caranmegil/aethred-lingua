#    start.py - driver program
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

from flask import Flask, request, jsonify
import lingua
import json
import time

aethred = lingua.Brain('./aethred.xml')
aethred.is_running = True
aethred.start()

print('Parsing the brain!')
while not aethred.get_brain():
    time.sleep(5)
print('The brain is parsed.  Starting up the routes.')

app = Flask(__name__)

@app.route('/', methods=['POST'])
def getResponse():
    obj = json.loads(request.get_data().decode())
    if obj and obj['text']:
        resp = aethred.get_brain().get_response(text=obj['text'])
        ret_obj = {}

        if type(resp) is list:
            ret_obj['response'] = resp
        else:
            ret_obj['response'] = [resp]
        return jsonify(ret_obj)
    else:
        return jsonify({'error': 0})
