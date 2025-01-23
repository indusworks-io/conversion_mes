# Copyright (c) 2024, IndusWorks and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Operation(Document):
	def before_save(self):
		for row in self.input_items:
			row.alternate_quantity = row.quantity * row.conversion_factor
		
		for row in self.output_items:
			row.alternate_quantity = row.quantity * row.conversion_factor