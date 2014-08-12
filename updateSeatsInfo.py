import parseHelper, json

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

def updateRoomInfo():
  initialRoomInfo = parseHelper.readRoomInfo('./data/initialRoomSetup.json')
  initialOrigins = getSeatsOrigins(initialRoomInfo)

  currentRoomInfo = parseHelper.readRoomInfo('./data/currentRoomSetup.json')
  currentOrigins = getSeatsOrigins(currentRoomInfo)
  splittedSeats = splitSeats(initialOrigins, currentOrigins)

  print splittedSeats

updateRoomInfo()
