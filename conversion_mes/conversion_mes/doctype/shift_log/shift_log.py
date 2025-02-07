# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, time_diff_in_seconds, add_days
from datetime import datetime

class ShiftLog(Document):
    def on_change(self):
        self.duration = 0
        if self.start_time and self.end_time:
            if self.start_time > self.end_time:
                print(f"Start Time: {self.start_time}")
                today = self.date
                tomorrow = add_days(today, 1)
                start_datetime_str = f"{today} {self.start_time}"
                end_datetime_str = f"{tomorrow} {self.end_time}"
                start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')
                end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S')
                self.duration = time_diff_in_seconds(end_datetime, start_datetime)
            else:
                start_datetime_str = f"{self.date} {self.start_time}"
                end_datetime_str = f"{self.date} {self.end_time}"
                start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')
                end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S')
                self.duration = time_diff_in_seconds(end_datetime, start_datetime)