function getScrollbarWidth() { return window.innerWidth - document.documentElement.clientWidth; }
function lockScroll() { const w = getScrollbarWidth(); document.body.style.overflow = 'hidden'; if (w > 0) document.body.style.paddingLeft = w + 'px'; }
function unlockScroll() { document.body.style.overflow = ''; document.body.style.paddingLeft = ''; }

function initTheme() {
    const toggle = document.getElementById('themeToggle');
    if (!toggle) return;
    const saved = localStorage.getItem('nexify-theme') || 'dark';
    document.documentElement.setAttribute('data-theme', saved);
    toggle.addEventListener('click', () => {
        const cur = document.documentElement.getAttribute('data-theme');
        const next = cur === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('nexify-theme', next);
    });
}

function initPreloader() {
    const p = document.getElementById('preloader');
    if (!p) return;
    let done = false;
    const t = setTimeout(() => { if (!done) { p.classList.add('hidden'); document.body.style.overflow = ''; done = true; } }, 3000);
    window.addEventListener('load', () => { if (!done) { clearTimeout(t); setTimeout(() => { p.classList.add('hidden'); document.body.style.overflow = ''; done = true; }, 600); } });
    document.body.style.overflow = 'hidden';
}

function initCounters() {
    document.querySelectorAll('.stat-value').forEach(el => {
        const obs = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const txt = el.textContent;
                    const num = parseInt(txt.replace(/[^0-9]/g, ''));
                    const suf = txt.replace(/[0-9]/g, '');
                    if (isNaN(num)) { obs.unobserve(el); return; }
                    const dur = 2000; const st = performance.now();
                    function upd(now) {
                        const p = Math.min((now - st) / dur, 1);
                        const v = Math.floor(num * (1 - Math.pow(1 - p, 3)));
                        el.textContent = v + suf;
                        if (p < 1) requestAnimationFrame(upd); else el.textContent = txt;
                    }
                    requestAnimationFrame(upd);
                    obs.unobserve(el);
                }
            });
        }, { threshold: 0.5 });
        obs.observe(el);
    });
}

function initReveal() {
    const obs = new IntersectionObserver((entries) => { entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }); }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });
    document.querySelectorAll('.reveal').forEach(el => obs.observe(el));
}

function initNavbar() {
    const nb = document.getElementById('navbar');
    if (!nb) return;
    window.addEventListener('scroll', () => nb.classList.toggle('scrolled', window.scrollY > 50));
}

function initBackToTop() {
    const btn = document.getElementById('backToTop');
    if (!btn) return;
    window.addEventListener('scroll', () => btn.classList.toggle('visible', window.scrollY > 500));
    btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}

function initMobileMenu() {
    const menu = document.getElementById('mobileMenu'), toggle = document.getElementById('mobileToggle'), close = document.getElementById('mobileMenuClose');
    if (!menu || !toggle || !close) return;
    toggle.addEventListener('click', () => menu.classList.add('open'));
    close.addEventListener('click', () => menu.classList.remove('open'));
    menu.querySelectorAll('a').forEach(l => l.addEventListener('click', () => menu.classList.remove('open')));
    document.addEventListener('keydown', e => { if (e.key === 'Escape' && menu.classList.contains('open')) menu.classList.remove('open'); });
}

function initActiveNav() {
    /* با URL های جنگو کار می‌کند: / ، /services/ ، /projects/ و... */
    const clean = s => s.length > 1 && s.endsWith('/') ? s.slice(0, -1) : s;
    const path = clean(window.location.pathname);
    document.querySelectorAll('.nav-link').forEach(l => {
        l.classList.remove('active');
        if (clean(l.getAttribute('href') || '') === path) l.classList.add('active');
    });
}

function initSmoothScroll() {
    if (typeof Lenis === 'undefined') return;
    const canSmooth = window.matchMedia('(hover: hover) and (pointer: fine)').matches;
    const btn = document.getElementById('backToTop');
    const anchors = document.querySelectorAll('a[href^="#"]');
    if (!canSmooth) {
        /* R6: موبایل/تاچ — Lenis اصلاً ساخته نمی‌شود؛ اسکرول بومی + smooth نیتیو */
        if (btn) btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
        anchors.forEach(a => {
            a.addEventListener('click', function(e) {
                const t = document.querySelector(this.getAttribute('href'));
                if (t) { e.preventDefault(); t.scrollIntoView({ behavior: 'smooth', block: 'start' }); }
            });
        });
        return;
    }
    const lenis = new Lenis({ duration: 1.2, easing: t => Math.min(1, 1.001 - Math.pow(2, -10 * t)), direction: 'vertical', gestureDirection: 'vertical', smooth: true, mouseMultiplier: 1, smoothTouch: false, touchMultiplier: 2, infinite: false });
    function raf(time) { lenis.raf(time); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
    if (btn) btn.addEventListener('click', () => lenis.scrollTo(0, { duration: 1.5 }));
    anchors.forEach(a => {
        a.addEventListener('click', function(e) {
            const t = document.querySelector(this.getAttribute('href'));
            if (t) { e.preventDefault(); lenis.scrollTo(t, { offset: -80, duration: 1.5 }); }
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    initTheme(); initPreloader(); initCounters(); initReveal();
    initNavbar(); initBackToTop(); initMobileMenu(); initActiveNav(); initSmoothScroll();
});