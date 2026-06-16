frappe.pages['sl-portal'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'بوابة اللوجستيات',
        single_column: true
    });

    if (!document.getElementById('sl-portal-css')) {
        var style = document.createElement('style');
        style.id = 'sl-portal-css';
        style.innerHTML = `
            .sl-portal {
                padding: 24px;
                direction: rtl;
                max-width: 1100px;
                margin: 0 auto;
            }
            .sl-welcome {
                background: var(--primary);
                color: var(--primary-color, #fff);
                padding: 28px 32px;
                border-radius: var(--border-radius-lg, 12px);
                margin-bottom: 32px;
            }
            .sl-welcome h2 {
                font-size: 22px;
                color: #fff;
                margin: 0 0 6px 0;
            }
            .sl-welcome p {
                margin: 0;
                opacity: .85;
                font-size: 14px;
                color: #fff;
            }
            .sl-section-title {
                font-size: 15px;
                font-weight: 700;
                color: var(--heading-color);
                margin: 0 0 16px 0;
                padding-bottom: 10px;
                border-bottom: 2px solid var(--border-color);
            }
            .sl-cards-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 18px;
                margin-bottom: 32px;
            }
            .sl-card {
                background: var(--card-bg);
                border: 1.5px solid var(--border-color);
                border-radius: var(--border-radius-lg, 12px);
                padding: 28px 16px;
                text-align: center;
                cursor: pointer;
                transition: all .25s;
                box-shadow: var(--card-shadow);
            }
            .sl-card:hover {
                transform: translateY(-3px);
                box-shadow: var(--shadow-md);
                border-color: var(--primary);
            }
            .sl-card-icon {
                font-size: 32px;
                margin-bottom: 12px;
                color: var(--primary);
            }
            .sl-card-icon i {
                font-size: 32px;
                color: var(--primary);
            }
            .sl-card-title {
                font-size: 15px;
                font-weight: 700;
                color: var(--heading-color);
                margin-bottom: 6px;
            }
            .sl-card-desc {
                font-size: 12px;
                color: var(--text-muted);
                line-height: 1.5;
            }
            .sl-section {
                background: var(--card-bg);
                border: 1px solid var(--border-color);
                border-radius: var(--border-radius-lg, 12px);
                padding: 22px;
                margin-bottom: 22px;
                box-shadow: var(--card-shadow);
            }
            .sl-table {
                width: 100%;
                border-collapse: collapse;
                font-size: 13px;
            }
            .sl-table th {
                background: var(--subtle-bg);
                color: var(--heading-color);
                padding: 9px 12px;
                text-align: right;
                font-weight: 700;
            }
            .sl-table td {
                padding: 9px 12px;
                border-bottom: 1px solid var(--border-color);
                color: var(--text-color);
            }
            .sl-table tr:last-child td {
                border-bottom: none;
            }
            .sl-table a {
                color: var(--primary);
                font-weight: 600;
                text-decoration: none;
                cursor: pointer;
            }
            .sl-badge {
                padding: 3px 10px;
                border-radius: 20px;
                font-size: 11px;
                font-weight: 700;
                display: inline-block;
            }
            .sl-gray    { background: var(--subtle-bg); color: var(--text-muted); }
            .sl-warning { background: #FFF3CD; color: #856404; }
            .sl-success { background: #D6F0D6; color: #1E5C1E; }
            .sl-danger  { background: #FAD7D7; color: #8B1A1A; }
            .sl-empty {
                text-align: center;
                color: var(--text-muted);
                padding: 20px;
                font-size: 13px;
            }
            @media(max-width:768px) { .sl-cards-grid { grid-template-columns: repeat(2,1fr); } }
            @media(max-width:480px) { .sl-cards-grid { grid-template-columns: 1fr; } }
        `;
        document.head.appendChild(style);
    }

    var cards = [
        { icon: 'fa fa-plane',     title: 'حجوزات السفر',      desc: 'رحلات عمل، فعاليات، دورات، وفود', doctype: 'SL Travel Request' },
        { icon: 'fa fa-ship',      title: 'التخليص الجمركي',   desc: 'شحنات مؤقتة ودائمة ومرافقة',      doctype: 'SL Custom Clearance' },
        { icon: 'fa fa-id-card',   title: 'الفيزا الحكومية',   desc: 'تأشيرات الزوار والموردين',          doctype: 'SL Government Visas' },
        { icon: 'fa fa-file-text', title: 'خطابات الأذونات',   desc: 'أذونات المشاركة في الفعاليات',     doctype: 'SL Leave Letters' },
        { icon: 'fa fa-archive',   title: 'طلبات المستودع',    desc: 'صرف المعدات والعهد',                doctype: 'SL Inventory Requests' },
        { icon: 'fa fa-building',  title: 'حجوزات المنشآت',    desc: 'حجز الملاعب والصالات',              doctype: 'SL Facility Bookings' },
    ];

    var cards_html = cards.map(function(c) {
        return `<div class="sl-card" data-doctype="${c.doctype}">
            <div class="sl-card-icon"><i class="${c.icon}"></i></div>
            <div class="sl-card-title">${c.title}</div>
            <div class="sl-card-desc">${c.desc}</div>
        </div>`;
    }).join('');

    $(wrapper).find('.page-content').html(`
        <div class="sl-portal">
            <div class="sl-welcome">
                <h2>👋 مرحباً بك في بوابة اللوجستيات</h2>
                <p>اختر نوع الطلب الذي تريد تقديمه</p>
            </div>
            <div class="sl-cards-grid">${cards_html}</div>
            <div class="sl-section">
                <div class="sl-section-title">📋 طلباتي الأخيرة</div>
                <div id="sl-my-requests"><div class="sl-empty">جاري التحميل...</div></div>
            </div>
        </div>
    `);

    $(wrapper).on('click', '.sl-card', function() {
        frappe.new_doc($(this).data('doctype'));
    });

    frappe.call({
        method: 'frappe.client.get_list',
        args: {
            doctype: 'SL Travel Request',
            fields: ['name', 'destination', 'start_date', 'status'],
            limit: 5,
            order_by: 'creation desc'
        },
        callback: function(r) {
            if (!r.message || !r.message.length) {
                $('#sl-my-requests').html('<div class="sl-empty">لا توجد طلبات بعد</div>');
                return;
            }
            var colors = {
                'مسودة': 'sl-gray',
                'انتظار المدير المباشر': 'sl-warning',
                'انتظار المدير التنفيذي': 'sl-warning',
                'معتمد': 'sl-success',
                'مرفوض': 'sl-danger',
                'ملغى': 'sl-gray'
            };
            var rows = r.message.map(function(row) {
                return `<tr>
                    <td><a onclick="frappe.set_route('Form','SL Travel Request','${row.name}')">${row.name}</a></td>
                    <td>${row.destination || '-'}</td>
                    <td>${row.start_date || '-'}</td>
                    <td><span class="sl-badge ${colors[row.status] || 'sl-gray'}">${row.status}</span></td>
                </tr>`;
            }).join('');
            $('#sl-my-requests').html(`
                <table class="sl-table">
                    <thead><tr>
                        <th>رقم الطلب</th>
                        <th>الوجهة</th>
                        <th>تاريخ السفر</th>
                        <th>الحالة</th>
                    </tr></thead>
                    <tbody>${rows}</tbody>
                </table>
            `);
        }
    });
};
