import frappe
from frappe.utils import date_diff, today


def check_passport_expiry():
    employees = frappe.get_all(
        "SL Employee",
        filters={"passport_expiry": ["!=", ""]},
        fields=["name", "full_name_ar", "email", "passport_expiry"]
    )
    for emp in employees:
        if not emp.passport_expiry or not emp.email:
            continue
        days_left = date_diff(emp.passport_expiry, today())
        if days_left in [90, 60, 30, 14]:
            frappe.sendmail(
                recipients=[emp.email],
                subject=f"تنبيه: جواز سفرك ينتهي خلال {days_left} يوم",
                message=f"""
                <p>عزيزي {emp.full_name_ar}،</p>
                <p>جواز سفرك سينتهي خلال <b>{days_left} يوم</b> بتاريخ {emp.passport_expiry}.</p>
                <p>يرجى تجديد جواز السفر في أقرب وقت ممكن.</p>
                <p>فريق اللوجستيات — اتحاد الرياضة للجميع</p>
                """,
            )


def check_pending_deadlines():
    pending = frappe.get_all(
        "SL Travel Request",
        filters={"status": ["in", ["انتظار المدير المباشر", "انتظار المدير التنفيذي"]]},
        fields=["name", "start_date", "destination", "status"]
    )
    for req in pending:
        if not req.start_date:
            continue
        days_left = date_diff(req.start_date, today())
        if days_left <= 7:
            frappe.sendmail(
                recipients=["administrator"],
                subject=f"⚠️ طلب سفر معلق عاجل — {req.name}",
                message=f"""
                <p>طلب سفر معلق يحتاج موافقة عاجلة:</p>
                <ul>
                    <li><b>رقم الطلب:</b> {req.name}</li>
                    <li><b>الوجهة:</b> {req.destination}</li>
                    <li><b>تاريخ السفر:</b> {req.start_date}</li>
                    <li><b>المتبقي:</b> {days_left} أيام</li>
                    <li><b>الحالة:</b> {req.status}</li>
                </ul>
                """,
            )
