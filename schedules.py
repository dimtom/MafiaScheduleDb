import os
import json


'''
Global dictionary with all schedules
'''
all_schedules = {}


def loadAllSchedules(data_directory):
    '''
    Load all schedules from .txt files in specified directory
    '''
    print(f"Loading schedules from: {data_directory}")
    result = {}
    for root, dirs, files in os.walk(data_directory):
        for filename in files:
            name, ext = os.path.splitext(filename)
            if ext != ".txt":
                print(f"Skipping file: {filename}")
                continue

            full_filename = os.path.join(root, filename)
            print(f"Loading from file: {full_filename}")
            with open(full_filename) as f:
                s = json.load(f)
                result[name] = s
    print(f"Total number of schedules loaded: {len(result)}")
    return result


def findAllSchedules() -> list[str]:
    result = [id for id in all_schedules.keys()]
    return result


def findSchedules(config: dict) -> list[str]:
    result = []
    for id, item in all_schedules.items():
        curr_config = item["configuration"]
        if config["numTables"] and config["numTables"] != curr_config["numTables"]:
            continue
        if config["numPlayers"] and config["numPlayers"] != curr_config["numPlayers"]:
            continue
        if config["numAttempts"] and config["numAttempts"] != curr_config["numAttempts"]:
            continue
        result.append(id)

    return result


def getJsonSchedule(id) -> dict:
    return all_schedules[id]


def getMwtSchedule(id) -> str:
    return "Not implemented"


def getLogSchedule(id) -> str:
    return "Not implemented"
