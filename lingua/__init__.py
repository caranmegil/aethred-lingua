#    lingua/__init__.py - actual parser and classes associated with it
#    Copyright (C) 2020  William R. Moore <caranmegil@gmail.com>
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import re, random, threading, time
import xml.etree.ElementTree
import os
import requests

def parse_response(rtype):
    mtype = rtype.findall('multiline')
    if mtype:
        lines = []
        for ltype in mtype[0].findall('line'):
            lines.append(ltype.text)
        return Response(response=Multiline(lines=lines))
    else:
        splorks = rtype.findall('splork')
        if splorks:
            return Response(response=Splork())
        else:
            return Response(response=rtype.text)

def parse(file_name):
    e = xml.etree.ElementTree.parse(file_name).getroot()
    patterns = []
    default = None

    for dtype in e.findall('default'):
        responses = []

        for rtype in dtype.findall('response'):
            responses.append(parse_response(rtype))

        default = Default(responses=responses)

    for ptype in e.findall('pattern'):
        responses = []
        regex = ptype.get('regex')

        for rtype in ptype.findall('response'):
            responses.append(parse_response(rtype))

        patterns.append(Pattern(regex=regex, responses=responses))
    return Lingua(default=default, patterns=patterns)

class Brain(threading.Thread):
    def __init__(self, file_name):
        threading.Thread.__init__(self)
        self.brain = None
        self.file_name = file_name
        self.last_parsed_time = None
        self.is_running = False
        self.brain_lock = threading.Lock()

    def get_brain(self):
        self.brain_lock.acquire()
        brain = self.brain
        self.brain_lock.release()

        return brain

    def stop_running(self):
        self.is_running = False
        self.join()

    def run(self):
        while self.is_running:
            file_time = os.path.getmtime(self.file_name)

            if not self.last_parsed_time or self.last_parsed_time < file_time:
                print('parsing')
                self.brain_lock.acquire()
                self.brain = parse(self.file_name)
                self.last_parsed_time = file_time
                self.brain_lock.release()
                print('done parsing')

            time.sleep(10)

class Lingua:
    def __init__(self, default, patterns):
        self.default = default
        self.patterns = patterns

    def get_response(self, text):
        for pattern in self.patterns:
            m = pattern.regex.match(text)
            if m:
                return pattern.get_response()
        return self.default.get_response()

class LinguaTag:
    def get_response(self):
        return None

class Default(LinguaTag):
    def __init__(self, responses):
        self.responses = responses

    def get_response(self):
        response = random.choice(self.responses)
        return response.get_response()

class Response(LinguaTag):
    def __init__(self, response):
        self.response = response

    def get_response(self):
        if type(self.response) is Multiline:
            return self.response.get_response()
        elif type(self.response) is Splork:
            return self.response.get_response()
        return self.response

class Pattern(LinguaTag):
    def __init__(self, regex, responses):
        self.regex = re.compile(regex)
        self.responses = responses

    def get_response(self):
        response = random.choice(self.responses)
        return response.get_response()

class Multiline(LinguaTag):
    def __init__(self, lines):
        self.lines = lines

    def get_response(self):
        return self.lines

class Splork(LinguaTag):
    def __init__(self):
        pass
    def get_response(self):
        r = requests.get('https://www.nerderium.com/splork/message')
        print(r)
        return r.json()['message']
