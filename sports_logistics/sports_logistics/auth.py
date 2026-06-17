import frappe


def on_login(login_manager):
    """عند تسجيل الدخول — ربط المستخدم بـ SL Employee وتحديد وجهته"""
    user = login_manager.user

    # تجاهل حساب Administrator
    if user == "Administrator":
        return

    # البحث عن SL Employee بنفس البريد
    employee = frappe.db.get_value(
        "SL Employee",
        {"email": user},
        ["name", "user_role", "full_name_ar"],
        as_dict=True
    )

    if not employee:
        return

    # التأكد من أن المستخدم لديه الدور الصحيح
    user_doc = frappe.get_doc("User", user)
    current_roles = [r.role for r in user_doc.roles]

    role_map = {
        "Employee":     "Employee",
        "Line Manager": "Line Manager",
        "Logistics":    "Logistics",
        "Finance":      "Finance",
        "MD":           "MD",
        "Admin":        "System Manager",
    }

    target_role = role_map.get(employee.user_role)

    if target_role and target_role not in current_roles:
        user_doc.append("roles", {"role": target_role})
        user_doc.save(ignore_permissions=True)
        frappe.db.commit()
