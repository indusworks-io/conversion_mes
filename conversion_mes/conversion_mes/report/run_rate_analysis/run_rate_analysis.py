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
			"width": 150
		},
		{
			'fieldname': 'workstation',
			'label': ('Workstation'),
			'fieldtype': 'Link',
			'options': 'Workstation',
			"width": 150
		},
		{
			'fieldname': 'posting_date',
			'label': ('Posting Date'),
			'fieldtype': 'Date',
			"width": 150
		},
		{
			'fieldname': 'name',
			'label': ('Manufacturing Order'),
			'fieldtype': 'Link',
			'options': 'Manufacturing Order',
			"width": 200
		},
		{
			'fieldname': 'status',
			'label': ('Status'),
			'fieldtype': 'Data',
			"width": 100
		},
		{
			'fieldname': 'program',
			'label': ('Program'),
			'fieldtype': 'Link',
			'options': 'Program',
			"width": 150
		},
		{
			'fieldname': 'planned_run_rate',
			'label': ('Planned Run Rate'),
			'fieldtype': 'Int',
			"width": 150
		},
		{
			'fieldname': 'actual_run_rate',
			'label': ('Actual Run Rate'),
			'fieldtype': 'Int',
			"width": 150
		},
		{
			'fieldname': 'run_rate_variance',
			'label': ('Run Rate Variance'),
			'fieldtype': 'Int',
			"width": 150
		},
		{
			'fieldname': 'run_rate_variance_percentage',
			'label': ('Run Rate Variance Percentage'),
			'fieldtype': 'Percent',
			"width": 150
		},
	]

def get_manufacturing_orders(from_date, to_date):
	manufacturing_orders = frappe.get_all("Manufacturing Order", filters={"posting_date": ["between", [from_date, to_date]]})
	return manufacturing_orders


def get_data(from_date, to_date):
	manufacturing_orders = get_manufacturing_orders(from_date, to_date)
	data = []
	for manufacturing_order in manufacturing_orders:
		manufacturing_order = frappe.get_doc("Manufacturing Order", manufacturing_order.name)
		run_rate_variance = manufacturing_order.actual_run_rate - manufacturing_order.planned_run_rate
		run_rate_variance_percentage = (run_rate_variance / manufacturing_order.planned_run_rate) * 100
		row = {
			"site": manufacturing_order.site,
			"workstation": manufacturing_order.workstation,
			"posting_date": manufacturing_order.posting_date,
			"name": manufacturing_order.name,
			"status": manufacturing_order.status,
			"program": manufacturing_order.program,
			"planned_run_rate": manufacturing_order.planned_run_rate,
			"actual_run_rate": manufacturing_order.actual_run_rate,
			"run_rate_variance": run_rate_variance,
			"run_rate_variance_percentage": run_rate_variance_percentage,
		}
		data.append(row)
	return data