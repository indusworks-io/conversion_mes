// Copyright (c) 2025, IndusWorks and contributors
// For license information, please see license.txt

frappe.query_reports["Workstation Wise KPI Analysis"] = {
	"filters": [
		{
			"fieldname": "site",
			"label": __("Site"),
			"fieldtype": "MultiSelectList",
			"get_data": function(txt) {return frappe.db.get_link_options("Site", txt);},
			"reqd": 1,
			"on_change": function() {
				let selected_sites = frappe.query_report.get_filter_value("site");
				if (!selected_sites || selected_sites.length === 0) {
					frappe.query_report.set_filter_value("site", []);
				}
			}
		},
		{
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_days(frappe.datetime.get_today(), -30),
            "reqd": 1
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1
        }
	]
};
