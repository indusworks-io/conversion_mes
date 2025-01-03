# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	columns = get_columns()
	data = get_data(from_date, to_date)
	return columns, data

def get_columns():
	return[
		{
			'fieldname': 'site',
			'label': ('Site'),
			'fieldtype': 'Link',
			'options': 'Site',
			"width": 200
		},
		{
			'fieldname': 'workstation',
			'label': ('Workstation'),
			'fieldtype': 'Link',
			'options': 'Workstation',
			"width": 300
		},
		{
			'fieldname': 'created_date',
			'label': ('Created Date'),
			'fieldtype': 'Date',
			"width": 150
		},
		{
			'fieldname': 'name',
			'label': ('Downtime Log Number'),
			'fieldtype': 'Link',
			'options': 'Downtime Log',
			"width": 200
		},
		{
			'fieldname': 'status',
			'label': ('Status'),
			'fieldtype': 'Data',
			"width": 100
		},
		{
			'fieldname': 'start_date_time',
			'label': ('Start Date Time'),
			'fieldtype': 'Datetime',
			"width": 200
		},
		{
			'fieldname': 'end_date_time',
			'label': ('End Date Time'),
			'fieldtype': 'Datetime',
			"width": 200
		},
		{
			'fieldname': 'duration',
			'label': ('Duration In Minutes'),
			'fieldtype': 'duration',
			"width": 150
		},
		{
			'fieldname': 'reason',
			'label': ('Reason'),
			'fieldtype': 'Data',
			"width": 150
		},
		{
			'fieldname': 'category',
			'label': ('Category'),
			'fieldtype': 'Data',
			"width": 150
		}
	]

def get_downtime_logs(from_date, to_date):
	records = frappe.get_all('Downtime Log', fields=['*'], filters={"created_date": ["between", [from_date, to_date]]}, order_by="created_date ASC")
	return records

def get_data(from_date, to_date):
	records = get_downtime_logs(from_date, to_date)
	data = []
	for record in records:
		duration_in_minutes = round(record['duration'] / 60, 0) if record['duration'] is not None else 0
		data.append({
			'site': record['site'],
			'workstation': record['workstation'],
			'created_date': record['created_date'],
			'name': record['name'],
			'status': record['status'],
			'start_date_time': record['start_date_time'],
			'end_date_time': record['end_date_time'],
			'duration': duration_in_minutes,
			'reason': record['reason'],
			'category': record['category']
		})
	return data