import frappe
from frappe import _
from frappe.utils import date_diff, today


def before_save(doc, method):
    if not doc.activity_date:
        return
    days_remaining = date_diff(doc.activity_date, today())
    if days_remaining < 28:
        frappe.throw(_(f"حجوزات المنشآت يجب تقديمها قبل 4 أسابيع. المتبقي: {days_remaining} يوم."))


def on_submit(doc, method):
    _log_action(doc, action="وافق", comment="تم اعتماد حجز المنشأة")


def _log_action(doc, action, comment=""):
    try:
        log = frappe.new_doc("SL Approvals Log")
        log.request_type = "Facility"
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
