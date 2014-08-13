import json, parseHelper

result = parseHelper.sendParseRequest('POST','/1/functions/getClosestSeat', json.dumps({
     "roomId": "aF4yoi7HZy"
   }))

print result
