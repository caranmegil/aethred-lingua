from flask import Flask, request, jsonify
import lingua
import json

app = Flask(__name__)

brain = lingua.parse('aethred.xml')

@app.route('/', methods=['POST'])
def getResponse():
    obj = json.loads(request.get_data())
    return jsonify({'response': [brain.get_response(text=obj['text'])]})
