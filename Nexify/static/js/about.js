/* ============================================================
   Nexify - درباره ما (about.html)
   ۱) انیمیشن نوارهای مهارت هنگام اسکرول
   ۲) نور دنبال‌کننده‌ی موس در بخش «ما که هستیم؟»
   ============================================================ */

// ۱) نوارهای مهارت
const skillFills = document.querySelectorAll('.skill-fill');
if (skillFills.length) {
    const skillObs = new IntersectionObserver((entries) => {
        entries.forEach(e => {
            if (e.isIntersecting) e.target.style.width = e.target.dataset.width + '%';
        });
    }, { threshold: 0.3 });
    skillFills.forEach(fill => skillObs.observe(fill));
}

// ۲) نور دنبال‌کننده‌ی موس در بخش «ما که هستیم؟»
// آخرین مختصات موس در متغیرهای بسته‌شده ذخیره می‌شود تا هر فریم از تازه‌ترین موقعیت استفاده کند
// getBoundingClientRect فقط یک‌بار در هر فریم خوانده می‌شود (بدون inline handler — سازگار با CSP)
const aboutHeroGrid = document.querySelector('.about-hero-grid');
if (aboutHeroGrid) {
    let rafId = null;
    let lastX = 0;
    let lastY = 0;
    let hasMove = false;
    aboutHeroGrid.addEventListener('pointermove', (e) => {
        lastX = e.clientX;
        lastY = e.clientY;
        hasMove = true;
        if (rafId) return;
        rafId = requestAnimationFrame(() => {
            rafId = null;
            if (!hasMove) return;
            const rect = aboutHeroGrid.getBoundingClientRect();
            aboutHeroGrid.style.setProperty('--mx', `${lastX - rect.left}px`);
            aboutHeroGrid.style.setProperty('--my', `${lastY - rect.top}px`);
        });
    });
    // نکته: هنگام خروج موس ریست نمی‌شود — افکت با opacity:0 به آرامی محو می‌شود و جای آخر خودش می‌ماند
}
