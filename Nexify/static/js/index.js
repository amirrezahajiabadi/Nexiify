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
