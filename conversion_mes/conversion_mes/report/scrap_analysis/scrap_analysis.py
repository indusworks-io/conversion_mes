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
			'fieldname': 'total_actual_output_quantity_in_default_uom',
			'label': ('Output Quantity'),
			'fieldtype': 'Int',
			"width": 150
		},
		{
			'fieldname': 'total_actual_scrap_quantity_in_default_uom',
			'label': ('Scrap Quantity'),
			'fieldtype': 'Int',
			"width": 150
		},
		{
			'fieldname': 'Scrap Percentage',
			'label': ('Scrap Percentage'),
			'fieldtype': 'Percent',
			"width": 150

		},		
		{
			'fieldname': 'total_actual_output_quantity_in_alternate_uom',
			'label': ('Output Quantity In Alternate UOM'),
			'fieldtype': 'Float',
			"width": 150
		},
		{
			'fieldname': 'total_actual_scrap_quantity_in_alternate_uom',
			'label': ('Scrap Quantity In Alternate UOM'),
			'fieldtype': 'Float',
			"width": 150
		},
		{
			'fieldname': 'Scrap Percentage In Alternate UOM',
			'label': ('Scrap Percentage In Alternate UOM'),
			'fieldtype': 'Percent',
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
		total_actual_output_quantity_in_default_uom = manufacturing_order.total_actual_output_quantity_in_default_uom
		total_actual_output_quantity_in_alternate_uom = manufacturing_order.total_actual_output_quantity_in_alternate_uom
		total_actual_scrap_quantity_in_default_uom = manufacturing_order.total_actual_scrap_quantity_in_default_uom
		total_actual_scrap_quantity_in_alternate_uom = manufacturing_order.total_actual_scrap_quantity_in_alternate_uom
		if total_actual_output_quantity_in_default_uom == 0:
			scrap_percentage = 0
		else:
			scrap_percentage = (total_actual_scrap_quantity_in_default_uom / total_actual_output_quantity_in_default_uom) * 100
		if total_actual_output_quantity_in_alternate_uom == 0:
			scrap_percentage_in_alternate_uom = 0
		else:
			scrap_percentage_in_alternate_uom = (total_actual_scrap_quantity_in_alternate_uom / total_actual_output_quantity_in_alternate_uom) * 100
		data.append({
			"site": manufacturing_order.site,
			"workstation": manufacturing_order.workstation,
			"posting_date": manufacturing_order.posting_date,
			"name": manufacturing_order.name,
			"status": manufacturing_order.status,
			"program": manufacturing_order.program,
			"total_actual_output_quantity_in_default_uom": total_actual_output_quantity_in_default_uom,
			"total_actual_output_quantity_in_alternate_uom": total_actual_output_quantity_in_alternate_uom,
			"total_actual_scrap_quantity_in_default_uom": total_actual_scrap_quantity_in_default_uom,
			"total_actual_scrap_quantity_in_alternate_uom": total_actual_scrap_quantity_in_alternate_uom,
			"Scrap Percentage": scrap_percentage,
			"Scrap Percentage In Alternate UOM": scrap_percentage_in_alternate_uom
		})
	return data