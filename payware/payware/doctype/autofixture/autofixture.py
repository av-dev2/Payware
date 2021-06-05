# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import fixtures


class AutoFixture(Document):
	def validate(self):
		fixture_lab = []
		for identified_app in frappe.get_installed_apps():
			for hook in frappe.get_hooks("fixtures", app_name=identified_app):
				filters = None
				if isinstance(hook, dict):
					doctype_name = hook.get("doctype")
					filters = hook.get("filters")
					for fil in filters:
						for filter in fil[2]:
							fixture_doctype = filter.split("-")[0]
							
							for item in self.fixture:
								row = fixture_lab.append({"doctype_name": item.doctype_name, "filter": item.filter, "identified_app": item.identified_app, "fixture_doctype": item.fixture_doctype})
								row.doctype_name = doctype_name
								row.filter = filter
								row.identified_app = identified_app
								row.fixture_doctype = doctype_name
								row.save()

"""
autofixture = frappe.new_doc("AutoFixture")
autofixture.old_doc = old_dc
autofixture.filter = filter
autofixture.app = app
autofixture.new_doc = new_dc
autofixture.save()
"""
