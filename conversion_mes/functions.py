import frappe
from frappe.utils import nowdate, time_diff_in_seconds
from datetime import datetime, timedelta



@frappe.whitelist(allow_guest=True)
def site_automation():
    today_date = nowdate()
    today_day = datetime.now().strftime("%A")
    sites = frappe.get_all("Site", filters={"is_active": "1", "enable_site_automation": "1"})
    for site in sites:
        site = frappe.get_doc("Site", site.name)
        is_today_working = is_working_day_checker(today_day, site)
        if is_today_working == 1:
            is_today_holiday = is_holiday_checker(today_date, site)
            if is_today_holiday is False:
                create_shift_logs(site, today_date)
                create_breaks_dt(site, today_date)


def is_working_day_checker(today_day, site):
    if today_day == "Monday":
        return site.monday
    elif today_day == "Tuesday":
        return site.tuesday
    elif today_day == "Wednesday":
        return site.wednesday
    elif today_day == "Thursday":
        return site.thursday
    elif today_day == "Friday":
        return site.friday
    elif today_day == "Saturday":
        return site.saturday
    elif today_day == "Sunday":
        return site.sunday
    else:
        return False
    

def is_holiday_checker(today_date, site):
    holiday_list = frappe.get_doc("Holiday List", site.holiday_list)
    print(f'Holiday List: {holiday_list.name}')
    holidays = holiday_list.holidays
    for holiday in holidays:
        if str(holiday.holiday_date) == str(today_date):
            return True
    return False

def create_holiday_dt(today_date, site, holiday_description):
    day_start_time = site.start_time
    day_end_time = site.end_time
    reason = site.downtime_reason_for_holidays
    start_datetime = datetime.strptime(f"{today_date} {day_start_time}", "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.strptime(f"{today_date} {day_end_time}", "%Y-%m-%d %H:%M:%S")
    if end_datetime <= start_datetime:
        end_datetime += timedelta(days=1)
    workstations = frappe.get_all("Workstation", filters={"site": site.name})
    for workstation in workstations:
        workstation = frappe.get_doc("Workstation", workstation.name)
        downtime_log = frappe.new_doc("Downtime Log")
        downtime_log.status = "Closed"
        downtime_log.created_date = today_date
        downtime_log.workstation = workstation.name
        downtime_log.site = site.name
        downtime_log.start_date_time = start_datetime
        downtime_log.end_date_time = end_datetime
        downtime_log.reason = reason
        downtime_log.remarks = holiday_description
        downtime_log.save()
        frappe.db.commit()

def create_no_shifts_dt(today_date, site):
    next_day = datetime.strptime(today_date, "%Y-%m-%d") + timedelta(days=1)
    day_start_time = site.start_time
    day_end_time = site.end_time
    reason = site.downtime_reason_for_non_working_hours
    
    # Ensure time strings are correctly formatted
    start_datetime = datetime.strptime(f"{today_date} {day_end_time}", "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.strptime(f"{next_day.strftime('%Y-%m-%d')} {day_start_time}", "%Y-%m-%d %H:%M:%S")
    
    workstations = frappe.get_all("Workstation", filters={"site": site.name})
    for workstation in workstations:
        workstation = frappe.get_doc("Workstation", workstation.name)
        downtime_log = frappe.new_doc("Downtime Log")
        downtime_log.status = "Closed"
        downtime_log.created_date = today_date
        downtime_log.workstation = workstation.name
        downtime_log.site = site.name
        downtime_log.start_date_time = start_datetime
        downtime_log.end_date_time = end_datetime
        downtime_log.reason = reason
        downtime_log.remarks = "System Generated Downtime: No Shift Scheduled"
        downtime_log.save()
        frappe.db.commit()


def create_non_working_day_dt(today_date, site):
    day_start_time = site.start_time
    day_end_time = site.end_time
    reason = site.downtime_reason_for_non_working_days
    start_datetime = datetime.strptime(f"{today_date} {day_start_time}", "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.strptime(f"{today_date} {day_end_time}", "%Y-%m-%d %H:%M:%S")
    if end_datetime <= start_datetime:
        end_datetime += timedelta(days=1)
    workstations = frappe.get_all("Workstation", filters={"site": site.name})
    for workstation in workstations:
        workstation = frappe.get_doc("Workstation", workstation.name)
        downtime_log = frappe.new_doc("Downtime Log")
        downtime_log.status = "Closed"
        downtime_log.created_date = today_date
        downtime_log.workstation = workstation.name
        downtime_log.site = site.name
        downtime_log.start_date_time = start_datetime
        downtime_log.end_date_time = end_datetime
        downtime_log.reason = reason
        downtime_log.remarks = "System Generated Downtime: Non Working Day"
        downtime_log.save()
        frappe.db.commit()


def create_breaks_dt(site, today_date):
    planned_breaks = site.breaks
    for planned_break in planned_breaks:
        description = planned_break.description
        reason = planned_break.downtime_reason
        start_time = planned_break.start_time
        end_time = planned_break.end_time
        start_datetime = datetime.strptime(f"{today_date} {start_time}", "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(f"{today_date} {end_time}", "%Y-%m-%d %H:%M:%S")
        workstations = frappe.get_all("Workstation", filters={"site": site.name})
        for workstation in workstations:
            workstation = frappe.get_doc("Workstation", workstation.name)
            downtime_log = frappe.new_doc("Downtime Log")
            downtime_log.status = "Closed"
            downtime_log.created_date = today_date
            downtime_log.workstation = workstation.name
            downtime_log.site = site.name
            downtime_log.start_date_time = start_datetime
            downtime_log.end_date_time = end_datetime
            downtime_log.reason = reason
            downtime_log.remarks = description
            downtime_log.save()
            frappe.db.commit()


def create_shift_logs(site, today_date):
    shifts = site.shift_timings
    if shifts:
        for shift in shifts:
            shift_name = shift.shift_name
            start_time = shift.start_time
            end_time = shift.end_time
            workstations = frappe.get_all("Workstation", filters={"site": site.name})
            for workstation in workstations:
                shift_log = frappe.new_doc("Shift Log")
                shift_log.workstation = workstation
                shift_log.shift = shift_name
                shift_log.date = today_date
                shift_log.start_time = start_time
                shift_log.end_time = end_time
                shift_log.save()
                frappe.db.commit()