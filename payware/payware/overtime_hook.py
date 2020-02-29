from __future__ import unicode_literals
# import json
import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import get_first_day, getdate, flt, add_to_date, rounded, time_diff_in_hours ,get_first_day_of_week
from frappe import _
from erpnext.hr.doctype.employee.employee import is_holiday
# from calendar import monthrange
from payware.payware.doctype.payware_settings import payware_settings
from frappe.desk.form.linked_with import get_linked_docs, get_linked_doctypes


def validate_min_overtime(overtime):
    if overtime >= payware_settings.get_min_overtime():
        return overtime
    else:
        return 0

def validate_daily_overtime(overtime):
    if payware_settings.get_max_daily() == 0:
        return overtime
    if overtime <= payware_settings.get_max_daily():
        return overtime
    else:
        return payware_settings.get_max_daily()


def validate_weekly_overtime(emp_name, overtime,date):
    max_weekly = payware_settings.get_max_weekly()
    if max_weekly== 0:
        return overtime
    start_week_date = get_first_day_of_week(date)
    sum_overtime = get_sum_overtime(emp_name,start_week_date,date)
    full_overtime = overtime + sum_overtime["sum_overtime_holidays"] + sum_overtime["sum_overtime_normal"]
    if full_overtime <= max_weekly:
        return overtime
    elif  sum_overtime <= max_weekly:
        return max_weekly - sum_overtime
    else:
        return 0
        


def validate_monthly_overtime(emp_name, overtime,date):
    max_monthly = payware_settings.get_max_monthly()
    if max_monthly == 0:
        return overtime
    start_month_date = get_first_day(date)
    sum_overtime = get_sum_overtime(emp_name,start_month_date,date)
    full_overtime = overtime + sum_overtime["sum_overtime_holidays"] + sum_overtime["sum_overtime_normal"]
    if full_overtime <= max_monthly:
        return overtime
    elif  sum_overtime <= max_monthly:
        return max_monthly - sum_overtime
    else:
        return 0


def get_sum_overtime(emp_name,start_date,end_date):
    # frappe.msgprint(str(emp_name)+" "+str(start_date)+" "+str(end_date))
    query = """select sum(overtime_normal) as overtime_normal, sum(overtime_holidays) as overtime_holidays
		from `tabAttendance` where
		attendance_date between %(from_date)s and %(to_date)s
		and docstatus < 2 and employee = %(employee)s"""
    overtime_sums = frappe.db.sql(query, {"from_date":start_date, "to_date":end_date, "employee":emp_name}, as_dict=True)

    sum_overtime_normal = overtime_sums[0]["overtime_normal"] or 0
    sum_overtime_holidays = overtime_sums[0]["overtime_holidays"] or 0

    return {"sum_overtime_normal":sum_overtime_normal , "sum_overtime_holidays":sum_overtime_holidays}

	
def validate_maximum_overtime_for_employee(emp_name, overtime, date):
    overtime = validate_min_overtime(overtime)
    overtime = validate_daily_overtime(overtime)
    overtime = validate_weekly_overtime(emp_name, overtime, date)
    overtime = validate_monthly_overtime(emp_name, overtime, date)
    return overtime


def time_diff_in_hour(start, end):
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
    if frappe.db.get_value("Shift Type", doc.shift, "determine_check_in_and_check_out") != 'Strictly based on Log Type in Employee Checkin':
        return
    overtime = 0
    holiday = is_holiday(doc.employee, doc.attendance_date)
    start_time = frappe.db.get_value("Shift Type", doc.shift, "start_time")
    end_time = frappe.db.get_value("Shift Type", doc.shift, "end_time")
    shift_duration = time_diff_in_hour(start_time, end_time)

    if payware_settings.get_overtime_mode() == "Checkout Time":
        # frappe.msgprint("Checkout Time")
        employee_checkout_time=get_chekout_time(doc.doctype,doc.name)
        if not employee_checkout_time:
            return
        employee_checkin_time=get_chekin_time(doc.doctype,doc.name)
        if not employee_checkin_time:
            return
        employee_checkin_date=getdate(employee_checkin_time)
        supposed_employee_checkin_time = str(employee_checkin_date)+ " " + str(start_time)
        supposed_employee_checkout_time = add_to_date(date = supposed_employee_checkin_time, hours = shift_duration)

        overtime = flt(time_diff_in_hours(employee_checkout_time, supposed_employee_checkout_time),2)

        if overtime < 0:
            return
        overtime = validate_maximum_overtime_for_employee(doc.employee, overtime, doc.attendance_date)
        if not holiday:
            # frappe.msgprint("overtime_normal" +" "+ str(overtime))
            doc.overtime_normal = overtime
        else:
            # frappe.msgprint("overtime_holidays" +" "+ str(overtime))
            doc.overtime_holidays = overtime

    elif payware_settings.get_overtime_mode() == "Working Hours":
        # frappe.msgprint("Working Hours")

        if doc.working_hours and doc.working_hours>=shift_duration:
            overtime = flt(doc.working_hours - shift_duration, 2)
            overtime = validate_maximum_overtime_for_employee(doc.employee, overtime, doc.attendance_date)
            if not holiday:
                # frappe.msgprint("overtime_normal" +" "+ str(overtime))
                doc.overtime_normal = overtime
            else:
                # frappe.msgprint("overtime_holidays" +" "+ str(overtime))
                doc.overtime_holidays = overtime


# def get_shift_duration(shift_name):
#     start_time = frappe.db.get_value("Shift Type", shift_name, "start_time")
#     end_time = frappe.db.get_value("Shift Type", shift_name, "end_time")
#     shift_duration = time_diff_in_hour(start_time, end_time)
#     return shift_duration


def geet_overtime_amount(emp_name,start_date,end_date,salary_component_doc,base):
    sum_overtime = get_sum_overtime(emp_name,start_date,end_date)
    sum_overtime_holidays = sum_overtime["sum_overtime_holidays"] 
    sum_overtime_normal = sum_overtime["sum_overtime_normal"]
    # frappe.msgprint("Base = "+str(base))
    # frappe.msgprint("sum_overtime_normal = "+str(sum_overtime_normal)+ "/ sum_overtime_holidays = " + str(sum_overtime_holidays))
    working_hours_per_month = payware_settings.get_working_hours_per_month()
    if salary_component_doc.based_on_hourly_rate and salary_component_doc.is_overtime and salary_component_doc.overtime_type == "Overtime Normal":
	    overtime_amount = (float(base)/ float(working_hours_per_month)) *  float(sum_overtime_normal) * (float(salary_component_doc.hourly_rate) / 100)
    elif salary_component_doc.based_on_hourly_rate and salary_component_doc.is_overtime and salary_component_doc.overtime_type == "Overtime Holidaysl":
        overtime_amount = (float(base)/ float(working_hours_per_month)) *  float(sum_overtime_holidays) * (float(salary_component_doc.hourly_rate) / 100)
    else:
        overtime_amount = 0
    # frappe.msgprint("overtime_amount = "+str(overtime_amount))
    return overtime_amount


@frappe.whitelist()
def calculate_overtime_amount(doc, method):
    if not payware_settings.get_enable_overtime() :
        return
    if doc.docstatus != 0:
        return
    add_overtime_components(doc)
    for component in doc.earnings:
        if str(component.salary_component).upper() == "BASIC":
            base = component.amount / doc.payment_days * doc.total_working_days
        if base == None:
            frappe.throw("Basic Component not Found")
    for earning_row in doc.earnings :
        component_doc = frappe.get_doc("Salary Component", earning_row.salary_component)
        if component_doc and component_doc.is_overtime and component_doc.based_on_hourly_rate:
            overtime_amount = geet_overtime_amount(doc.employee,doc.start_date,doc.end_date,component_doc,base)
            earning_row.amount = overtime_amount
    frappe.db.commit()
    doc.calculate_net_pay()


def add_overtime_components(salary_slip_doc):
    salary_structure = frappe.get_doc("Salary Structure", salary_slip_doc.salary_structure)
    for earning_row in salary_structure.earnings:
        exist = False
        component_doc = frappe.get_doc("Salary Component", earning_row.salary_component)
        if component_doc and component_doc.is_overtime and component_doc.based_on_hourly_rate:
            for component in salary_slip_doc.earnings :
                if component.salary_component == component_doc.name:
                    exist = True
                    # frappe.msgprint("Salary Overtime Component IS Exist "+ str(component_doc.name))
            if exist == False:
                # frappe.msgprint("Salary Overtime Component NOT Exist "+ str(component_doc.name))
                new = salary_slip_doc.append('earnings', {})
                new.salary_component = earning_row.salary_component
                new.abbr = earning_row.abbr
                frappe.db.commit()
                