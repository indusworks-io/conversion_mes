import frappe
from frappe.utils import now, nowdate, nowtime, get_timedelta
from datetime import datetime
import requests

### WORKSTATION APPLICATION RELATED API ENDPOINTS ###
@frappe.whitelist()
def get_operators(workstation):
    try:
        Workstation = frappe.get_doc("Workstation", workstation)
        operators = []
        for operator in Workstation.operators:
            operators.append(operator.operator)
        return operators
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Operators Error")


@frappe.whitelist()
def start_order(order_name, operator):
    try:
        order = frappe.get_doc("Manufacturing Order", order_name)
        if order.status == 'Not Started':
            order.status = 'In Progress'
            order.actual_start_date_time = now()
            time_log = order.append('time_logs', {})
            time_log.operator = operator
            time_log.start_time = now()
            order.save(ignore_permissions=True)
            frappe.db.commit()
            return {
                'status': True,
                'status_code': 200,
                'message': 'Order Started Sucessfully',
                'data': order
            }
        elif order.status == 'In Progress':
            return {
                'status': False,
                'status_code': 400,
                'message': 'Order Already Started',
                'data': order
            }
        elif order.status == 'Completed':
            return {
                'status': False,
                'status_code': 400,
                'message': 'Order Already Completed',
                'data': order
            }
        elif order.status == 'Stopped':
            order.status = 'In Progress'
            time_log = order.append('time_logs', {})
            time_log.operator = operator
            time_log.start_time = now()
            order.save(ignore_permissions=True)
            frappe.db.commit()
            return {
                'status': True,
                'status_code': 200,
                'message': 'Order Started Sucessfully',
                'data': order
            }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Start Order Error")
        return str(e)

@frappe.whitelist()
def stop_order(order_name):
    try:
        order = frappe.get_doc("Manufacturing Order", order_name)
        if order.status == 'In Progress':
            order.status = 'Stopped'
            time_log = order.time_logs[-1]
            time_log.end_time = now()
            time_log.duration = frappe.utils.time_diff_in_seconds(time_log.end_time, time_log.start_time)
            order.save(ignore_permissions=True)
            frappe.db.commit()
            return {
                'status': True,
                'status_code': 200,
                'message': 'Order Stopped Sucessfully',
                'data': order
            }
        elif order.status == 'Not Started':
            return {
                'status': False,
                'status_code': 400,
                'message': 'Order Not Started',
                'data': order
            }
        elif order.status == 'Stopped':
            return {
                'status': False,
                'status_code': 400,
                'message': 'Order Already Stopped',
                'data': order
            }
        elif order.status == 'Completed':
            return {
                'status': False,
                'status_code': 400,
                'message': 'Order Already Completed',
                'data': order
            }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Stop Order Error")
        return str(e)

@frappe.whitelist()
def complete_order(order_name):
    try:
        order = frappe.get_doc("Manufacturing Order", order_name)
        if order.status == 'Not Started':
            return {
                'status': False,
                'status_code': 400,
                'message': 'Order Not Started',
                'data': order
            }
        elif order.status == 'In Progress':
            order.status = 'Completed'
            order.actual_end_date_time = now()
            time_log = order.time_logs[-1]
            time_log.end_time = now()
            time_log.duration = frappe.utils.time_diff_in_seconds(time_log.end_time, time_log.start_time)
            order.save(ignore_permissions=True)
            frappe.db.commit()
            return {
                'status': True,
                'status_code': 200,
                'message': 'Order Completed Sucessfully',
                'data': order
            }
        elif order.status == 'Stopped':
            order.status = 'Completed'
            order.actual_end_date_time = now()
            order.save(ignore_permissions=True)
            frappe.db.commit()
            print("this code block executed")
            return {
                'status': True,
                'status_code': 200,
                'message': 'Order Completed Sucessfully',
                'data': order
            }
        elif order.status == 'Completed':
            return {
                'status': False,
                'status_code': 400,
                'message': 'Order Already Completed',
                'data': order
            }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Stop Error")
        return str(e)

@frappe.whitelist()
def log_batch_serial_number(order_name, operator, batch_serial_number):
    try:
        order = frappe.get_doc("Manufacturing Order", order_name)
        batch_serial_log = order.append('batch_serial_logs', {})
        batch_serial_log.operator = operator
        batch_serial_log.timestamp = now()
        batch_serial_log.batch_serial_number = batch_serial_number
        order.save(ignore_permissions=True)
        frappe.db.commit()
        return {
            'status': True,
            'status_code': 200,
            'message': 'Batch/Serial Number Logged Sucessfully',
            'data': order
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Log Serial & Batch Error")
        return str(e)

@frappe.whitelist()
def log_cycles(order_name, operator, cycle_count):
    try:
        order = frappe.get_doc("Manufacturing Order", order_name)
        cycle_log = order.append('cycle_logs', {})
        cycle_log.operator = operator
        cycle_log.timestamp = now()
        cycle_log.cycles = int(cycle_count)
        order.save(ignore_permissions=True)
        frappe.db.commit()
        return {
            'status': True,
            'status_code': 200,
            'message': 'Cycle Count Logged Sucessfully',
            'data': order
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Log Cycle Error")
        return str(e)

@frappe.whitelist()
def log_output(order_name, operator, item, quantity):
    try:
        order = frappe.get_doc("Manufacturing Order", order_name)
        output_log = order.append('output_logs', {})
        output_log.operator = operator
        output_log.timestamp = now()
        output_log.item = item
        output_log.quantity = int(quantity)
        order.save(ignore_permissions=True)
        frappe.db.commit()
        return {
            'status': True,
            'status_code': 200,
            'message': 'Output Logged Sucessfully',
            'data': order
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Log Output Error")
        return str(e)

@frappe.whitelist()
def log_scrap(order_name, operator, item, quantity):
    try:
        order = frappe.get_doc("Manufacturing Order", order_name)
        scrap_log = order.append('scrap_logs', {})
        scrap_log.operator = operator
        scrap_log.timestamp = now()
        scrap_log.item = item
        scrap_log.quantity = int(quantity)
        order.save(ignore_permissions=True)
        frappe.db.commit()
        return {
            'status': True,
            'status_code': 200,
            'message': 'Scrap Logged Sucessfully',
            'data': order
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Log Scrap Error")
        return str(e)

@frappe.whitelist()
def get_downtime_reasons():
    try:
        reasons = []
        downtime_reasons = frappe.get_all('Downtime Reason', filters={"is_active": 1,"show_to_operator": 1})
        for downtime_reason in downtime_reasons:
            reasons.append(downtime_reason.name)
        return {
            'status': True,
            'status_code': 200,
            'message': 'Got Reasons Sucessfully',
            'data': reasons
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Downtime Reason Error")
        return str(e)

@frappe.whitelist()
def update_downtime_reason(downtime_name, downtime_reason):
    try:
        downtime = frappe.get_doc("Downtime Log", downtime_name)
        downtime.reason = downtime_reason
        downtime.save(ignore_permissions=True)
        return{
            'status': True,
            'status_code': 200,
            'message': 'Downtime Reason Updated',
            'data': downtime
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Update Downtime Reason Error")
        return str(e)


### DOWNTIME REALTED API ENDPOINTS ###

@frappe.whitelist(allow_guest=True)
def get_configuration(device_name):
    """
    This function needs to provide following data:
    1. from Device DocType: workstation, heartbeat_threshold
    2. from Workstation DocType: workstation_name, idle_current_threshold, idle_time_threshold
    3. from shift Log DocType: Shifts
    4. from Downtime Log DocType: Open Downtime & Closed Downtime
    """
    try:

        workstation, heartbeat_threshold = frappe.get_value("Device", device_name, ["workstation", "heartbeat_threshold"])
        
        idle_current_threshold, idle_time_threshold = frappe.get_value("Workstation", workstation, ["idle_current_threshold", "idle_time_threshold"])
        
        Date = nowdate()
        shifts = []
        shift_logs = frappe.get_all("Shift Log", filters={"workstation": workstation, "date": Date}, fields=["start_time", "end_time"])
        for log in shift_logs:
            shifts.append({"start_time": log["start_time"], "end_time": log["end_time"]})
        
        open_downtime_logs = frappe.get_all("Downtime Log", filters={"workstation": workstation, "status": "Open"}, fields=["name"])
        open_downtime = None
        if open_downtime_logs:
            open_downtime = open_downtime_logs[0]['name']
            
        
        closed_downtime_logs = frappe.get_all("Downtime Log", filters={"workstation": workstation, "status": "Closed", "created_date": Date}, fields=["start_date_time", "end_date_time"])
        
        closed_downtimes = None

        if closed_downtime_logs:
            closed_downtimes = []
            for log in closed_downtime_logs:
                closed_downtimes.append({
                    "start_date_time": log["start_date_time"].strftime('%Y-%m-%d %H:%M:%S'),
                    "end_date_time": log["end_date_time"].strftime('%Y-%m-%d %H:%M:%S')
                })
            
        
        return {
            "workstation_name": workstation,
            "heartbeat_threshold": heartbeat_threshold,
            "idle_current_threshold": idle_current_threshold,
            "idle_time_threshold": idle_time_threshold,
            "shifts": shifts,
            "open_downtime": open_downtime,
            "closed_downtimes": closed_downtimes
        }
        
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Configuration Error")
        return str(e)





@frappe.whitelist()
def get_configuration_data(device_name):
    try:
        ct_sensitivity, workstation, heartbeat_threshold = frappe.get_value("Device", device_name, ["ct_sensitivity", "workstation", "heartbeat_threshold"])
        idle_current_threshold, idle_time_threshold = frappe.get_value("Workstation", workstation, ["idle_current_threshold", "idle_time_threshold"])
        configuration_data = {
            "ct_sensitivity": ct_sensitivity,
            "workstation_name": workstation,
            "idle_current_threshold": idle_current_threshold,
            "idle_time_threshold": idle_time_threshold,
            "heartbeat_threshold": heartbeat_threshold
        }
        return configuration_data
    except Exception as e:
        return str(e)


@frappe.whitelist()
def get_shifts(workstation_name):
    try:
        Date = nowdate()

        shifts = []

        # Fetch Shift Logs
        shift_logs = frappe.get_all("Shift Log",
            filters={"workstation": workstation_name, "date": Date},
            fields=["start_time", "end_time"]
        )

        # Add shift periods
        for log in shift_logs:
            shifts.append({"start_time": log["start_time"], "end_time": log["end_time"]})

        return shifts
    except Exception as e:
        return str(e)



@frappe.whitelist()
def get_open_downtime(workstation_name):
    try:
        downtime = frappe.get_all("Downtime Log", filters={"workstation": workstation_name, "status": "Open"}, fields=["name"])
        if downtime:
            return downtime[0]['name']
        else:
            return None
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


## TO DO ##
@frappe.whitelist(allow_guest=True)
def get_closed_downtime(workstation_name):
    try:
        Today = nowdate()
        downtime = frappe.get_all("Downtime Log", filters={"workstation": workstation_name, "status": "Closed", "created_date": Today}, fields=["*"])
        if downtime:
            return downtime
        else:
            return None
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }




@frappe.whitelist()
def create_downtime(workstation_name):
    try:
        downtime = frappe.new_doc("Downtime Log")
        downtime.status = "Open"
        downtime.created_date = nowdate()
        downtime.workstation = workstation_name
        downtime.start_date_time = now()
        downtime.save(ignore_permissions=True)
        return downtime
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Downtime Error")
        return {
            "status": "error",
            "message": str(e)
        }



@frappe.whitelist()
def close_downtime(downtime_name):
    try:
        downtime = frappe.get_doc("Downtime Log", downtime_name)
        downtime.end_date_time = now()
        downtime.duration = frappe.utils.time_diff_in_seconds(downtime.end_date_time, downtime.start_date_time)
        downtime.status = "Closed"
        workstation = frappe.get_doc("Workstation", downtime.workstation)
        if workstation.auto_update_minor_stops:
            if downtime.duration <= int(workstation.minor_stop_threshold):
                downtime.reason = workstation.minor_stop_downtime_reason
        downtime.save(ignore_permissions=True)
        frappe.db.commit()
        return downtime
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Close Downtime Error")
        return {
            "status": "error",
            "message": str(e)
        }




@frappe.whitelist()
def create_telemetry(device_id, current):
    try:
        telemetry = frappe.new_doc("Telemetry")
        telemetry.device = device_id
        telemetry.value = float(current)
        telemetry.timestamp = now()
        telemetry.save(ignore_permissions=True)
        frappe.db.commit()
        return telemetry
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Create Telemetry Error")
        return {
            "status": "error",
            "message": str(e)
        }


@frappe.whitelist()
def device_offline_event():
    try:
        devices = frappe.get_all("Device", fields=["*"])
        for device in devices:
            device_id = device['name']
            last_telemetry = frappe.get_all("Telemetry", filters={"device": device_id}, fields=["timestamp"], order_by="timestamp desc", limit=1)
            if last_telemetry:
                last_telemetry_timestamp = last_telemetry[0]['timestamp']
                now_timestamp = datetime.strptime(now(), '%Y-%m-%d %H:%M:%S.%f')
                if (now_timestamp - last_telemetry_timestamp).seconds > 60 * 60:
                    event = frappe.new_doc("Device Alert")
                    event.device_id = device_id
                    event.timestamp = now()
                    event.assigned_to = device.supervisor
                    event.insert(ignore_permissions=True)
            else:
                event = frappe.new_doc("Device Alert")
                event.device_id = device_id
                event.timestamp = now()
                event.assigned_to = device.supervisor
                event.insert(ignore_permissions=True)
    except:
        frappe.log_error(frappe.get_traceback(), "Device Offline Event Error")
        return {
            "status": "error",
            "message": str(e)
        }
