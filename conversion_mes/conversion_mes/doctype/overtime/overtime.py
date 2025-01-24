# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Overtime(Document):
	def on_change(self):
		# Based On the Overtime Workstation, Date & Duration we need to update the Downtime Log for the respective Workstation in which we change the start_date_time & end_date_time.
		# downtime_log = frappe.db.get_value("Downtime Log", {"workstation": self.workstation, "created_date": self.date})
		pass