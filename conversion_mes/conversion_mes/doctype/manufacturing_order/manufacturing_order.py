# Copyright (c) 2024, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now, time_diff_in_seconds
from frappe.model.document import Document

class ManufacturingOrder(Document):
	def before_save(self):

		# Update Planned Input & Output based on Operation and Cycles

		operation = frappe.get_doc("Operation", self.operation)
		cycles = self.planned_cycles

		input_items = operation.input_items
		self.planned_input = []
		for input_item in input_items:
			self.append('planned_input', {
				'item': input_item.item,
				'track_batch_serial_number': input_item.track_batch_serial_number,
				'quantity': input_item.quantity*cycles,
				'uom': input_item.uom,
				'conversion_factor': input_item.conversion_factor,
				'alternate_quantity': input_item.quantity*cycles*input_item.conversion_factor,
				'alternate_uom': input_item.alternate_uom
			})
		

		output_items = operation.output_items
		self.planned_output = []
		for output_item in output_items:
			self.append('planned_output', {
				'item': output_item.item,
				'quantity': output_item.quantity*cycles,
				'uom': output_item.uom,
				'conversion_factor': output_item.conversion_factor,
				'alternate_quantity': output_item.quantity*cycles*output_item.conversion_factor,
				'alternate_uom': output_item.alternate_uom
			})
		
		# Update Planned Input & Output Quantities
		self.total_planned_input_quantity_in_default_uom = sum([item.quantity for item in self.planned_input])

		self.total_planned_input_quantity_in_alternate_uom = sum([item.alternate_quantity for item in self.planned_input])

		self.total_planned_output_quantity_in_default_uom = sum([item.quantity for item in self.planned_output])

		self.total_planned_output_quantity_in_alternate_uom = sum([item.alternate_quantity for item in self.planned_output])

		# Update Planned Duration based on Planned Setup Time, Planned Cycle Time and Planned Cycles
		self.planned_duration = self.planned_setup_time + (self.planned_cycle_time * cycles)

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
		
		self.actual_cycles = 0
		for log in self.cycle_logs:
			self.actual_cycles += log.cycles

		self.actual_cycle_time = 0
		if self.actual_duration and self.actual_cycles:
			self.actual_cycle_time = self.actual_duration / self.actual_cycles
		
		# Update Batch/Serial Number Summary
		self.batch_serial_number_summary = []
		for batch_serial_log in self.batch_serial_logs:
			batch_serial_log.item
			batch_serial_log.batch_serial_number
			found = False
			for summary in self.batch_serial_number_summary:
				if (summary.item == batch_serial_log.item and summary.serial_batch_number == batch_serial_log.batch_serial_number):
					found = True
					break
			if not found:
				self.append('batch_serial_number_summary', {
					'item': batch_serial_log.item,
					'serial_batch_number': batch_serial_log.batch_serial_number
				})
		
		# Update Actual Input based on Cycles
		self.actual_input_summary = []
		self.total_actual_input_quantity_in_default_uom = 0
		self.total_actual_input_quantity_in_alternate_uom = 0
		if self.actual_cycles:
			for input_item in input_items:
				self.append('actual_input_summary', {
					'item': input_item.item,
					'quantity': input_item.quantity * self.actual_cycles,
					'uom': input_item.uom,
					'conversion_factor': input_item.conversion_factor,
					'alternate_quantity': input_item.quantity * self.actual_cycles * input_item.conversion_factor,
					'alternate_uom': input_item.alternate_uom
				})
				self.total_actual_input_quantity_in_default_uom += input_item.quantity * self.actual_cycles
				self.total_actual_input_quantity_in_alternate_uom += input_item.quantity * self.actual_cycles * input_item.conversion_factor
		
		# Update Actual Output based on Cycles
		self.actual_output_summary = []
		self.total_actual_output_quantity_in_default_uom = 0
		self.total_actual_output_quantity_in_alternate_uom = 0
		if self.actual_cycles:
			for output_item in output_items:
				self.append('actual_output_summary', {
					'item': output_item.item,
					'quantity': output_item.quantity * self.actual_cycles,
					'uom': output_item.uom,
					'conversion_factor': output_item.conversion_factor,
					'alternate_quantity': output_item.quantity * self.actual_cycles * output_item.conversion_factor,
					'alternate_uom': output_item.alternate_uom
				})
				self.total_actual_output_quantity_in_default_uom += output_item.quantity * self.actual_cycles
				self.total_actual_output_quantity_in_alternate_uom += output_item.quantity * self.actual_cycles * output_item.conversion_factor
		
		# Update Scrap Summary
		self.actual_scrap_summary = []
		self.total_actual_scrap_quantity_in_default_uom = 0
		self.total_actual_scrap_quantity_in_alternate_uom = 0
		for scrap_log in self.scrap_logs:
			scrap_item = scrap_log.item
			scrap_quantity = scrap_log.quantity
			scrap_alternate_quantity = scrap_log.alternate_quantity
			found = False
			
			