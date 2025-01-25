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
			'fieldname': 'program',
			'label': ('Program'),
			'fieldtype': 'Link',
			'options': 'Program',
			"width": 150
		},
		{
			'fieldname': 'status',
			'label': ('Status'),
			'fieldtype': 'Data',
			"width": 100
		},
		{
			'fieldname': 'planned_duration',
			'label': ('Planned Duration'),
			'fieldtype': 'Duration',
			"width": 150
		},
		{
			'fieldname': 'actual_duration',
			'label': ('Actual Duration'),
			'fieldtype': 'Duration',
			"width": 150
		},
		{
			'fieldname': 'planned_cycle_time',
			'label': ('Planned Cycle Time'),
			'fieldtype': 'Duration',
			"width": 150
		},
		{
			'fieldname': 'actual_cycle_time',
			'label': ('Actual Cycle Time'),
			'fieldtype': 'Duration',
			"width": 150
		},
		{
			'fieldname': 'total_planned_output_quantity_in_default_uom',
			'label': ('Planned Output Quantity'),
			'fieldtype': 'Int',
			"width": 150
		},
		{
			'fieldname': 'total_actual_output_quantity_in_default_uom',
			'label': ('Actual Output Quantity'),
			'fieldtype': 'Int',
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
		row = {
			"posting_date": manufacturing_order.posting_date,
			"name": manufacturing_order.name,
			"site": manufacturing_order.site,
			"workstation": manufacturing_order.workstation,
			"program": manufacturing_order.program,
			"status": manufacturing_order.status,
			"planned_duration": manufacturing_order.planned_duration,
			"actual_duration": manufacturing_order.actual_duration,
			"total_planned_output_quantity_in_default_uom": manufacturing_order.total_planned_output_quantity_in_default_uom,
			"total_actual_output_quantity_in_default_uom": manufacturing_order.total_actual_output_quantity_in_default_uom,
			"planned_cycle_time": manufacturing_order.planned_cycle_time,
			"actual_cycle_time": manufacturing_order.actual_cycle_time
		}
		data.append(row)
	return data