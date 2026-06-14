INSERT INTO public.approval_routing_rules
(rule_id, request_type, requester_department, assigned_manager_id, backup_manager_id, requires_md_approval, created_at, updated_at)
VALUES(nextval('approval_routing_rules_rule_id_seq'::regclass), '', '', 0, 0, false, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO public.approvals_log
(log_id, request_type, request_ref_id, approver_id, approver_role, "action", "comment", action_timestamp, previous_status, new_status)
VALUES(nextval('approvals_log_log_id_seq'::regclass), '', 0, 0, '', '', '', CURRENT_TIMESTAMP, '', '');
INSERT INTO public.custom_clearance
(clearance_id, requester_id, related_travel_id, shipment_type, import_purpose, port_of_entry_type, port_of_entry_name, entry_date, exit_date, flight_details, passenger_passports, invoices, packing_list_ar, item_pictures, gcc_drivers_data, broker_company, broker_mobile, broker_email, status, md_approval_date, created_at, updated_at)
VALUES(nextval('custom_clearance_clearance_id_seq'::regclass), 0, 0, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO public.delegations_list
(delegation_item_id, parent_travel_request_id, member_type, registration_type, player_status, game_name, registration_date, full_name, nationality, passport_number, passport_expiry, national_id, mobile, departure_city, arrival_city, passport_copy, id_copy, birth_certificate, created_at)
VALUES(nextval('delegations_list_delegation_item_id_seq'::regclass), 0, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', CURRENT_TIMESTAMP);
INSERT INTO public.employees
(employee_id, full_name_ar, full_name_en, nationality, job_title, department, national_id_iqama, mobile_number, email, date_of_birth, employment_type, work_sector, educational_qual, years_experience, religion, marital_status, passport_number, passport_expiry, employment_contract, cv_file, created_at, updated_at, "password", user_role)
VALUES(nextval('employees_employee_id_seq'::regclass), '', '', '', '', '', '', '', '', '', '', '', '', 0, '', '', '', '', '', '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, '', 'Employee'::character varying);
INSERT INTO public.facility_bookings
(facility_booking_id, requester_id, org_or_group_name, facility_city, facility_name, facility_branch, hall_number, activity_type, activity_details, activity_date, start_time, end_time, visitors_count, status, cancellation_reason, logistics_notes, created_at)
VALUES(nextval('facility_bookings_facility_booking_id_seq'::regclass), 0, '', '', '', '', '', '', '', '', '', '', 0, '', '', '', CURRENT_TIMESTAMP);
INSERT INTO public.government_visas
(visa_request_id, requester_id, expected_arrival_date, visitor_full_name, visitor_nationality, visitor_organization, visitor_type, visitor_form, passport_pdf, personal_photo, gcc_residence_permit, visa_type, vendor_notified, status, rejection_reason, issue_date, notes, created_at, updated_at)
VALUES(nextval('government_visas_visa_request_id_seq'::regclass), 0, '', '', '', '', '', '', '', '', '', '', false, '', '', '', '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO public.inventory_requests
(inventory_req_id, requester_id, delivery_date, items_description, contains_asics_shoes, contains_tshirts, requires_md_approval, status, logistics_notes, created_at)
VALUES(nextval('inventory_requests_inventory_req_id_seq'::regclass), 0, '', '', false, false, false, '', '', CURRENT_TIMESTAMP);
INSERT INTO public.leave_letters
(leave_id, requester_id, member_type, registration_type, player_type, registration_date, game_name, event_name, event_type, request_reason, leave_duration_days, start_date, event_region, event_city, event_street, postal_code, event_venue, has_camp, recipient_position, recipient_org, recipient_email, health_report, birth_certificate, work_sector, status, created_at)
VALUES(nextval('leave_letters_leave_id_seq'::regclass), 0, '', '', '', '', '', '', '', '', 0, '', '', '', '', '', '', false, '', '', '', '', '', '', '', CURRENT_TIMESTAMP);
INSERT INTO public.transportation_schedule
(trans_item_id, parent_travel_request_id, from_location, to_location, date_time, car_size_type, with_driver, guests_count, luggage_pieces, transport_purpose, notes, created_at)
VALUES(nextval('transportation_schedule_trans_item_id_seq'::regclass), 0, '', '', '', '', false, 0, 0, '', '', CURRENT_TIMESTAMP);
INSERT INTO public.travel_requests
(request_id, requester_id, trip_type, travel_scope, departure_city, destination, start_date, end_date, reason_for_trip, flight_required, preferred_flight_times, traveler_id_copy, hotel_required, hotel_option_1, hotel_option_2, hotel_option_3, insurance_required, transportation_req, car_with_driver, visa_required, full_board_required, status, cancellation_reason, logistics_notes, created_at, updated_at)
VALUES(nextval('travel_requests_request_id_seq'::regclass), 0, '', '', '', '', '', '', '', false, '', '', false, '', '', '', false, false, false, false, false, '', '', '', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
