from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
	
		{
			"label": _("Attendance"),
			"items": [
				
				{
					"type": "report",
					"is_query_report": True,
					"name": "Monthly Attendance Sheet With Overtime",
					"doctype": "Attendance"
				},
			]
		},
		
	]
