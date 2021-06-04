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
							autofixture = frappe.new_doc("doc")
							autofixture.old_doc = old_dc
							autofixture.filter = filter
							autofixture.app = app
							autofixture.new_doc = new_dc
							autofixture.save()
							#return auto_fixture
