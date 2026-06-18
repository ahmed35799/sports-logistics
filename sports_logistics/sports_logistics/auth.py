import frappe

ROLE_WORKSPACE = {
    "Employee": "SL Employee",
    "Line Manager": "SL Line Manager",
    "MD": "SL MD",
    "Logistics": "SL Logistics",
}

def on_login(login_manager):
    user = login_manager.user
    roles = frappe.get_roles(user)
    import json
    for role, workspace in ROLE_WORKSPACE.items():
        if role in roles:
            frappe.db.sql(
                "UPDATE `tabUser` SET home_settings = %s WHERE name = %s",
                (json.dumps({"workspace": workspace}), user),
                auto_commit=True
            )
            break

def has_employee_permission():
    return "Employee" in frappe.get_roles()

def has_line_manager_permission():
    return "Line Manager" in frappe.get_roles()

def has_md_permission():
    return "MD" in frappe.get_roles()

def has_logistics_permission():
    return "Logistics" in frappe.get_roles()
