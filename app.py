import flask
import os
import sys
import time

import schedules

from decouple import config

start_time = time.gmtime(time.time())

# create a new flask application
app = flask.Flask(__name__)

# initialization: load all schedules to dictionary
# data_directory = os.path.join(app.root_path, 'data')
# schedules.all_schedules = schedules.loadAllSchedules(data_directory)

connection_string = config('AZURE_STORAGE_CONNECTION_STRING', default=None)
container_name = "schedules"
if connection_string:
    schedules.all_schedules = schedules.loadAllSchedulesFromAzure(
        connection_string, container_name)

    # just a hint that data was loaded from Azure Blob service
    schedules.all_schedules["azure"] = '{"azure": 1}'


@app.route("/")
def handler_main():
    return flask.render_template("index.html", base_url=flask.request.base_url)


@app.route("/info", methods=['GET'])
def handler_info():
    curr_time = time.gmtime(time.time())

    version_lines = []
    version_filename = "./github_version.txt"
    if os.path.exists(version_filename):
        with open(version_filename) as f:
            version_lines = f.readlines()

    lines = version_lines + [
        f"Python version: {sys.version}",
        f"Start: {time.asctime(start_time)}",
        f"Now  : {time.asctime(curr_time)}",
    ]
    text = '\n'.join(lines)
    response = flask.make_response(text)
    response.mimetype = "text/plain"
    return response


@app.route("/health", methods=['GET'])
def handler_health():
    response = flask.make_response("Health status: OK")
    return response, 200


@app.route("/schedule", methods=['GET'])
def handler_allSchedules():
    ids = schedules.findAllSchedules()

    response = {"schedules": ids}
    return response


@app.route("/schedule/<id>", methods=['GET'])
def handler_getSchedule(id):
    if id not in schedules.all_schedules:
        flask.abort(404)
        return

    mode = flask.request.args.get("mode", "json")
    mode = mode.lower()

    response = None
    if mode == "json":
        response = flask.make_response(schedules.getJsonSchedule(id), 200)
        response.mimetype = "application/json"
    elif mode == "mwt":
        response = flask.make_response(schedules.getMwtSchedule(id), 200)
        response.mimetype = "text/plain"
    elif mode == "log":
        response = flask.make_response(schedules.getLogSchedule(id), 200)
        response.mimetype = "text/plain"
    else:
        flask.abort(
            400, "Invalid mode value. Valid values are: json | mwt | log.")
    return response


@app.route("/find")
def handler_find():
    numPlayers = flask.request.args.get("players", 0)
    numTables = flask.request.args.get("tables", 0)
    numAttempts = flask.request.args.get("distance", 0)

    try:
        configuration = {
            "numPlayers": int(numPlayers),
            "numTables": int(numTables),
            "numAttempts": int(numAttempts)
        }
    except ValueError:
        flask.abort(400)

    ids = schedules.findSchedules(configuration)
    response = {"schedules": ids}
    return response
