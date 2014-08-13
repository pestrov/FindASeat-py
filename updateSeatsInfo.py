import parseHelper, json, urllib

def getSeatsOrigins(roomInfo):
  seats = []
  for topKey, topValue in roomInfo.iteritems():
    if topKey == "seats":
      for seat in topValue:
        seats.append((seat["position"][0], seat["position"][1]))
  return seats

def originsMatch(initialOrigin, currentOrigin):
  if (abs(initialOrigin[0] - currentOrigin[0]) < 5) & (abs(initialOrigin[1] - currentOrigin[1]) < 5):
    return True

def splitSeats(initialOrigins, currentOrigins):
  vacantSeats = []
  occupiedSeats = []

  for initialOrigin in initialOrigins:
    foundItemToDelete = 0
    for currentOrigin in currentOrigins:
      if originsMatch(initialOrigin, currentOrigin):
        vacantSeats.append(initialOrigins.index(initialOrigin))
        foundItemToDelete = currentOrigin
        break

    if foundItemToDelete:
      currentOrigins.remove(foundItemToDelete)
    else:
      occupiedSeats.append(initialOrigins.index(initialOrigin))

  return (vacantSeats, occupiedSeats)

def seatInfoToUpdate(seat, state):
  return {
  "method":"PUT",
  "path":"/1/classes/Seat/%s" % seat,
  "body":{
    "vacant":state
    }
  }

def updateSeatsState(seatsIds, state, roomId):

  params = urllib.urlencode({"where":json.dumps({"roomId":roomId}),
                              "order":"seatID"})
  seats = parseHelper.sendParseRequest('GET','/1/classes/Seat?%s' % params, '')
  print seatsIds
  seatsBatch = []
  for seat in seatsIds:
    seatsBatch.append(seatInfoToUpdate(seats["results"][seat]["objectId"], state))
  result = parseHelper.sendParseRequest('POST', '/1/batch', json.dumps({
       "requests":seatsBatch}))
  print result
  print seatsBatch

def updateRoomInfo():
  roomId = parseHelper.readRoomInfo('./data/roomId.json')["roomId"]

  initialRoomInfo = parseHelper.readRoomInfo('./data/initialRoomSetup.json')
  initialOrigins = getSeatsOrigins(initialRoomInfo)

  currentRoomInfo = parseHelper.readRoomInfo('./data/currentRoomSetup.json')
  currentOrigins = getSeatsOrigins(currentRoomInfo)
  splittedSeats = splitSeats(initialOrigins, currentOrigins)
  updateSeatsState(splittedSeats[0], True, roomId)
  updateSeatsState(splittedSeats[1], False, roomId)
  print splittedSeats

updateRoomInfo()
