# -*- coding: utf-8 -*-
# Copyright (c) 2019, Aakvatech and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _

class PaywareSettings(Document):

	def validate(self):
		self.validate_round_total()
		self.validate_base_day()
		self.validate_max_daily()
		self.validate_max_weekly()
		self.validate_max_monthly()
		self.validate_enable_overtime()


	def validate_round_total(self):
		if not self.round_total:
			self.round_total = 0
		if self.round_total < 0 or self.round_total > 1:
			frappe.throw(_("Round Total Overtime value should be between [0, 1]"))


	def validate_base_day(self):
		if not self.base_day:
			self.base_day = 0
		self.base_day = int(self.base_day)
		if self.base_day < 0 or self.base_day > 28:
			frappe.throw(_("Overtime Base Day value should be between [0, 28]"))


	def validate_max_daily(self):
		if not self.max_daily:
			self.max_daily = 0
		self.max_daily = int(self.max_daily)
		if self.max_daily < 0 or self.max_daily > 12:
			frappe.throw(_("Maximum Daily Overtime value should be between [0, 12]"))
	

	def validate_max_weekly(self):
		if not self.max_weekly:
			self.max_weekly = 0
		self.max_weekly = int(self.max_weekly)
		if self.max_weekly < 0 or self.max_weekly > 60:
			frappe.throw(_("Maximum Weekly Overtime value should be between [0, 60]"))


	def validate_max_monthly(self):
		if not self.max_monthly:
			self.max_monthly = 0
		self.max_monthly = int(self.max_monthly)
		if self.max_monthly < 0 or self.max_monthly > 240:
			frappe.throw(_("Maximum Monthly Overtime value should be between [0, 240]"))



	def validate_enable_overtime(self):
		if not self.enable_overtime:
			self.enable_overtime = 0



	def get_enable_overtime(self):
		if not self.enable_overtime:
			self.enable_overtime = 0
		self.enable_overtime = int(self.enable_overtime)
		if self.enable_overtime == 1 :
			return True
		else:
			return False


	def get_overtime_mode(self):
		if not self.overtime_mode:
			frappe.throw(_("Pleas Set Overtime Mode!"))
		else :
			return self.overtime_mode


	def get_base_day(self):
		return int(self.base_day)


	def get_round_total(self):
		return self.round_total


	def get_max_daily(self):
		return self.max_daily


	def get_max_weekly(self):
		return self.max_weekly


	def get_max_monthly(self):
		return self.max_monthly