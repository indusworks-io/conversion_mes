# Copyright (c) 2024, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now, time_diff_in_seconds
from frappe.model.document import Document

class ManufacturingOrder(Document):
	def before_save(self):
		# Update Alternate Quantity In Planned Input Table
		for row in self.planned_input:
			row.alternate_quantity = row.quantity * row.conversion_factor

		# Update Alternate Quantity In Planned Output Table
		for row in self.planned_output:
			row.alternate_quantity = row.quantity * row.conversion_factor

		# Update Total Planned Input Quantity in Default UOM
		self.total_planned_input_quantity_in_default_uom = sum([row.quantity for row in self.planned_input])

		# Update Total Planned Input Quantity in Alternate UOM
		self.total_planned_input_quantity_in_alternate_uom = sum([row.alternate_quantity for row in self.planned_input])

		# Update Total Planned Output Quantity in Default UOM
		self.total_planned_output_quantity_in_default_uom = sum([row.quantity for row in self.planned_output])

		# Update Total Planned Output Quantity in Alternate UOM
		self.total_planned_output_quantity_in_alternate_uom = sum([row.alternate_quantity for row in self.planned_output])

		# Update Planned Duration
		self.planned_duration = self.planned_setup_time + ((self.total_planned_input_quantity_in_alternate_uom/self.planned_run_rate)*60)
		
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
		
		# Update actual_input_summary from input_logs
		self.total_actual_input_quantity_in_default_uom = 0
		self.total_actual_input_quantity_in_alternate_uom = 0
		self.actual_input_summary = []
		for input_log in self.input_logs:
			input_log.alternate_quantity = input_log.quantity * input_log.conversion_factor
			input_item = input_log.item
			input_quantity = input_log.quantity
			uom = input_log.uom
			conversion_factor = input_log.conversion_factor
			alternate_quantity = input_log.alternate_quantity
			alternate_uom = input_log.alternate_uom
			batch_number = input_log.batch_number
			found = False
			for summary in self.actual_input_summary:
				if (summary.item == input_item and summary.batch_number == batch_number):
					summary.quantity += input_quantity
					summary.alternate_quantity += alternate_quantity
					found = True
					break
			if not found:
				self.append('actual_input_summary', {
					'item': input_item,
					'quantity': input_quantity,
					'uom': uom,
					'conversion_factor': conversion_factor,
					'alternate_quantity': alternate_quantity,
					'alternate_uom': alternate_uom,
					'batch_number': batch_number
				})
			self.total_actual_input_quantity_in_default_uom += input_quantity
			self.total_actual_input_quantity_in_alternate_uom += alternate_quantity

		# Update Actual Output Summary from Output Logs
		self.total_actual_output_quantity_in_default_uom = 0
		self.total_actual_output_quantity_in_alternate_uom = 0
		self.actual_output_summary = []
		for output_log in self.output_logs:
			output_log.alternate_quantity = output_log.quantity * output_log.conversion_factor
			output_item = output_log.item
			output_quantity = output_log.quantity
			uom = output_log.uom
			conversion_factor = output_log.conversion_factor
			alternate_quantity = output_log.alternate_quantity
			alternate_uom = output_log.alternate_uom
			batch_number = output_log.batch_number
			found = False
			for summary in self.actual_output_summary:
				if (summary.item == output_item and summary.batch_number == batch_number):
					summary.quantity += output_quantity
					summary.alternate_quantity += alternate_quantity
					found = True
					break
			if not found:
				self.append('actual_output_summary', {
					'item': output_item,
					'quantity': output_quantity,
					'uom': uom,
					'conversion_factor': conversion_factor,
					'alternate_quantity': alternate_quantity,
					'alternate_uom': alternate_uom,
					'batch_number': batch_number
				})
			self.total_actual_output_quantity_in_default_uom += output_quantity
			self.total_actual_output_quantity_in_alternate_uom += alternate_quantity


		# Update Run Rate
		if self.actual_duration != 0:
			self.actual_run_rate = (self.total_actual_input_quantity_in_alternate_uom/self.actual_duration)*60