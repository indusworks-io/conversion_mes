# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime

def execute(filters=None):
	sites = filters.get("site", [])
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	columns = get_columns()
	data = get_data(sites, from_date, to_date)
	return columns, data


def get_columns():
	return [
		# Return following columns: Workstation	Total Time	Schedule Loss	Planned Downtime	Planned Production Time	Unplanned Downtime	Run Time	Utilization Percentage	Availability Percentage	Output	Scrap	Total Output	Ideal Run Rate	Performance Percentage	Quality	OEE	TEEP
		{"fieldname": "workstation", "label": "Workstation", "fieldtype": "Link", "options": "Workstation", "width": 200},
		{"fieldname": "total_time", "label": "Total Time", "fieldtype": "Duration", "width": 150},
		{"fieldname": "shift_duration", "label": "Shift Duration", "fieldtype": "Duration", "width": 150},
		{"fieldname": "planned_downtime", "label": "Planned Downtime", "fieldtype": "Duration", "width": 150},
		{"fieldname": "planned_production_time", "label": "Planned Production Time", "fieldtype": "Duration", "width": 150},
		{"fieldname": "unplanned_downtime", "label": "Unplanned Downtime", "fieldtype": "Duration", "width": 150},
		{"fieldname": "run_time", "label": "Run Time", "fieldtype": "Duration", "width": 150},
		{"fieldname": "utilization", "label": "Utilization Percentage", "fieldtype": "Percent", "width": 150},
		{"fieldname": "availability", "label": "Availability Percentage", "fieldtype": "Percent", "width": 150},
		{"fieldname": "output", "label": "Output", "fieldtype": "Float", "width": 150},
		{"fieldname": "scrap", "label": "Scrap", "fieldtype": "Float", "width": 150},
		{"fieldname": "total_output", "label": "Total Output", "fieldtype": "Int", "width": 150},
		{"fieldname": "ideal_cycle_time", "label": "Ideal Cycle Time", "fieldtype": "Duration", "width": 150},
		{"fieldname": "performance", "label": "Performance Percentage", "fieldtype": "Percent", "width": 150},
		{"fieldname": "quality", "label": "Quality", "fieldtype": "Percent", "width": 150},
		{"fieldname": "oee", "label": "OEE", "fieldtype": "Percent", "width": 150},
		{"fieldname": "teep", "label": "TEEP", "fieldtype": "Percent", "width": 150}
	]

# def get_total_time(from_date, to_date):
# 	try:
# 		total_time = (datetime.strptime(to_date, "%Y-%m-%d") - datetime.strptime(from_date, "%Y-%m-%d")).total_seconds()
# 	except ValueError:
# 		total_time = 0  # Handle invalid dates gracefully
# 	return total_time

def get_total_time(from_date, to_date):
    try:
        from_dt = datetime.strptime(from_date, "%Y-%m-%d")
        to_dt = datetime.strptime(to_date, "%Y-%m-%d")
        if from_dt == to_dt:
            total_time = 86400  # 24 hours in seconds
        else:
            total_time = (to_dt - from_dt).total_seconds()
    except ValueError:
        total_time = 0  # Handle invalid dates gracefully
    return total_time


def get_downtime_losses(workstation, from_date, to_date):
	schedule_loss = 0
	planned_downtime = 0
	unplanned_downtime = 0
	
	downtime_logs = frappe.get_all("Downtime Log", filters={"workstation": workstation, "created_date": ["between", [from_date, to_date]]}, fields=["category", "duration"])

	for log in downtime_logs:
		duration = log['duration'] or 0
		if log['category'] == "Schedule Loss":
			schedule_loss += duration
		elif log['category'] == "Planned Downtime":
			planned_downtime += duration
		elif log['category'] == "Unplanned Downtime":
			unplanned_downtime += duration
	return schedule_loss, planned_downtime, unplanned_downtime

def get_manufacturing_data(workstation, from_date, to_date):
	manufacturing_orders = frappe.get_all("Manufacturing Order", filters={"workstation": workstation, "posting_date": ["between", [from_date, to_date]], "status":"Completed"}, fields=["planned_cycle_time","total_actual_output_quantity_in_alternate_uom", "total_actual_scrap_quantity_in_alternate_uom",])

	output = 0
	scrap = 0
	total_output = 0
	weighed_count = 0

	for manufacturing_order in manufacturing_orders:
		output_quantity = manufacturing_order['total_actual_output_quantity_in_alternate_uom'] or 0
		scrap_quantity = manufacturing_order['total_actual_scrap_quantity_in_alternate_uom'] or 0
		total_quantity = output_quantity + scrap_quantity
		pcc = manufacturing_order['planned_cycle_time'] or 0
		output += output_quantity
		scrap += scrap_quantity
		total_output += total_quantity
		weighed_count += pcc * total_output

	if total_output == 0:
		pcc = 0
	else:
		pcc = weighed_count / total_output

	return pcc, output, scrap, total_output

def get_shift_length(workstation, from_date, to_date):
	duration_list = frappe.get_all("Shift Log", filters={"workstation": workstation, "date": ["between", [from_date, to_date]]}, fields=["duration"])
	duration = sum(float(log['duration']) for log in duration_list if log['duration'] is not None)
	return duration

def get_data(sites, from_date, to_date):
	data = []
	workstations = []
	for site in sites:
		workstations += frappe.get_all("Workstation", filters={"site": site})

	for workstation in workstations:
		workstation = frappe.get_doc("Workstation", workstation.name)
		total_time = get_total_time(from_date, to_date)
		schedule_loss, planned_downtime, unplanned_downtime = get_downtime_losses(workstation.name, from_date, to_date)
		pcc, output, scrap, total_output = get_manufacturing_data(workstation.name, from_date, to_date)
		
		shift_length = get_shift_length(workstation.name, from_date, to_date)

		planned_production_time = shift_length - planned_downtime

		run_time = shift_length - planned_downtime - unplanned_downtime
		
		run_time_in_minutes = run_time / 60
		
		utilization = ((planned_production_time) / total_time)*100 if total_time else 0

		availability = ((run_time) / (planned_production_time))*100 if planned_production_time else 0

		performance = ((total_output / run_time_in_minutes) / pcc)*100 if pcc and run_time_in_minutes else 0
		
		quality = (output / total_output)*100 if total_output else 0

		oee = availability * performance * quality / 10000 if availability and performance and quality else 0

		teep = (oee * utilization)/100 if oee and utilization else 0

		data.append({
			"workstation": workstation.name,
			"total_time": total_time,
			"shift_duration": shift_length,
			"planned_downtime": planned_downtime,
			"unplanned_downtime": unplanned_downtime,
			"planned_production_time": planned_production_time,
			"run_time": run_time,
			"utilization": utilization,
			"availability": availability,
			"output": output,
			"scrap": scrap,
			"total_output": total_output,
			"ideal_cycle_time": pcc,
			"performance": performance,
			"quality": quality,
			"oee": oee,
			"teep": teep
		})
	return data