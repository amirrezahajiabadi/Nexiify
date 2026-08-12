/* ============================================================
   Nexify - صفحه اصلی (index.html)
   انیمیشن شبکه‌ی عصبی (Canvas) + ذرات شناور
   ============================================================ */

const canvas = document.getElementById('neuralCanvas');
const ctx = canvas.getContext('2d');
let width, height, nodes = [];
let mouseX = -1000, mouseY = -1000;
/* R6: پرفورمنس موبایل */
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const isTouch = window.matchMedia('(hover: none)').matches;
let frame = 0;

function resizeCanvas() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    initNodes();
}

function initNodes() {
    nodes = [];
    const isMobile = window.innerWidth < 768;
    /* در تاچ: ذرات خیلی کمتر (باتری) — divisor بزرگ‌تر = تعداد کمتر */
    const divisor = isTouch ? 90000 : (isMobile ? 50000 : 28000);
    const count = Math.floor((width * height) / divisor);
    for (let i = 0; i < count; i++) {
        nodes.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 0.25,
            vy: (Math.random() - 0.5) * 0.25,
            radius: Math.random() * 1.5 + 0.5
        });
    }
}

function drawNeuralNetwork() {
    ctx.clearRect(0, 0, width, height);
    const isLight = document.documentElement.getAttribute('data-theme') === 'light';
    const nodeColor = isLight ? 'rgba(124,58,237,0.2)' : 'rgba(167,139,250,0.25)';
    const lineColor = isLight ? 'rgba(124,58,237,0.06)' : 'rgba(124,58,237,0.05)';
    const mouseLineColor = isLight ? 'rgba(124,58,237,0.1)' : 'rgba(167,139,250,0.08)';
    nodes.forEach(node => {
        node.x += node.vx;
        node.y += node.vy;
        if (node.x < 0 || node.x > width) node.vx *= -1;
        if (node.y < 0 || node.y > height) node.vy *= -1;
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
        ctx.fillStyle = nodeColor;
        ctx.fill();
    });
    nodes.forEach(a => {
        const dMouse = Math.hypot(a.x - mouseX, a.y - mouseY);
        if (dMouse < 200) {
            ctx.beginPath();
            ctx.moveTo(a.x, a.y);
            ctx.lineTo(mouseX, mouseY);
            ctx.strokeStyle = mouseLineColor.replace('0.08', (0.08 * (1 - dMouse / 200)).toString());
            ctx.lineWidth = 0.5;
            ctx.stroke();
        }
    });
    nodes.forEach((a, i) => {
        nodes.slice(i + 1).forEach(b => {
            const d = Math.hypot(a.x - b.x, a.y - b.y);
            if (d < 150) {
                ctx.beginPath();
                ctx.moveTo(a.x, a.y);
                ctx.lineTo(b.x, b.y);
                ctx.strokeStyle = lineColor.replace('0.05', (0.05 * (1 - d / 150)).toString());
                ctx.lineWidth = 0.3;
                ctx.stroke();
            }
        });
    });
    /* R6: در reduced-motion فقط یک فریم ثابت (بدون حلقه) — در تاچ ۳۰fps */
    if (reducedMotion) return;
    if (isTouch && (++frame % 2 !== 0)) { requestAnimationFrame(drawNeuralNetwork); return; }
    requestAnimationFrame(drawNeuralNetwork);
}

window.addEventListener('resize', resizeCanvas);
document.addEventListener('mousemove', e => { mouseX = e.clientX; mouseY = e.clientY; });
resizeCanvas();
drawNeuralNetwork();

document.getElementById('themeToggle').addEventListener('click', () => {
    setTimeout(() => { nodes = []; initNodes(); }, 100);
});

/* افکت spotlight دنبال‌کننده موس روی کارت‌های خدمات (CSP-safe: فقط setProperty) */
function initServiceSpotlight() {
    const cards = document.querySelectorAll('.service-card:not(.service-card-cta)');
    if (!cards.length) return;
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reducedMotion) return;
    cards.forEach(card => {
        let mx = '50%', my = '50%', rafId = null;
        card.addEventListener('pointermove', e => {
            const rect = card.getBoundingClientRect();
            mx = `${e.clientX - rect.left}px`;
            my = `${e.clientY - rect.top}px`;
            if (rafId) return;
            rafId = requestAnimationFrame(() => {
                rafId = null;
                card.style.setProperty('--mx', mx);
                card.style.setProperty('--my', my);
            });
        });
    });
}
initServiceSpotlight();

/* ذرات شناور — R6: در reduced-motion ساخته نمی‌شوند */
const particlesContainer = document.getElementById('bgParticles');
function createParticle() {
    const p = document.createElement('div');
    p.classList.add('particle');
    const s = Math.random() * 2 + 1;
    p.style.width = s + 'px';
    p.style.height = s + 'px';
    p.style.left = Math.random() * 100 + '%';
    p.style.animationDuration = (Math.random() * 15 + 12) + 's';
    p.style.animationDelay = Math.random() * 10 + 's';
    particlesContainer.appendChild(p);
    p.addEventListener('animationend', () => { p.remove(); createParticle(); });
}
const isMobile = window.innerWidth < 768;
if (!reducedMotion) { for (let i = 0; i < (isMobile ? 12 : 25); i++) { createParticle(); } }

/* ============================================================
   شمارنده‌ی نرم آمار — هنگام ورود به دید، از صفر تا مقدار نهایی می‌شمارد
   (IntersectionObserver + requestAnimationFrame + easeOutExpo + ارقام فارسی)
   CSP-safe: فقط textContent — بدون innerHTML
   ============================================================ */
(function () {
    const counters = document.querySelectorAll('.stat-count[data-count]');
    if (!counters.length) return;

    const FA_DIGITS = '۰۱۲۳۴۵۶۷۸۹';
    const toFa = (n) => String(n).replace(/[0-9]/g, (d) => FA_DIGITS[+d]);
    const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const DURATION = 1600;        // ms — نرم و آرام
    const STAGGER = 140;          // ms — تأخیر پلکانی بین آیتم‌ها

    function animate(el, delay) {
        const target = parseInt(el.dataset.count, 10) || 0;
        if (reducedMotion) {
            el.textContent = toFa(target);
            return;
        }
        el.textContent = toFa(0);
        const start = performance.now() + delay;
        function frame(now) {
            const t = Math.max(0, Math.min((now - start) / DURATION, 1));
            const eased = 1 - Math.pow(1 - t, 4); // easeOutQuart — شروع تند، پایان نرم
            el.textContent = toFa(Math.round(eased * target));
            if (t < 1) requestAnimationFrame(frame);
        }
        requestAnimationFrame(frame);
    }

    const obs = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            const el = entry.target;
            const index = Array.prototype.indexOf.call(counters, el);
            animate(el, index * STAGGER);
            obs.unobserve(el);
        });
    }, { threshold: 0.5 });

    counters.forEach((el) => obs.observe(el));
})();

/* ============================================================
   فاز U6 — ویجت مسیر انتخاب «من یک...»
   دو مرحله: نوع کسب‌وکار + نیاز → مسیر پیشنهادی + لینک تماس با پری‌سلکت
   CSP-safe: فقط textContent / classList — بدون innerHTML
   ============================================================ */
(function () {
    const card = document.querySelector('.path-card');
    if (!card) return;
    const contactUrl = card.dataset.contactUrl || '/contact/';
    const resultText = card.querySelector('.path-result-text');
    const resultCta = card.querySelector('.path-result-cta');

    const WHO_LABELS = {
        store: 'فروشگاه آنلاین',
        startup: 'استارتاپ',
        company: 'شرکت و سازمان',
        clinic: 'کلینیک و سلامت'
    };
    const WANT = {
        site:    { label: 'سایت و فروشگاه بسازم', type: 'web-design' },
        agent:   { label: 'Agent هوشمند بسازم',   type: 'agent-ai' },
        mlops:   { label: 'اتوماسیون و MLOps',    type: 'mlops' },
        consult: { label: 'مشاوره بگیرم',         type: 'consulting' }
    };
    const TYPE_LABELS = {
        'web-design': 'طراحی سایت',
        'agent-ai': 'ساخت Agent AI',
        'mlops': 'MLOps و استقرار مدل',
        'consulting': 'مشاوره رایگان'
    };

    let who = null, want = null;

    function setPills() {
        card.querySelectorAll('.path-option').forEach(function (btn) {
            const active = (btn.dataset.who && btn.dataset.who === who) ||
                           (btn.dataset.want && btn.dataset.want === want);
            btn.classList.toggle('selected', active);
            btn.setAttribute('aria-pressed', active ? 'true' : 'false');
        });
    }

    function render() {
        setPills();
        if (!who || !want) return;
        const wantMeta = WANT[want];
        const params = new URLSearchParams({ type: wantMeta.type, subject: WHO_LABELS[who] + ' — ' + wantMeta.label });
        resultCta.href = contactUrl + '?' + params.toString();
        resultCta.hidden = false;

        /* ساخت متن بدون innerHTML (CSP-safe) */
        resultText.textContent = '';
        resultText.appendChild(document.createTextNode('عالی! برای «' + WHO_LABELS[who] + '» که می‌خواهد «' + wantMeta.label + '»، بهترین مسیر '));
        const strong = document.createElement('strong');
        strong.textContent = TYPE_LABELS[wantMeta.type];
        resultText.appendChild(strong);
        resultText.appendChild(document.createTextNode(' است. همین حالا درخواست بده تا رایگان مشورت کنیم.'));
    }

    card.querySelectorAll('.path-option').forEach(function (btn) {
        btn.addEventListener('click', function () {
            if (btn.dataset.who) who = btn.dataset.who;
            if (btn.dataset.want) want = btn.dataset.want;
            render();
        });
    });
})();
