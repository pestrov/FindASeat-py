import json, httplib

def credentials():
  return {
    "X-Parse-Application-Id": "Bvvlzr8qEBylzyQ9J4rmpul9iqZS3KZwZ1AbC4Hh",
    "X-Parse-REST-API-Key": "m7DPeMctrrlQvWFglna4FnKQUVBjilqXCq84CCte",
    "Content-Type": "application/json"
  }

def parseBatchLimit():
  return 50

def sendParseRequest(requestType, path, data):
  print data
  connection = httplib.HTTPSConnection('api.parse.com', 443)
  connection.connect()
  connection.request(requestType, path, data, credentials())
  result = json.loads(connection.getresponse().read())
  return result

#Reading the info formed by CV algorithm
def readRoomInfo():
  with open('./data/room.json') as fp:
    roomInfo = json.load(fp)
  return roomInfo

def getSeatsIds(seatResults):
  seatsIds = []
  for seat in seatResults:
    for statusKey, value in seat.iteritems():
      if statusKey == "success":
        for key, seatValue in value.iteritems():
          if key == "objectId":
            seatsIds.append(seatValue)
  return seatsIds

def attachRoomToSeats(seatResults, roomId):
  seatsIds = getSeatsIds(seatResults)
  print seatsIds
  updateSeatsBatch = []
  for seatId in seatsIds:
    updateSeatsBatch.append({ "__type": "Pointer",
                              "className": "Seat",
                              "objectId": seatId
                              })
  print "add"
  print updateSeatsBatch
  result = sendParseRequest("PUT", "/1/classes/Room/" + roomId, json.dumps({"seats":{
                                                          "__op":"AddRelation",
                                                          "objects":updateSeatsBatch
                                                          }
                                                        }))
  print result


def seatInfoForParse(seat):
  return {
  "method":"POST",
  "path":"/1/classes/Seat",
  "body":{
    "seatID":seat["number"],
    "vacant":False,
    "x":seat["position"][0],
    "y":seat["position"][1],
    "width":seat["size"][0],
    "height":seat["size"][1]
    }
  }

def sendSeatsInfo(seatsBatch):
  return sendParseRequest('POST', '/1/batch', json.dumps({
       "requests":seatsBatch}))

def createSeats(seats, roomId):
  seatsBatch = []
  for seat in seats:
    seatsBatch.append(seatInfoForParse(seat))

    if len(seatsBatch) == parseBatchLimit():
      seatResults = sendSeatsInfo(seatsBatch)
      attachRoomToSeats(seatResults, roomId)
      seatsBatch = []

  if len(seatsBatch) > 0:
    seatResults = sendSeatsInfo(seatsBatch)
    attachRoomToSeats(seatResults, roomId)

def createRoom(roomInfo):
  result = sendParseRequest('POST', '/1/classes/Room', json.dumps({
       "width": roomInfo["size"][0],
       "height": roomInfo["size"][1]
     }))
  roomId = result["objectId"]
  return roomId
#Making a request to PARSE server

def registerRoom():
  roomInfo = readRoomInfo()
  roomId = createRoom(roomInfo)
  for topKey, topValue in roomInfo.iteritems():
    if topKey == "seats":
      createSeats(topValue, roomId)

#Just calling the main function
registerRoom()
