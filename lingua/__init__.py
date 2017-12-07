import re, random, threading, time
import xml.etree.ElementTree
import os

def parse_response(rtype):
    mtype = rtype.findall('multiline')
    if mtype:
        lines = []
        for ltype in mtype[0].findall('line'):
            lines.append(ltype.text)
        return Response(response=Multiline(lines=lines))
    else:
        return Response(response=rtype.text)

def parse(file_name):
    e = xml.etree.ElementTree.parse(file_name).getroot()
    patterns = []
    default = None

    for dtype in e.findall('default'):
        responses = []

        for rtype in dtype.findall('response'):
            if rtype:
                responses.append(parse_response(rtype[0]))

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
                self.brain_lock.acquire()
                self.brain = parse(self.file_name)
                self.last_parsed_time = file_time
                self.brain_lock.release()

            time.sleep(10)

class LinguaTag:
    def get_response(self):
        return None

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
