import frappe


def _get_user_employee(user=None):
    user = user or frappe.session.user
    employee = frappe.db.get_value("SL Employee", {"email": user}, "name")
    return employee


def _is_privileged():
    privileged_roles = {"MD", "Logistics", "Line Manager", "Finance", "System Manager"}
    return bool(privileged_roles.intersection(set(frappe.get_roles())))


def get_travel_request_conditions(user):
    if _is_privileged():
        return ""
    employee = _get_user_employee(user)
    if not employee:
        return "1=0"
    return f"`tabSL Travel Request`.requester = '{employee}'"


def get_clearance_conditions(user):
    if _is_privileged():
        return ""
    employee = _get_user_employee(user)
    if not employee:
        return "1=0"
    return f"`tabSL Custom Clearance`.requester = '{employee}'"


def get_visa_conditions(user):
    if _is_privileged():
        return ""
    employee = _get_user_employee(user)
    if not employee:
        return "1=0"
    return f"`tabSL Government Visas`.requester = '{employee}'"


def get_leave_conditions(user):
    if _is_privileged():
        return ""
    employee = _get_user_employee(user)
    if not employee:
        return "1=0"
    return f"`tabSL Leave Letters`.requester = '{employee}'"


def get_inventory_conditions(user):
    if _is_privileged():
        return ""
    employee = _get_user_employee(user)
    if not employee:
        return "1=0"
    return f"`tabSL Inventory Requests`.requester = '{employee}'"


def get_facility_conditions(user):
    if _is_privileged():
        return ""
    employee = _get_user_employee(user)
    if not employee:
        return "1=0"
    return f"`tabSL Facility Bookings`.requester = '{employee}'"
