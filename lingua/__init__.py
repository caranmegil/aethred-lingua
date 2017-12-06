import re, random
import xml.etree.ElementTree

def parse(file_name):

    e = xml.etree.ElementTree.parse(file_name).getroot()
    patterns = []
    default = None
    for ptype in e.findall('pattern'):
        responses = []
        pattern = ptype.get('regex')

        for rtype in ptype.findall('response'):
            responses.append(Response(response=rtype.text))
        patterns.append(Pattern(pattern=pattern, responses=responses))
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

class Response(LinguaTag):
    def __init__(self, response):
        self.response = response

    def get_response(self):
        return self.response

class Pattern(LinguaTag):
    def __init__(self, pattern, responses):
        self.pattern = re.compile(pattern)
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
