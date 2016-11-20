import json

pyDict = {'type':'dictionary', 'language':'Python'}
print(type(pyDict))
print(pyDict)
# Python object -> JSON string
jsonObj = json.dumps(pyDict)
print(jsonObj)
print(type(jsonObj))
# JSON string -> Python object
jsonToPy = json.loads(jsonObj)
print(jsonToPy)
print(type(jsonToPy))
# comparison: initial Python object vs. JSON-to-Python object
print(pyDict == jsonToPy)
