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
			'fieldname': 'item',
			'label': ('Input Item'),
			'fieldtype': 'Link',
			'options': 'Item',
			"width": 300
		},
		{
			'fieldname': 'batch_serial_number',
			'label': ('Batch/Serial Number'),
			'fieldtype': 'Data',
			"width": 150
		}
	]


def get_manufacturing_orders(from_date, to_date):
	manufacturing_orders = frappe.get_all("Manufacturing Order", filters={"posting_date": ["between", [from_date, to_date]]})
	return manufacturing_orders


def get_data(from_date, to_date):
	manufacturing_orders = get_manufacturing_orders(from_date, to_date)
	data = []
	for manufacturing_order in manufacturing_orders:
		manufacturing_order = frappe.get_doc("Manufacturing Order", manufacturing_order.name)
		for row in manufacturing_order.batch_serial_number_summary:
			data.append({
				"posting_date": manufacturing_order.posting_date,
				"name": manufacturing_order.name,
				"site": manufacturing_order.site,
				"workstation": manufacturing_order.workstation,
				"program": manufacturing_order.program,
				"status": manufacturing_order.status,
				"item": row.item,
				"batch_serial_number": row.serial_batch_number
			})
	return data