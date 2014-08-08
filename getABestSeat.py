import json, parseHelper

result = parseHelper.sendParseRequest('POST','/1/functions/getClosestSeat', json.dumps({
     "roomId": "el3DyZD4b2"
   }))

print result
