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
		for time_log in self.time_logs:
			start = time_log.start_time
			end = time_log.end_time
			if end is None:
				time_log.duration = time_diff_in_seconds(now(), start)
				self.actual_duration += time_log.duration
			else:
				time_log.duration = time_diff_in_seconds(end, start)
				self.actual_duration += time_log.duration

		# Update Total Actual Input Quantity in Default UOM

		# Update Total Actual Input Quantity in Alternate UOM

		# Update Total Actual Output Quantity in Default UOM

		# Update Total Actual Output Quantity in Alternate UOM

		# Update Run Rate