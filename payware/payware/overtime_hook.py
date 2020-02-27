from __future__ import unicode_literals
import json
import frappe
from frappe.model.document import Document
from dateutil.relativedelta import relativedelta
from frappe.utils import cint, format_datetime,get_datetime_str,now_datetime,add_days,today,formatdate,date_diff,getdate,add_months,flt, nowdate, fmt_money, add_to_date, DATE_FORMAT, rounded, to_timedelta, get_time, get_datetime,time_diff
from frappe import _
from erpnext.hr.doctype.employee.employee import is_holiday
from calendar import monthrange
from datetime import datetime
from dateutil.parser import parse
from payware.payware.doctype.payware_settings import payware_settings
from frappe.desk.form.linked_with import get_linked_docs, get_linked_doctypes




def validate_daily_overtime(emp_name, overtime):
	pass


def validate_weekly_overtime(emp_name, overtime,date):
	pass


def validate_monthly_overtime(emp_name, overtime,date):
	pass

	
def validate_maximum_overtime_for_employee(emp_name, overtime,date):
	return True


def time_diff_in_hours(start, end):
	return round((end-start).total_seconds() / 3600, 1)

def get_chekout_time(doctype,docname):
    linkinfo = get_linked_doctypes(doctype)
    linked_doc = get_linked_docs(doctype,docname,linkinfo)
    if linked_doc:
        for key, value in linked_doc.items() :
            if key != "Activity Log" and key == "Employee Checkin":
                for val in value:
                    log_type = frappe.db.get_value("Employee Checkin", val.name, "log_type")
                    if log_type == "OUT":
                        return frappe.db.get_value("Employee Checkin", val.name, "time")


def get_chekin_time(doctype,docname):
    linkinfo = get_linked_doctypes(doctype)
    linked_doc = get_linked_docs(doctype,docname,linkinfo)
    if linked_doc:
        for key, value in linked_doc.items() :
            if key != "Activity Log" and key == "Employee Checkin":
                for val in value:
                    log_type = frappe.db.get_value("Employee Checkin", val.name, "log_type")
                    if log_type == "IN":
                        return frappe.db.get_value("Employee Checkin", val.name, "time")
                    




@frappe.whitelist()
def calculate_overtime(doc, method):
    if not payware_settings.get_enable_overtime() :
        return

    overtime = 0
    holiday = is_holiday(doc.employee, doc.attendance_date)
    start_time = frappe.db.get_value("Shift Type", doc.shift, "start_time")
    end_time = frappe.db.get_value("Shift Type", doc.shift, "end_time")
    shift_duration = time_diff_in_hours(start_time, end_time)

    if payware_settings.get_overtime_mode() == "Checkout Time":
        
        employee_checkin_date=getdate(get_chekin_time(doc.doctype,doc.name))
        employee_checkin_time=get_chekin_time(doc.doctype,doc.name)
        supposed_employee_checkin_time = str(employee_checkin_date)+ " " + str(start_time)
        supposed_employee_checkout_time = add_to_date(date = supposed_employee_checkin_time, hours = shift_duration)
        employee_checkout_time=get_chekout_time(doc.doctype,doc.name)
        frappe.msgprint("supposed_employee_checkin_time" + " " + str(supposed_employee_checkin_time))
        frappe.msgprint("employee_checkin_time" + " " + str(employee_checkin_time))
        frappe.msgprint("employee_checkout_time" + " " + str(employee_checkout_time))
        frappe.msgprint("supposed_employee_checkout_time" + " " + str(supposed_employee_checkout_time))
        # overtime = flt(employee_checkin_time - supposed_employee_checkout_time, 2)
        overtime = time_diff(employee_checkout_time, supposed_employee_checkout_time)

        if not holiday:
            frappe.msgprint("overtime_normal" +" "+ str(overtime))
            # doc.overtime_normal = overtime
        else:
            frappe.msgprint("overtime_holidays" +" "+ str(overtime))
            # doc.overtime_holidays = overtime

    elif payware_settings.get_overtime_mode() == "Working Hours":

        if doc.working_hours and doc.working_hours>=shift_duration:
            overtime = flt(doc.working_hours - shift_duration, 2)
            
            if not holiday:
                frappe.msgprint("overtime_normal" +" "+ str(overtime))
                # doc.overtime_normal = overtime
            else:
                frappe.msgprint("overtime_holidays" +" "+ str(overtime))
                # doc.overtime_holidays = overtime
            







