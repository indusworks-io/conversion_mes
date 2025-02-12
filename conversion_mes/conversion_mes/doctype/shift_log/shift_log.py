# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now, time_diff_in_seconds, add_days
from datetime import datetime

class ShiftLog(Document):
    def before_save(self):
        self.duration = 0
        if self.start_time and self.end_time:
            print(f"Start Time: {self.start_time}")
            print(f"End Time: {self.end_time}")
            start_datetime_str = f"{self.date} {self.start_time}"
            start_datetime = datetime.strptime(start_datetime_str, '%Y-%m-%d %H:%M:%S')
            end_datetime_str = f"{self.date} {self.end_time}"
            end_datetime = datetime.strptime(end_datetime_str, '%Y-%m-%d %H:%M:%S')
            
            if end_datetime < start_datetime:
                end_datetime = add_days(end_datetime, 1)
                self.duration = time_diff_in_seconds(end_datetime, start_datetime)
            else:
                self.duration = time_diff_in_seconds(end_datetime, start_datetime)