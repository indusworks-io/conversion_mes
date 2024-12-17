# Copyright (c) 2024, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Workstation(Document):
	def before_save(self):
		self.total_operating_cost = self.land_cost + self.labor_cost + self.energy_cost + self.other_cost