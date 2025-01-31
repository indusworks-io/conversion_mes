# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, time_diff_in_seconds, add_days

class ShiftLog(Document):
	def before_save(self):
		self.duration = 0
		if self.start_time and self.end_time:
			start_datetime = f"{self.date} {self.start_time}"
			end_datetime = f"{self.date} {self.end_time}"

            # If end time is earlier than start time, assume it's on the next day
			if self.end_time < self.start_time:
				end_datetime = f"{add_days(self.date, 1)} {self.end_time}"
            
			self.duration = time_diff_in_seconds(end_datetime, start_datetime)