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
    elif rtype.findall('ref'):
        for rrtype in rtype.findall('ref'):
            id = rrtype.get('id')
            return Response(response=Ref(id=id))
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
    mappings = {}
    blocks = []

    for dtype in e.findall('default'):
        responses = []

        for rtype in dtype.findall('response'):
            responses.append(parse_response(rtype))

        default = Default(responses=responses)

    for btype in e.findall('block'):
        id = btype.get('id')
        responses = []

        for rtype in btype.findall('response'):
            responses.append(parse_response(rtype))

        if not id == None:
           block = Block(responses = responses)
           blocks.append(block)
           mappings[id] = block
 
    for ptype in e.findall('pattern'):
        responses = []
        regex = ptype.get('regex')
        id = ptype.get('id')

        for rtype in ptype.findall('response'):
            responses.append(parse_response(rtype))

        pattern = Pattern(regex=regex, responses=responses)
        patterns.append(pattern)
        if not id == None:
            mappings[id] = pattern
    return Lingua(default=default, patterns=patterns, mappings=mappings, blocks=blocks)

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
    def __init__(self, default, patterns, mappings={}, blocks=None):
        self.default = default
        self.patterns = patterns
        self.mappings = mappings
        self.blocks = blocks

    def get_response(self, text):
        for pattern in self.patterns:
            m = pattern.regex.match(text)
            if m:
                return pattern.get_response(self.mappings)
        return self.default.get_response(self.mappings)

class LinguaTag:
    def get_response(self, mappings):
        return None

class Default(LinguaTag):
    def __init__(self, responses):
        self.responses = responses

    def get_response(self, mappings):
        response = random.choice(self.responses)
        return response.get_response(mappings)

class Response(LinguaTag):
    def __init__(self, response):
        self.response = response

    def get_response(self, mappings):
        if type(self.response) is Multiline:
            return self.response.get_response(mappings)
        elif type(self.response) is Splork:
            return self.response.get_response(mappings)
        elif type(self.response) is Ref:
            return self.response.get_response(mappings)
        return self.response

class Ref(LinguaTag):
    def __init__(self, id):
        self.id = id

    def get_response(self, mappings):
        response = mappings[self.id]
        return response.get_response(mappings)

class Pattern(LinguaTag):
    def __init__(self, regex, responses):
        self.regex = re.compile(regex, re.IGNORECASE)
        self.responses = responses

    def get_response(self, mappings):
        response = random.choice(self.responses)
        return response.get_response(mappings)

class Block(LinguaTag):
    def __init__(self, responses):
        self.responses = responses

    def get_response(self, mappings):
        response = random.choice(self.responses)
        return response.get_response(mappings)

class Multiline(LinguaTag):
    def __init__(self, lines):
        self.lines = lines

    def get_response(self, mappings):
        return self.lines

class Splork(LinguaTag):
    def __init__(self):
        pass
    def get_response(self, mappings):
        r = requests.get('https://splork.herokuapp.com/message')
        print(r)
        return r.json()['message']
