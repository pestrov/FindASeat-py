import json, httplib

#Reading the info formed by CV algorithm
def readRoomInfo():
  with open('./data/room.csv') as fp:
    roomInfo = json.load(fp)
  return roomInfo

def credentials():
  return {
    "X-Parse-Application-Id": "Bvvlzr8qEBylzyQ9J4rmpul9iqZS3KZwZ1AbC4Hh",
    "X-Parse-REST-API-Key": "m7DPeMctrrlQvWFglna4FnKQUVBjilqXCq84CCte",
    "Content-Type": "application/json"
  }

#Making a request to PARSE server
def sendInfo(userInfo):
  connection = httplib.HTTPSConnection('api.parse.com', 443)
  connection.connect()
  connection.request('POST', '/1/classes/Room', json.dumps({
       "roomID": 1337
     }),credentials())
  result = json.loads(connection.getresponse().read())
  print result


def registerRoom():
  roomInfo = readRoomInfo()
  sendInfo(roomInfo)
  print(roomInfo)

#Just calling the main function
registerRoom()
