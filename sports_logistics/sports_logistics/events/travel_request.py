import frappe
from frappe import _
from frappe.utils import date_diff, today


def before_save(doc, method):
    _validate_deadlines(doc)


def on_submit(doc, method):
    _log_action(doc, action="وافق", comment="تم إرسال الطلب")


def on_cancel(doc, method):
    _log_action(doc, action="رفض", comment="تم إلغاء الطلب")


def on_update_after_submit(doc, method):
    if doc.has_value_changed("status"):
        _log_action(
            doc,
            action="وافق" if doc.status == "معتمد" else "رفض",
            comment=f"تغيرت الحالة إلى: {doc.status}"
        )
        _send_status_notification(doc)


def _validate_deadlines(doc):
    if not doc.start_date:
        return
    days_remaining = date_diff(doc.start_date, today())
    if doc.travel_scope == "محلي" and days_remaining < 5:
        frappe.throw(_(f"الرحلات المحلية تتطلب تقديم الطلب قبل 5 أيام عمل. المتبقي: {days_remaining} يوم."))
    if doc.travel_scope == "دولي" and days_remaining < 21:
        frappe.throw(_(f"الرحلات الدولية تتطلب تقديم الطلب قبل 21 يوماً. المتبقي: {days_remaining} يوم."))
    if doc.trip_type == "وفد / لاعبون" and days_remaining < 42:
        frappe.throw(_(f"رحلات الوفود تتطلب تقديم الطلب قبل 6 أسابيع. المتبقي: {days_remaining} يوم."))


def _send_status_notification(doc):
    try:
        employee = frappe.get_doc("SL Employee", doc.requester)
        if not employee.email:
            return
        frappe.sendmail(
            recipients=[employee.email],
            subject=f"تحديث حالة طلب السفر — {doc.name}",
            message=f"""
            <p>عزيزي {employee.full_name_ar}،</p>
            <p>تم تحديث حالة طلب السفر الخاص بك:</p>
            <ul>
                <li><b>رقم الطلب:</b> {doc.name}</li>
                <li><b>الوجهة:</b> {doc.destination}</li>
                <li><b>الحالة الجديدة:</b> {doc.status}</li>
            </ul>
            <p>فريق اللوجستيات — اتحاد الرياضة للجميع</p>
            """,
        )
    except Exception as e:
        frappe.log_error(f"خطأ في إرسال الإشعار: {str(e)}", "SL Travel Notification")


def _log_action(doc, action, comment=""):
    try:
        log = frappe.new_doc("SL Approvals Log")
        log.request_type = "Travel"
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
