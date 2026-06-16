import frappe
from frappe import _
from frappe.utils import date_diff, today


def before_save(doc, method):
    if doc.contains_asics_shoes or doc.contains_tshirts:
        doc.requires_md_approval = 1
        if doc.status == "جديد":
            doc.status = "انتظار MD"
    else:
        doc.requires_md_approval = 0

    if doc.delivery_date:
        days_remaining = date_diff(doc.delivery_date, today())
        if days_remaining < 2:
            frappe.throw(_(f"طلب المستودع يجب تقديمه قبل يومين. المتبقي: {days_remaining} يوم."))


def on_submit(doc, method):
    _log_action(doc, action="وافق", comment="تم اعتماد طلب المستودع")


def _log_action(doc, action, comment=""):
    try:
        log = frappe.new_doc("SL Approvals Log")
        log.request_type = "Inventory"
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
