import re, random
import xml.etree.ElementTree

def parse_response(rtype):
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

class LinguaTag:
    def __init__(self):
        pass

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

class Response(LinguaTag):
    def __init__(self, response):
        self.response = response

    def get_response(self):
        return self.response

class Pattern(LinguaTag):
    def __init__(self, regex, responses):
        self.regex = re.compile(regex)
        self.responses = responses

    def get_response(self):
        response = random.choice(self.responses)
        return response.get_response()

class Default(LinguaTag):
    def __init__(self, responses):
        self.responses = responses

    def get_response(self):
        response = random.choice(self.responses)
        return response.get_response()
