import frappe
from frappe import _
from frappe.utils import date_diff, today


def before_save(doc, method):
    if not doc.entry_date:
        return
    days_remaining = date_diff(doc.entry_date, today())
    if days_remaining < 14:
        frappe.throw(_(f"طلب التخليص الجمركي يجب تقديمه قبل أسبوعين. المتبقي: {days_remaining} يوم."))


def on_submit(doc, method):
    if doc.status == "معتمد للتخليص" and doc.broker_email:
        _send_to_broker(doc)
    _log_action(doc, action="وافق", comment="تم اعتماد طلب التخليص")


def _send_to_broker(doc):
    try:
        frappe.sendmail(
            recipients=[doc.broker_email],
            subject=f"طلب تخليص جمركي — {doc.name} — اتحاد الرياضة للجميع",
            message=f"""
            <p>السادة شركة {doc.broker_company}،</p>
            <p>يرجى البدء في إجراءات التخليص الجمركي للشحنة التالية:</p>
            <ul>
                <li><b>رقم الطلب:</b> {doc.name}</li>
                <li><b>نوع الشحنة:</b> {doc.shipment_type}</li>
                <li><b>منفذ الدخول:</b> {doc.port_of_entry_name} ({doc.port_of_entry_type})</li>
                <li><b>تاريخ الدخول:</b> {doc.entry_date}</li>
            </ul>
            <p>فريق اللوجستيات — اتحاد الرياضة للجميع</p>
            """,
        )
    except Exception as e:
        frappe.log_error(f"خطأ في إرسال بريد المخلص: {str(e)}", "SL Customs Broker Email")


def _log_action(doc, action, comment=""):
    try:
        log = frappe.new_doc("SL Approvals Log")
        log.request_type = "Customs"
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
