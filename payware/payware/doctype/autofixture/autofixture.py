# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import fixtures


class AutoFixture(Document):
    pass


def on_reload():
    #frappe.db.sql("DELETE FROM `tabAuFix` WHERE name != 'a1' ")
    frappe.db.commit()
    for app_name in frappe.get_installed_apps():
        for fixture_doc in frappe.get_hooks("fixtures", app_name=app_name):
            filters = None
            if isinstance(fixture_doc, dict):
                doctype_name = fixture_doc.get("doctype")
                filters = fixture_doc.get("filters")
                for fil in filters:
                    for filter in list(fil[2]):
                        custom_doctype = filter.split("-")[0]
                        #identified_fieldname = filter.split("-")[1]
                        #property_type = filter.split("-")[2]

                        doc = frappe.new_doc("AutoFixture")
                        doc.doctype_name = doctype_name
                        doc.filter = filter
                        doc.identified_app = app_name
                        doc.custom_doctype = custom_doctype
                        #doc.identified_fieldname = identified_fieldname
                        #doc.property_type = property_type
                        doc.insert(ignore_if_duplicate=True)


on_reload()
