/* ============================================================
   Nexify - پنل مدیریت (admin.html)
   ناوبری سایدبار + مودال‌ها + فیلدهای داینامیک + تم
   (بدون onclick اینلاین — آماده برای CSP)
   این پنل نمایشی است و در فاز ۴ با Django Admin جایگزین می‌شود.
   ============================================================ */

/* --- ناوبری سایدبار --- */
document.querySelectorAll('.sidebar-link').forEach(link => {
    link.addEventListener('click', () => {
        document.querySelectorAll('.sidebar-link').forEach(l => l.classList.remove('active'));
        link.classList.add('active');
        const sectionId = link.dataset.section;
        document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
        document.getElementById(sectionId).classList.add('active');
        document.getElementById('pageTitle').textContent = link.textContent.trim();
        if (window.innerWidth < 768) closeSidebar();
    });
});

function toggleSidebar() { document.getElementById('sidebar').classList.toggle('open'); }
function closeSidebar() { document.getElementById('sidebar').classList.remove('open'); }

/* --- مودال‌ها --- */
function openServiceModal() { document.getElementById('serviceModal').classList.add('open'); }
function closeModal(id) { document.getElementById(id).classList.remove('open'); }

/* --- فیلدهای داینامیک --- */
/* ساخت فیلدهای داینامیک بدون innerHTML (ضد XSS) */
function addFieldRow(listId, placeholders) {
    const div = document.createElement('div');
    div.className = 'form-row';
    div.style.marginBottom = '12px';
    placeholders.forEach(ph => {
        const input = document.createElement('input');
        input.className = 'form-input';
        input.placeholder = ph;
        div.appendChild(input);
    });
    document.getElementById(listId).appendChild(div);
}

function addSkillField() {
    addFieldRow('skillsList', ['نام مهارت', 'درصد']);
}

function addTimelineField() {
    addFieldRow('timelineList', ['سال', 'عنوان']);
}

/* --- تم پنل --- */
function toggleAdminTheme() {
    const root = document.documentElement;
    if (root.style.getPropertyValue('--admin-bg') === '#0f172a') {
        // حالت روشن
        root.style.setProperty('--admin-bg', '#f5f6fa');
        root.style.setProperty('--admin-surface', '#ffffff');
        root.style.setProperty('--admin-text', '#1e293b');
        root.style.setProperty('--sidebar-bg', '#1e293b');
    } else {
        // حالت تاریک
        root.style.setProperty('--admin-bg', '#0f172a');
        root.style.setProperty('--admin-surface', '#1e293b');
        root.style.setProperty('--admin-text', '#f1f5f9');
        root.style.setProperty('--sidebar-bg', '#0f172a');
    }
}

/* --- اتصال رویدادها (به‌جای onclick اینلاین) --- */
document.getElementById('sidebarToggle').addEventListener('click', toggleSidebar);
document.getElementById('openServiceModalBtn').addEventListener('click', openServiceModal);
document.getElementById('addSkillFieldBtn').addEventListener('click', addSkillField);
document.getElementById('addTimelineFieldBtn').addEventListener('click', addTimelineField);
document.getElementById('toggleAdminThemeBtn').addEventListener('click', toggleAdminTheme);

document.querySelectorAll('[data-close-modal]').forEach(btn => {
    btn.addEventListener('click', () => closeModal(btn.dataset.closeModal));
});
