# Copyright (c) 2024, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.utils import now, time_diff_in_seconds
from frappe.model.document import Document

class ManufacturingOrder(Document):
	def before_save(self):

		# Validate If Work Order Is Open
		if self.work_orders:
			for work_order_number in self.work_orders:
				work_order = frappe.get_doc("Work Order", work_order_number)
				if work_order.status == "Draft":
					frappe.throw(f"{work_order.name} status is Draft. Please Change the status to open.")
				elif work_order.status == "Completed":
					frappe.throw(f"{work_order.name} has already been completed. Please select another work order.")
				elif work_order.status == "Cancelled":
					frappe.throw(f"{work_order.name} has been cancelled. Please select another work order.")
		
		# Validate If Work Orders Has Items Same As Planned Output
		if self.work_orders:
			for work_order_number in self.work_orders:
				work_order = frappe.get_doc("Work Order", work_order_number)
				work_order_item = work_order.item
				for output in self.planned_output:
					found = False
					if work_order_item == output.item:
						found = True
						break
					if not found:
						frappe.throw(f"Item {work_order_item} of {work_order.name} is not in the planned output items. Please check the planned output items and try again.")
		
		
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
		
		# Update Actual Output based on Cycles
		self.actual_output_summary = []
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
		
		# Subtract Scrap Quantity from Actual Output Summary. Add a Check That There Is Item In Actual Output Summary. Also if the scrap item is raw material then add the quantity to actual input summary.
		if self.actual_output_summary and self.actual_scrap_summary:
			for scrap in self.actual_scrap_summary:
				for output in self.actual_output_summary:
					if scrap.item == output.item:
						output.quantity -= scrap.quantity
						output.alternate_quantity -= scrap.alternate_quantity
						break
				for input in self.actual_input_summary:
					if scrap.item == input.item:
						input.quantity += scrap.quantity
						input.alternate_quantity += scrap.alternate_quantity
						break
		
		# Update Actual Input, Output & Scrap Quantities
		
		self.total_actual_input_quantity_in_default_uom = 0
		self.total_actual_input_quantity_in_alternate_uom = 0
		self.total_actual_output_quantity_in_default_uom = 0
		self.total_actual_output_quantity_in_alternate_uom = 0
		self.total_actual_scrap_quantity_in_default_uom = 0
		self.total_actual_scrap_quantity_in_alternate_uom = 0

		if self.actual_input_summary:
			self.total_actual_input_quantity_in_default_uom = sum([item.quantity for item in self.actual_input_summary])
			self.total_actual_input_quantity_in_alternate_uom = sum([item.alternate_quantity for item in self.actual_input_summary])
		
		if self.actual_output_summary:
			self.total_actual_output_quantity_in_default_uom = sum([item.quantity for item in self.actual_output_summary])
			self.total_actual_output_quantity_in_alternate_uom = sum([item.alternate_quantity for item in self.actual_output_summary])
		
		if self.actual_scrap_summary:
			self.total_actual_scrap_quantity_in_default_uom = sum([item.quantity for item in self.actual_scrap_summary])
			self.total_actual_scrap_quantity_in_alternate_uom = sum([item.alternate_quantity for item in self.actual_scrap_summary])
		
		# Update completed_quantity in Work Orders based on Actual Output Summary
		if self.work_orders and self.actual_output_summary:
			for work_order_number in self.work_orders:
				work_order = frappe.get_doc("Work Order", work_order_number)
				for output in self.actual_output_summary:
					if work_order.item == output.item:
						work_order.completed_quantity += output.quantity
						if work_order.completed_quantity > 0:
							work_order.status = "In Progress"
						if work_order.completed_quantity >= work_order.planned_quantity:
							work_order.status = "Completed"
						work_order.save()