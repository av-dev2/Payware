// Copyright (c) 2016, Aakvatech and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"optons": "Company",
			"default": frappe.defaults.get_user_default("Company")
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options":[
				" ",
				"Active",
				"Left"
			], 
			"default": ""
		}, 
		{
			"fieldname": "gender",
			"label": __("Gender"),
			"fieldtype": "Link",
			"options": "Gender"
		}
	]
};
