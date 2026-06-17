import frappe
from frappe import _
import secrets
import string


@frappe.whitelist()
def create_user_from_employee(employee_name):
    """إنشاء User من SL Employee"""

    # التحقق من الصلاحية
    if "System Manager" not in frappe.get_roles():
        frappe.throw(_("هذه العملية متاحة للمدير فقط"))

    employee = frappe.get_doc("SL Employee", employee_name)

    # التحقق من وجود البريد
    if not employee.email:
        frappe.throw(_("يجب إضافة البريد الإلكتروني للموظف أولاً"))

    # التحقق من عدم وجود المستخدم مسبقاً
    if frappe.db.exists("User", employee.email):
        frappe.throw(_("المستخدم موجود بالفعل بهذا البريد الإلكتروني"))

    # تحديد الدور
    role_map = {
        "Employee":     "Employee",
        "Line Manager": "Line Manager",
        "Logistics":    "Logistics",
        "Finance":      "Finance",
        "MD":           "MD",
        "Admin":        "System Manager",
    }
    target_role = role_map.get(employee.user_role, "Employee")

    # توليد كلمة مرور عشوائية
    chars = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(chars) for _ in range(10))

    # إنشاء المستخدم
    user = frappe.new_doc("User")
    user.email = employee.email
    user.first_name = employee.full_name_ar or employee.full_name_en or employee.email
    user.mobile_no = employee.mobile_number
    user.language = "ar"
    user.time_zone = "Asia/Riyadh"
    user.send_welcome_email = 0
    user.new_password = password
    user.append("roles", {"role": target_role})
    user.insert(ignore_permissions=True)

    frappe.db.commit()

    return {
        "success": True,
        "message": f"تم إنشاء الحساب بنجاح",
        "email": employee.email,
        "password": password,
        "role": target_role
    }
