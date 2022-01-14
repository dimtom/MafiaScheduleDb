import os
import itertools
import json

import mafia_schedule as ms

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


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

def loadAllSchedulesFromAzure(connection_string, container_name):
    '''
    Load all schedules from Azure blob service (in schedules container)
    '''
    service = BlobServiceClient.from_connection_string(connection_string)
    container = service.get_container_client(container_name)

    result = {}
    for blob in container.list_blobs():
        stream = container.download_blob(blob)
        s = stream.content_as_text()
        result[blob.name] = s
    
    print(f"Total number of schedules loaded: {len(result)}")
    return result
      
        

def findAllSchedules():
    result = [id for id in all_schedules.keys()]
    return result


def findSchedules(config: dict):
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
    s = ms.Schedule.fromJson(all_schedules[id])
    lines = ms.Print.mwtSchedule(s)
    return '\n'.join(lines)


def getLogSchedule(id) -> str:
    s = ms.Schedule.fromJson(all_schedules[id])
    s.generateSlotsFromGames()

    lines = itertools.chain(
        ms.Print.scheduleByGames(s),
        ms.Print.scheduleByPlayers(s),
        ms.Print.opponentsMatrix(s),
        ms.Print.pairsMatrix(s),
        ms.Print.minMaxPairs(s, [0, 1]),
        ms.Print.minMaxPairs(s, [6, 7, 8, 9]),
        ms.Print.seatsMatrix(s),
        ["\n*** MWT-compatible schedule:"],
        ms.Print.mwtSchedule(s))

    return '\n'.join(lines)
