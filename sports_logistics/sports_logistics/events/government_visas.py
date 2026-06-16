import frappe
from frappe import _
from frappe.utils import date_diff, today


def before_save(doc, method):
    if not doc.expected_arrival_date:
        return
    days_remaining = date_diff(doc.expected_arrival_date, today())
    if doc.visitor_type == "عضو وفد خارجي" and days_remaining < 60:
        frappe.throw(_(f"تأشيرات الوفود يجب تقديمها قبل شهرين. المتبقي: {days_remaining} يوم."))
    elif days_remaining < 21:
        frappe.throw(_(f"طلب الفيزا يجب تقديمه قبل 15 يوم عمل. المتبقي: {days_remaining} يوم."))


def on_submit(doc, method):
    _log_action(doc, action="وافق", comment="تم اعتماد طلب الفيزا")


def _log_action(doc, action, comment=""):
    try:
        log = frappe.new_doc("SL Approvals Log")
        log.request_type = "Visa"
        log.request_ref_id = doc.name
        log.approver = frappe.session.user
        log.approver_role = ", ".join(frappe.get_roles(frappe.session.user))
        log.action = action
        log.comment = comment
        log.action_timestamp = frappe.utils.now()
        log.previous_status = doc.get_db_value("status") or "جديد"
        log.new_status = doc.status
        log.insert(ignore_permissions=True)
    except Exception as e:
        frappe.log_error(f"خطأ في تسجيل Approvals Log: {str(e)}", "SL Approvals Log")
