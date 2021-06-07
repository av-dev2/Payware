# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import fixtures


class AutoFixture(Document):
	def validate(self):
		frappe.msgprint("Validate")
		for identified_app in frappe.get_installed_apps():
			for hook in frappe.get_hooks("fixtures", app_name=identified_app):
				filters = None
				if isinstance(hook, dict):
					doctype_name = hook.get("doctype")
					filters = hook.get("filters")
					for fil in filters:
						for filter in list(fil[2]):
							fixture_doctype = filter.split("-")[0]

							doc = frappe.new_doc("Fixtures")

							doc.doctype_name = doctype_name
							doc.filter = filter
							doc.identified_app = identified_app
							doc.fixture_doctype = fixture_doctype
							doc.save()
							doc.submit()

	#print(validate())
