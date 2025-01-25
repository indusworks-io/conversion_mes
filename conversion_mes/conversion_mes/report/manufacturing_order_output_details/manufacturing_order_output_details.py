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
			'fieldname': 'operation',
			'label': ('Operation'),
			'fieldtype': 'Link',
			'options': 'Operation',
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
			'label': ('Item'),
			'fieldtype': 'Link',
			'options': 'Item',
			"width": 300
		},
		{
			'fieldname': 'quantity',
			'label': ('Quantity'),
			'fieldtype': 'Int',
			"width": 100
		},
		{
			'fieldname': 'uom',
			'label': ('UOM'),
			'fieldtype': 'Link',
			'options': 'UOM',
			"width": 100
		},
		{
			'fieldname': 'alternate_quantity',
			'label': ('Alternate Quantity'),
			'fieldtype': 'Float',
			"width": 100
		},
		{
			'fieldname': 'alternate_uom',
			'label': ('Alternate UOM'),
			'fieldtype': 'Link',
			'options': 'UOM',
			"width": 100
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
		for row in manufacturing_order.actual_output_summary:
			data.append({
				"posting_date": manufacturing_order.posting_date,
				"name": manufacturing_order.name,
				"site": manufacturing_order.site,
				"workstation": manufacturing_order.workstation,
				"program": manufacturing_order.operation,
				"status": manufacturing_order.status,
				"item": row.item,
				"quantity": row.quantity,
				"uom": row.uom,
				"alternate_quantity": row.alternate_quantity,
				"alternate_uom": row.alternate_uom
			})
		data.append({
			"posting_date": manufacturing_order.posting_date,
			"name": manufacturing_order.name,
			"site": manufacturing_order.site,
			"workstation": manufacturing_order.workstation,
			"operation": manufacturing_order.operation,
			"status": manufacturing_order.status,
			"item": manufacturing_order.scrap_item_code,
			"quantity": manufacturing_order.total_actual_scrap_quantity_in_default_uom,
			"uom": manufacturing_order.scrap_uom,
			"alternate_quantity": manufacturing_order.total_actual_scrap_quantity_in_alternate_uom,
			"alternate_uom": manufacturing_order.scrap_alternate_uom
		})
	return data