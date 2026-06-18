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
    
    for role, workspace in ROLE_WORKSPACE.items():
        if role in roles:
            import json
            frappe.db.sql(
                "UPDATE `tabUser` SET home_settings = %s, default_app = %s WHERE name = %s",
                (json.dumps({"workspace": workspace}), "sports_logistics", user),
                auto_commit=True
            )
            frappe.local.response["home_page"] = "/desk/" + workspace.lower().replace(" ", "-")
            break
