/* اسکریپت صفحات ورود/ثبت‌نام — کاملاً CSP-safe (بدون inline handler، بدون innerHTML) */

function initAuthPasswordToggles() {
    document.querySelectorAll('.auth-password-toggle').forEach(function (btn) {
        const input = document.getElementById(btn.dataset.target);
        if (!input) return;
        btn.addEventListener('click', function () {
            const show = input.type === 'password';
            input.type = show ? 'text' : 'password';
            btn.classList.toggle('active', show);
            btn.setAttribute('aria-pressed', String(show));
        });
    });
}

/* هاله‌ی دنبال‌کننده‌ی موس روی کارت — rAF throttle + فقط transform/opacity (GPU) */
function initAuthSpotlight() {
    const card = document.getElementById('authCard');
    const glow = card && card.querySelector('.auth-card-glow');
    if (!card || !glow) return;
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    let raf = null;
    card.addEventListener('pointermove', function (e) {
        if (raf) return;
        raf = requestAnimationFrame(function () {
            raf = null;
            const r = card.getBoundingClientRect();
            const mx = e.clientX - r.left;
            const my = e.clientY - r.top;
            // 140 = نصف قطر گوی (280px) برای وسط‌چین‌کردن روی موس
            glow.style.opacity = '1';
            glow.style.transform = 'translate3d(' + (mx - 140) + 'px, ' + (my - 140) + 'px, 0)';
        });
    });
    card.addEventListener('pointerleave', function () {
        if (raf) { cancelAnimationFrame(raf); raf = null; }
        glow.style.opacity = '0';
    });
}

/* متر قدرت رمز عبور (فقط راهنمای UX — اعتبارسنجی واقعی سمت سرور است) */
function initAuthStrength() {
    const meter = document.getElementById('authStrength');
    const input = meter && document.getElementById(meter.dataset.target || '');
    if (!meter || !input) return;

    const text = meter.querySelector('.auth-strength-text');
    const labels = ['ضعیف', 'متوسط', 'قوی'];

    function score(value) {
        let s = 0;
        if (value.length >= 8) s++;
        if (/\d/.test(value)) s++;
        if (/[A-Z]/.test(value) || /[^A-Za-z0-9]/.test(value)) s++;
        return s;
    }

    input.addEventListener('input', function () {
        const v = input.value;
        if (!v) { meter.hidden = true; meter.className = 'auth-strength'; return; }
        const s = score(v);
        meter.hidden = false;
        meter.className = 'auth-strength strength-' + Math.max(s, 1);
        if (text) text.textContent = labels[Math.min(Math.max(s - 1, 0), 2)];
    });
}

document.addEventListener('DOMContentLoaded', function () {
    initAuthPasswordToggles();
    initAuthSpotlight();
    initAuthStrength();
});
