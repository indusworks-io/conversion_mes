# Copyright (c) 2024, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now, time_diff_in_seconds
from frappe.model.document import Document

class ManufacturingOrder(Document):
	def before_save(self):
		# Update Alternate Quantity for each row In planned_output table based on conversion factor
		for item in self.planned_output:
			item.alternate_quantity = item.quantity * item.conversion_factor

		# Update Planned Output Total Quantities
		self.total_planned_output_quantity_in_default_uom = sum([item.quantity for item in self.planned_output])
		self.total_planned_output_quantity_in_alternate_uom = sum([item.alternate_quantity for item in self.planned_output])

		# Update Duration Feild In Time Logs Table && Actual Duration
		self.actual_duration = 0
		if self.time_logs:
			for time_log in self.time_logs:
				start = time_log.start_time
				end = time_log.end_time
				if end is None:
					time_log.duration = time_diff_in_seconds(now(), start)
					self.actual_duration += time_log.duration
				else:
					time_log.duration = time_diff_in_seconds(end, start)
					self.actual_duration += time_log.duration
		
		# Update Batch/Serial Number Summary
		self.batch_serial_number_summary = []
		for batch_serial_log in self.batch_serial_logs:
			self.append('batch_serial_number_summary', {
				'serial_batch_number': batch_serial_log.batch_serial_number
			})
		
		# Update Alternate Quantity In Output Logs
		for output_log in self.output_logs:
			output_log.alternate_quantity = output_log.quantity*output_log.conversion_factor

		# Update Actual Output Summary. If the output item appears more than once, add the quantities. append to actual_output_summary and calculate the total output quantity.
		self.actual_output_summary = []
		for output_log in self.output_logs:
			output_item = output_log.item
			output_quantity = output_log.quantity
			output_uom = output_log.uom
			output_conversion_factor = output_log.conversion_factor
			found = False
			for item in self.actual_output_summary:
				if item.item == output_item:
					item.quantity += output_quantity
					item.alternate_quantity += output_quantity * output_conversion_factor
					found = True
					break
			if not found:
				self.append('actual_output_summary', {
					'item': output_item,
					'quantity': output_quantity,
					'uom': output_uom,
					'conversion_factor': output_conversion_factor,
					'alternate_quantity': output_quantity * output_conversion_factor,
					'alternate_uom': output_log.alternate_uom
				})

		# Update Alternate Quantity In Scrap Logs
		for scrap_log in self.scrap_logs:
			scrap_log.alternate_quantity = scrap_log.quantity*scrap_log.conversion_factor
		
		# Update Actual Scrap Summary. If the scrapped item appears more than once, add the quantities. append to actual_scrap_summary and calculate the total scrapped quantity.
		self.actual_scrap_summary = []
		for scrap_log in self.scrap_logs:
			scrap_item = scrap_log.item
			scrap_quantity = scrap_log.quantity
			scrap_uom = scrap_log.uom
			scrap_conversion_factor = scrap_log.conversion_factor
			found = False
			for item in self.actual_scrap_summary:
				if item.item == scrap_item:
					item.quantity += scrap_quantity
					item.alternate_quantity += scrap_quantity * scrap_conversion_factor
					found = True
					break
			if not found:
				self.append('actual_scrap_summary', {
					'item': scrap_item,
					'quantity': scrap_quantity,
					'uom': scrap_uom,
					'conversion_factor': scrap_conversion_factor,
					'alternate_quantity': scrap_quantity * scrap_conversion_factor,
					'alternate_uom': scrap_log.alternate_uom
				})
		
		# Update Actual Input, Output & Scrap Quantities
		self.total_actual_output_quantity_in_default_uom = 0
		self.total_actual_output_quantity_in_alternate_uom = 0
		self.total_actual_scrap_quantity_in_default_uom = 0
		self.total_actual_scrap_quantity_in_alternate_uom = 0
		
		if self.actual_output_summary:
			self.total_actual_output_quantity_in_default_uom = sum([item.quantity for item in self.actual_output_summary])
			self.total_actual_output_quantity_in_alternate_uom = sum([item.alternate_quantity for item in self.actual_output_summary])
		
		if self.actual_scrap_summary:
			self.total_actual_scrap_quantity_in_default_uom = sum([item.quantity for item in self.actual_scrap_summary])
			self.total_actual_scrap_quantity_in_alternate_uom = sum([item.alternate_quantity for item in self.actual_scrap_summary])