frappe.ui.form.on('SL Employee', {
    refresh: function(frm) {
        // زر إنشاء حساب — للـ Admin فقط
        if (frappe.user_roles.includes('System Manager') && !frm.is_new()) {

            // التحقق من وجود مستخدم مسبق
            frappe.call({
                method: 'frappe.client.get_count',
                args: {
                    doctype: 'User',
                    filters: { email: frm.doc.email }
                },
                callback: function(r) {
                    if (r.message === 0) {
                        frm.add_custom_button(__('إنشاء حساب مستخدم'), function() {
                            frappe.confirm(
                                `هل تريد إنشاء حساب لـ <b>${frm.doc.full_name_ar}</b>؟<br>
                                سيتم إرسال بيانات الدخول عبر البريد: <b>${frm.doc.email}</b>`,
                                function() {
                                    frappe.call({
                                        method: 'sports_logistics.api.create_user_from_employee',
                                        args: { employee_name: frm.doc.name },
                                        callback: function(r) {
                                            if (r.message && r.message.success) {
                                                frappe.msgprint({
                                                    title: 'تم بنجاح ✅',
                                                    message: `
                                                        <b>البريد:</b> ${r.message.email}<br>
                                                        <b>كلمة المرور:</b> ${r.message.password}<br>
                                                        <b>الدور:</b> ${r.message.role}<br><br>
                                                        <i>احتفظ بهذه البيانات وأرسلها للموظف</i>
                                                    `,
                                                    indicator: 'green'
                                                });
                                                frm.reload_doc();
                                            }
                                        }
                                    });
                                }
                            );
                        }, __('إدارة المستخدمين'));
                    } else {
                        frm.add_custom_button(__('حساب موجود ✅'), function() {
                            frappe.set_route('Form', 'User', frm.doc.email);
                        }, __('إدارة المستخدمين'));
                    }
                }
            });
        }
    }
});
