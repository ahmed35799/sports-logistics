import frappe
from frappe import _
from frappe.utils import date_diff, today


def before_save(doc, method):
    if not doc.start_date:
        return
    days_remaining = date_diff(doc.start_date, today())
    if days_remaining < 14:
        frappe.throw(_(f"خطابات الأذونات يجب تقديمها قبل أسبوعين. المتبقي: {days_remaining} يوم."))


def on_submit(doc, method):
    if doc.status == "صدر الخطاب" and doc.recipient_email:
        _send_letter(doc)
    _log_action(doc, action="وافق", comment="صدر خطاب الإذن")


def _send_letter(doc):
    try:
        employee = frappe.get_doc("SL Employee", doc.requester)
        frappe.sendmail(
            recipients=[doc.recipient_email],
            subject=f"خطاب إذن — {employee.full_name_ar}",
            message=f"""
            <p>السادة {doc.recipient_org}،</p>
            <p>نفيدكم بأن {employee.full_name_ar} — {employee.job_title}
            في اتحاد الرياضة للجميع، مأذون له بالمشاركة في فعالية
            <b>{doc.event_name}</b> من تاريخ {doc.start_date}
            لمدة {doc.leave_duration_days} أيام.</p>
            <p>فريق اللوجستيات — اتحاد الرياضة للجميع</p>
            """,
        )
    except Exception as e:
        frappe.log_error(f"خطأ في إرسال خطاب الإذن: {str(e)}", "SL Leave Letter Email")


def _log_action(doc, action, comment=""):
    try:
        log = frappe.new_doc("SL Approvals Log")
        log.request_type = "Leave"
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
