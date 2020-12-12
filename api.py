import os
import flask
from sugaroid import sugaroid
from flask import request
from base64 import b64decode, b64encode
import ast

DOMAINS = [
    "https://sugaroid.srevinsaju.me",
    "http://sugaroid.srevinsaju.me",
    "https://bot.srevinsaju.me",
    "https://srevinsaju.me",
    "https://srevinsaju.github.io"
]

sg = sugaroid.Sugaroid()
app = flask.Flask(__name__)
app.config["DEBUG"] = True if os.getenv("SUGAROID_DEBUG") else False


if os.getenv("SUGAROID_DEBUG"):
    if os.getenv("SUGAROID_CORS"):
        DOMAINS += os.getenv("SUGAROID_CORS")


def process_sugaroid_statement_json_serialize(glob):
    new_history = []
    for i in glob['history']['total']:
        if i == 0:
            new_history.append(0)
            continue
        new_history.append(str(i))
    glob['history']['total'] = new_history
    new_debug = []
    for i in glob['DEBUG']:
        if isinstance(i, str):
            continue

        glob['DEBUG'][i]['response'] = str(glob['DEBUG'][i]['response'])
    return glob


@app.route('/', methods=['GET'])
def home():
    return "<h1>This is Sugaroid API</h1>"


@app.route('/wake', methods=['GET'])
def wake():
    response = flask.jsonify({"test": "Ok"})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@app.route('/chatbot', methods=['POST'])
def process():
    request_params = dict(request.args)
    msg = request_params.pop("usermsg")
    if request.data and request.data.decode() == "NULL":
        pass
    elif request.data:
        json_data = b64decode(request.data).decode()
        print(json_data)
        data = ast.literal_eval(json_data)
        sg.chatbot.globals.update(data)
    parsed_msg = sg.parse(msg)
    new_globals = sg.chatbot.globals
    sg.chatbot.reset_variables()
    try:
        emotion = parsed_msg.emotion
    except AttributeError:
        emotion = 0
    message = str(parsed_msg)
    response = flask.jsonify({"message": message, "emotion": emotion, "data": b64encode(
        str(process_sugaroid_statement_json_serialize(new_globals)).encode('utf-8')).decode()})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == "__main__":
    app.run()
