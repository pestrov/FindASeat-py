import parseHelper, json, registerEntrances

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
  result = parseHelper.sendParseRequest("PUT", "/1/classes/Room/" + roomId, json.dumps({"seats":{
                                                          "__op":"AddRelation",
                                                          "objects":updateSeatsBatch
                                                          }
                                                        }))
  print result


def seatInfoForParse(seat, roomId, number):
  return {
  "method":"POST",
  "path":"/1/classes/Seat",
  "body":{
    "seatID":number,
    "vacant":False,
    "x":seat["position"][0],
    "y":seat["position"][1],
    "width":seat["size"][0],
    "height":seat["size"][1],
    "rowID":seat["rowID"],
    "roomId":roomId
    }
  }

def sendSeatsInfo(seatsBatch):
  return parseHelper.sendParseRequest('POST', '/1/batch', json.dumps({
       "requests":seatsBatch}))

def createSeats(seats, roomId):
  seatsBatch = []
  for seat in seats:
    seatsBatch.append(seatInfoForParse(seat, roomId, seats.index(seat)))

    if len(seatsBatch) == parseHelper.parseBatchLimit():
      seatResults = sendSeatsInfo(seatsBatch)
      attachRoomToSeats(seatResults, roomId)
      seatsBatch = []

  if len(seatsBatch) > 0:
    seatResults = sendSeatsInfo(seatsBatch)
    attachRoomToSeats(seatResults, roomId)

def createRoom(roomInfo):
  result = parseHelper.sendParseRequest('POST', '/1/classes/Room', json.dumps({
       "width": roomInfo["size"][0],
       "height": roomInfo["size"][1]
     }))
  roomId = result["objectId"]

  with open('./data/roomId.json', 'w') as outfile:
    json.dump({"roomId":roomId}, outfile)

  return roomId
#Making a request to PARSE server

def registerRoom():
  roomInfo = parseHelper.readRoomInfo('./data/initialRoomSetup.json')
  roomId = createRoom(roomInfo)
  registerEntrances.bindBeaconsToRoom(roomId)
  for topKey, topValue in roomInfo.iteritems():
    if topKey == "seats":
      createSeats(topValue, roomId)

#Just calling the main function
registerRoom()
