# Copyright (c) 2025, IndusWorks and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime


def execute(filters=None):
	sites = filters.get("site", [])
	workstations = filters.get("workstation", [])
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	columns, data = [], []

	columns = [
        {"fieldname": "downtime_reason", "label": "Downtime Reasons", "fieldtype": "Data", "width": 300},
        {"fieldname": "category", "label": "Category", "fieldtype": "Data", "width": 200},
        {"fieldname": "count", "label": "Count", "fieldtype": "Int", "width": 100},
        {"fieldname": "duration", "label": "Duration", "fieldtype": "Duration", "width": 200},
		{"fieldname": "average_duration", "label": "Average Duration", "fieldtype": "Duration", "width": 200}
    ]

	message = "Please select Site, Workstation, From Date and To Date to get the report."

	
	if not (sites and workstations and from_date and to_date):
		return columns, [], message
     
	data = get_downtime_summary(workstations, from_date, to_date)

	return columns, data


def get_downtime_summary(workstations, from_date, to_date):
    # Convert date strings to datetime objects
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%Y-%m-%d")

    # Fetch downtime logs filtered by the provided criteria
    downtime_logs = frappe.get_all(
        'Downtime Log',
        fields=["reason", "duration", "category"],
        filters={
            "workstation": ["in", workstations],
            "created_date": ["between", [from_date, to_date]]
        }
    )

	# Dictionary to aggregate downtime data by reason
    downtime_summary = {}

    for log in downtime_logs:
        category = log["category"] or "(Category Not Mentioned)"
        reason = log["reason"] or "(Reason Not Mentioned)"
        duration = log["duration"] or 0  # Default to 0 if no duration is recorded

        # Initialize the downtime reason entry if not present
        if reason not in downtime_summary:
            downtime_summary[reason] = {"count": 0, "total_duration": 0, "category": category}

        # Update count and total duration
        downtime_summary[reason]["count"] += 1
        downtime_summary[reason]["total_duration"] += duration
        downtime_summary[reason]["category"] = category

    # Prepare data for the report
    report_data = []
    for reason, summary in downtime_summary.items():
        avg_duration = summary["total_duration"] / summary["count"] if summary["count"] > 0 else 0

        # Add row data for each downtime reason
        report_data.append({
            "downtime_reason": reason,
            "category": summary["category"],
            "count": summary["count"],
            "duration": summary["total_duration"],
            "average_duration": avg_duration
        })

    return report_data