# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime

def execute(filters=None):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	columns = get_columns()
	data = get_data(from_date, to_date)
	return columns, data

def get_columns():
	return [
		{"fieldname": "site", "label": "Site", "fieldtype": "Link", "options": "Site", "width": 200},
		{"fieldname": "total_time", "label": "Total Time", "fieldtype": "Duration", "width": 150},
		{"fieldname": "schedule_loss", "label": "Schedule Loss", "fieldtype": "Duration", "width": 150},
		{"fieldname": "planned_downtime", "label": "Planned Downtime", "fieldtype": "Duration", "width": 150},
		{"fieldname": "planned_production_time", "label": "Planned Production Time", "fieldtype": "Duration", "width": 150},
		{"fieldname": "unplanned_downtime", "label": "Unplanned Downtime", "fieldtype": "Duration", "width": 150},
		{"fieldname": "run_time", "label": "Run Time", "fieldtype": "Duration", "width": 150},
		{"fieldname": "utilization", "label": "Utilization Percentage", "fieldtype": "Percent", "width": 150},
		{"fieldname": "availability", "label": "Availability Percentage", "fieldtype": "Percent", "width": 150},
		{"fieldname": "output", "label": "Output", "fieldtype": "Float", "width": 150},
		{"fieldname": "scrap", "label": "Scrap", "fieldtype": "Float", "width": 150},
		{"fieldname": "total_output", "label": "Total Output", "fieldtype": "Int", "width": 150},
		{"fieldname": "ideal_run_rate", "label": "Ideal Run Rate", "fieldtype": "Int", "width": 150},
		{"fieldname": "performance", "label": "Performance Percentage", "fieldtype": "Percent", "width": 150},
		{"fieldname": "quality", "label": "Quality", "fieldtype": "Percent", "width": 150},
		{"fieldname": "oee", "label": "OEE", "fieldtype": "Percent", "width": 150},
		{"fieldname": "teep", "label": "TEEP", "fieldtype": "Percent", "width": 150}
	]

def get_total_time(from_date, to_date):
	try:
		total_time = (datetime.strptime(to_date, "%Y-%m-%d") - datetime.strptime(from_date, "%Y-%m-%d")).total_seconds()
	except ValueError:
		total_time = 0  # Handle invalid dates gracefully
	return total_time

def get_downtime_losses(site, from_date, to_date):
	schedule_loss = 0
	planned_downtime = 0
	unplanned_downtime = 0
	
	downtime_logs = frappe.get_all("Downtime Log", filters={"site": site, "created_date": ["between", [from_date, to_date]]}, fields=["category", "duration"])

	for log in downtime_logs:
		duration = log['duration'] or 0
		if log['category'] == "Schedule Loss":
			schedule_loss += duration
		elif log['category'] == "Planned Downtime":
			planned_downtime += duration
		elif log['category'] == "Unplanned Downtime":
			unplanned_downtime += duration
	return schedule_loss, planned_downtime, unplanned_downtime

def get_manufacturing_data(site, from_date, to_date):
	manufacturing_orders = frappe.get_all("Manufacturing Order", filters={"site": site, "posting_date": ["between", [from_date, to_date]], "status":"Completed"}, fields=["planned_run_rate","total_actual_output_quantity_in_alternate_uom", "total_actual_scrap_quantity_in_alternate_uom",])

	output = 0
	scrap = 0
	total_output = 0
	weighed_count = 0

	for manufacturing_order in manufacturing_orders:
		output_quantity = manufacturing_order['total_actual_output_quantity_in_alternate_uom'] or 0
		scrap_quantity = manufacturing_order['total_actual_scrap_quantity_in_alternate_uom'] or 0
		total_quantity = output_quantity + scrap_quantity
		irr = manufacturing_order['planned_run_rate'] or 0
		output += output_quantity
		scrap += scrap_quantity
		total_output += total_quantity
		weighed_count += irr * total_output

	if total_output == 0:
		irr = 0
	else:
		irr = weighed_count / total_output

	return irr, output, scrap, total_output

def get_data(from_date, to_date):
	data = []
	sites = frappe.get_all("Site", filters={"is_active": 1})
	for site in sites:
		total_time = get_total_time(from_date, to_date)
		schedule_loss, planned_downtime, unplanned_downtime = get_downtime_losses(site.name, from_date, to_date)
		irr, output, scrap, total_output = get_manufacturing_data(site.name, from_date, to_date)
		planned_production_time = total_time - schedule_loss
		run_time = total_time - schedule_loss - planned_downtime - unplanned_downtime
		run_time_in_minutes = run_time / 60
		utilization = ((total_time - schedule_loss) / total_time)*100 if total_time else 0
		availability = ((total_time - schedule_loss - planned_downtime - unplanned_downtime) / (total_time - schedule_loss))*100 if total_time else 0
		performance = ((total_output / run_time_in_minutes) / irr)*100 if irr else 0
		quality = (output / total_output)*100 if total_output else 0
		oee = availability * performance * quality / 10000 if availability and performance and quality else 0
		teep = oee * utilization if oee and utilization else 0
		data.append({
			"workstation": site.name,
			"total_time": total_time,
			"schedule_loss": schedule_loss,
			"planned_downtime": planned_downtime,
			"unplanned_downtime": unplanned_downtime,
			"planned_production_time": planned_production_time,
			"run_time": run_time,
			"utilization": utilization,
			"availability": availability,
			"output": output,
			"scrap": scrap,
			"total_output": total_output,
			"ideal_run_rate": irr,
			"performance": performance,
			"quality": quality,
			"oee": oee,
			"teep": teep
		})
	return data