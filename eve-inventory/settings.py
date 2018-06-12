from datetime import datetime

RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DBNAME = 'inventory'

DATE_FORMAT = "%d-%m-%Y %I:%M:%S"

IF_MATCH = False

item_schema = {
	"name":{
		"required":True,
		"type":"string",
	},
	"quantityAvailable":{
		"required":True,
		"type":"integer",
	},
	"type":{
		"type":"string",
	},
	"price":{
		"required":True,
		"type":"integer",
	},
	"description":{
		"type":"string",
	}
}

employee_schema={
	"name":{
		"type":"string",
		"required":True
	},
	"dateOfJoining":{
		"type":"datetime",
		"default":datetime.now()
	},
	"active":{
		"type":"string",
		"default":"Y",
		"maxlength":1
	},
	"dateOfExit":{
		"type":"string",
		"required":False,
	},
	"email":{
		"isemail":True,	
		"type":"emailtype"
	}
}

item_resource = {
	"schema": item_schema,
	"additional_lookup":{
		'url':'regex("[\d]+")',
		'field':'_id'
	},
}

employee_resource = {
	"schema": employee_schema,
	"additional_lookup":{
		'url':'regex("[\d]+")',
		'field':'_id'
	},
}

assignment_schema ={
	"employeeId":{
		"type":"string",
		"data_relation": {
            "resource": "employee",
            "field":"_id"
        },
	},
	"itemId":{
		"type":"string",
		"data_relation":{
			"resource":"item",
			"field":"_id"
		},
	},
	"quantityAssigned":{
		"type":"integer",
	},
	"fromDate":{
		"type":"datetime",
		"default":datetime.now()
	},
	"toDate":{
		"type":"datetime",
		"required":False,
	}
}

assignment_resource = {
	"schema": assignment_schema,
	"additional_lookup":{
		'url':'regex("[\d+]")',
		'field':'_id'
	},
}

DOMAIN={
	'employees':employee_resource,
	'items':item_resource,
	'assignments':assignment_resource,
}
