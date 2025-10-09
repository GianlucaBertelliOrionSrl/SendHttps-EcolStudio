import json

def PythonToJSON():
	x = {
		"name": "John",
		"age": 30,
		"married": True,
		"divorced": False,
		"children": ("Ann","Billy"),
		"pets": None,
		"cars": 
		[
			{"model": "BMW 230", "mpg": 27.5},
			{"model": "Ford Edge", "mpg": 24.1}
		]
	}

	s = json.dumps(x) 
	print(s)

def CheckStringJSON(s):
	try:
		o = json.loads(s) #JSON OBJ from STRING
		b = True
	except ValueError:
		b = False

	return b

def StringToJSON(s):
	n = json.dumps(s) #STRING from JSON OBJ
	b = CheckStringJSON(n)

	if b==True:
		js = json.loads(n) #JSON OBJ from STRING
		return js

def StringToJSONdict(s):
	js = json.loads(s) #JSON OBJ from STRING
	return js

def FileToJSON(f):
	with open(f,"r") as json_file:
		json_data = json.load(json_file)

	json_obj = json.dumps(json_data)

	b = CheckStringJSON(json_obj)

	if b==True:
		js = json.loads(json_obj)
		n = len(js)
	else:
		js = ""

	return js

def CheckFileJSON(f):
	try:
		with open(f,"r") as json_file:
			json_data = json.load(json_file)

		json_obj = json.dumps(json_data)
		b = CheckStringJSON(json_obj)
	except Exception as e:
		print(str(e))
		b = False

	return b

