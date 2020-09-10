from flask import Flask, request, jsonify
import lingua
import json
import time

aethred = lingua.Brain()
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
