import xml.etree.ElementTree
import lingua

def parse(file_name):
    e = xml.etree.ElementTree.parse(file_name).getroot()
    for atype in e.findall('pattern'):
        print(atype.get('regex'))
        for rtype in atype.findall('response'):
            print(atype.text)
