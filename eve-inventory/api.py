from eve import Eve
from flask import abort
from bson import ObjectId
from datetime import datetime
from eve.io.mongo import Validator
import cerberus
import string
import re

# def emailtype(self, value):
    
#     if emailtype.is_valid(value):
#     	return True

# emailtype = cerberus.TypeDefinition('emailtype', (str,), ())
# Validator.types_mapping['emailtype'] = emailtype

class EmailValidator(Validator):
    def _validate_isemail(self, isemail, field, value):

        if isemail and re.match("[^@]+@[^@]+\.[^@]+", value) is None:
            self._error(field, "Must be a valid email address")

    def _validate_type_emailtype(self, value):
    	if isinstance(value, str):
    		return True


app = Eve(validator=EmailValidator)

def assignment_check(resourceName, requests):
	if resourceName == "assignments":
		request = requests[0]
		
		employeeDB = app.data.driver.db.employees
		itemDB = app.data.driver.db.items

		item = itemDB.find_one(ObjectId(request["itemId"]))
		employee = employeeDB.find_one(ObjectId(request["employeeId"]))

		qty = item["quantityAvailable"]
		status = employee["active"]

		qty_asgn = request["quantityAssigned"]

		if qty < qty_asgn or status is "N":
			abort(400)


def quantity_change(resourceName, items):
	if resourceName == "assignments":
		itemFetched = items[0]
		
		itemDB = app.data.driver.db.items

		item = itemDB.find_one(ObjectId(itemFetched["itemId"]))
		
		
		prev_qty = item["quantityAvailable"]
		
		qty = itemFetched["quantityAssigned"]
		new_qty = int(prev_qty)-int(qty)
		
		
		itemDB.update_one({'_id':ObjectId(itemFetched["itemId"])},{'$set':{"quantityAvailable":new_qty}})

def remove_items(resourceName, updates, original):
	if resourceName == "employees":

		if original["active"] == "N" and updates["active"] == "N":
			print("Employee Already Inactive")
			abort(400)

		if original["active"] == "Y" and updates["active"] == "Y":
			print("Employee Already Active")
			abort(400)

		if original["active"] == "N" and updates["active"] == "Y":
			employeeDB = app.data.driver.db.employees
			employeeDB.update_one({'_id':ObjectId(str(original['_id']))},{'$set':{"dateOfJoining":datetime.now()}})
			employeeDB.update_one({'_id':ObjectId(str(original['_id']))},{'$set':{"dateOfExit":None}})
		
		if original["active"] == "Y" and updates["active"] == "N":
			itemDB = app.data.driver.db.items
			assignDB = app.data.driver.db.assignments
			assignments = list(assignDB.find({"employeeId": str(original["_id"])}))
		
			for assignment in assignments:
				item = itemDB.find_one(ObjectId(assignment["itemId"]))
				qty=int(item["quantityAvailable"])
				qty+=int(assignment["quantityAssigned"])
				itemDB.update_one({'_id':ObjectId(item["_id"])},{'$set':{"quantityAvailable":qty}})
				
			for assignment in assignments:
				assignDB.delete_one(assignment)		

			employeeDB = app.data.driver.db.employees
			employeeDB.update_one({'_id':ObjectId(str(original['_id']))}, {'$set':{"dateOfExit":datetime.now()}})


app.on_insert += assignment_check
app.on_inserted += quantity_change
app.on_update += remove_items
if __name__=='__main__':
	app.run()