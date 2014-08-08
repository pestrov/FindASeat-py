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
