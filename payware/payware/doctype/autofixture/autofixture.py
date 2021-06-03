# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import fixtures


class AutoFixture(Document):
	def validate(self):
		self.create_fixture()


	def create_fixture(self):
		for app in frappe.get_installed_apps():
			for hook in frappe.get_hooks("fixtures", app_name=app):
				filters = None
				if isinstance(hook, dict):
					old_dc = hook.get("doctype")
					filters = hook.get("filters")
					for fil in filters:
						for filter in fil[2]:
							new_dc = filter.split("-")[0]
							auto_fixture = frappe.new_doc("doc")
							auto_fixture.old_doc = old_dc
							auto_fixture.filter = filter
							auto_fixture.app = app
							auto_fixture.new_doc = new_dc
							auto_fixture.save()
