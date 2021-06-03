from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters) 
	data = get_data(filters)
	return columns, data


def get_columns(filters):
	return [
		{
			"fieldname": "first_name",
			"label": _("First Name"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "middle_name",
			"label": _("Middle Name"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "last_name",
			"label": _("Last Name"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "employee_name",
			"label": _("Full Name"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "gender",
			"label": _("Gender"),
			"fieldtype": "Link",
			"options": "Gender"
		},
		{
			"fieldname": "date_of_birth",
			"label": _("Date of Birth"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "date_of_joining",
			"label": _("Date of Joining"),
			"fieldtype": "Date"
		},
		{
			"fieldname": "tin_number",
			"label": _("TIN Number"),
			"fieldtype": "Data"
		},
		{
			"fieldname": "national_identity",
			"label": _("National Identity"),
			"fieldtype": "Data"
		}
	]
	#return columns


def get_conditions(filters):
	conditions = {}

	if filters.company:
		conditions["company"] = filters.company
		return conditions
	
	if filters.status:
		conditions["status"] = filters.status
	
	if filters.gender:
		conditions["gender"] = filters.gender
	
	return conditions


def get_data(filters):
	data  = []

	conditions = get_conditions(filters)

	records = frappe.get_all("Employee", 
			fields=['first_name', 'middle_name', 'last_name', 'employee_name', 'date_of_birth', 
			'gender', 'date_of_joining', 'tin_number', 'national_identity'], filters=conditions
		)
	
	for record in records:
		row = {
			"first_name": record.first_name,
			"middle_name": record.middle_name,
			"last_name": record.last_name, 
			"employee_name": record.employee_name,
			"gender": record.gender,
			"date_of_birth": record.date_of_birth,
			"date_of_joining": record.date_of_joining,
			"tin_number": record.tin_number,
			"national_identity": record.national_identity
		}
	
		data.append(row)

	return data