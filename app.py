import flask
import os

# create a new flask application
app = flask.Flask(__name__)


@app.route("/")
def handler_main():
    return "MafiaScheduleDb"


@app.route("/health", methods=['GET'])
def handler_health():
    response = flask.make_response("Health status: OK")
    return response, 200
