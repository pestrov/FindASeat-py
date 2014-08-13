import parseHelper, json
def createBeacon():
  result = parseHelper.sendParseRequest('POST','/1/classes/Entrance', json.dumps({
       "entranceNumber": 100001,
       "x": 100,
       "y": 150
     }))

  print result

  for key, value in result.iteritems():
    if key == "objectId":
      return value
  return False

def bindBeaconsToRoom(roomId):
  createdBeaconId = createBeacon()
  print "Started"
  parseHelper.sendParseRequest("PUT", "/1/classes/Entrance/" + createdBeaconId,
   json.dumps({
       "room":{
         "__op": "AddRelation",
         "objects": [
           {
             "__type": "Pointer",
             "className": "Room",
             "objectId": roomId
           }
         ]
       }
       }))
