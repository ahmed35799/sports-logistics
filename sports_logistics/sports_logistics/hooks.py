app_name = "sports_logistics"
app_title = "Sports Logistics"
app_publisher = "Ahmed Saad"
app_description = "Logistics Automation System for Sports Federation"
app_email = "ah.elbahwashy@gmail.com"
app_license = "mit"

fixtures = [
    {"doctype": "DocType", "filters": [["module", "=", "Sports Logistics"]]},
    {"doctype": "Workflow", "filters": [["document_type", "like", "SL%"]]},
    {"doctype": "Role", "filters": [["name", "in", ["Employee", "Line Manager", "Logistics", "Finance", "MD"]]]},
]

doc_events = {
    "SL Travel Request": {
        "before_save": "sports_logistics.events.travel_request.before_save",
        "on_submit": "sports_logistics.events.travel_request.on_submit",
        "on_cancel": "sports_logistics.events.travel_request.on_cancel",
        "on_update_after_submit": "sports_logistics.events.travel_request.on_update_after_submit",
    },
    "SL Custom Clearance": {
        "before_save": "sports_logistics.events.custom_clearance.before_save",
        "on_submit": "sports_logistics.events.custom_clearance.on_submit",
    },
    "SL Government Visas": {
        "before_save": "sports_logistics.events.government_visas.before_save",
        "on_submit": "sports_logistics.events.government_visas.on_submit",
    },
    "SL Leave Letters": {
        "before_save": "sports_logistics.events.leave_letters.before_save",
        "on_submit": "sports_logistics.events.leave_letters.on_submit",
    },
    "SL Inventory Requests": {
        "before_save": "sports_logistics.events.inventory_requests.before_save",
        "on_submit": "sports_logistics.events.inventory_requests.on_submit",
    },
    "SL Facility Bookings": {
        "before_save": "sports_logistics.events.facility_bookings.before_save",
        "on_submit": "sports_logistics.events.facility_bookings.on_submit",
    },
}

scheduler_events = {
    "daily": [
        "sports_logistics.tasks.daily.check_passport_expiry",
        "sports_logistics.tasks.daily.check_pending_deadlines",
    ],
}

permission_query_conditions = {
    "SL Travel Request": "sports_logistics.permissions.get_travel_request_conditions",
    "SL Custom Clearance": "sports_logistics.permissions.get_clearance_conditions",
    "SL Government Visas": "sports_logistics.permissions.get_visa_conditions",
    "SL Leave Letters": "sports_logistics.permissions.get_leave_conditions",
    "SL Inventory Requests": "sports_logistics.permissions.get_inventory_conditions",
    "SL Facility Bookings": "sports_logistics.permissions.get_facility_conditions",
}

# ربط User بـ SL Employee عند تسجيل الدخول
on_login = "sports_logistics.auth.on_login"
