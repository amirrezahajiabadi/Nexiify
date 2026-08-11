/* ============================================================
   Nexify - نمونه کارها (projects.html)
   فیلتر دسته‌بندی + مودال جزئیات پروژه
   دیتا از data-* های کارت می‌آید که سمت سرور جنگو رندر شده
   (بدون innerHTML — امن در برابر XSS حتی با دیتای داینامیک)

   U3: دسترس‌پذیری مودال —
   - role="dialog" + aria-modal + aria-labelledby
   - Focus trap (Tab/Shift+Tab داخل مودال می‌ماند)
   - فوکوس اولیه روی دکمه‌ی بستن
   - بعد از بستن، فوکوس به دکمه‌ی مبدا برمی‌گردد
   ============================================================ */

/* --- فیلتر دسته‌بندی --- */
const filterBtns = document.querySelectorAll('.filter-btn');
const projectCards = document.querySelectorAll('.project-card');

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;
        projectCards.forEach(card => {
            const cat = card.dataset.category;
            if (filter === 'all' || cat.includes(filter)) {
                card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                card.style.opacity = '1';
                card.style.transform = 'scale(1)';
                card.style.pointerEvents = '';
                card.style.display = '';
            } else {
                card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                card.style.opacity = '0';
                card.style.transform = 'scale(0.95)';
                card.style.pointerEvents = 'none';
            }
        });
    });
});

/* --- مودال جزئیات --- */
const modalOverlay = document.getElementById('modalOverlay');
const modalContent = document.getElementById('modalContent');

/* U3: معناشناسی مودال برای Screen Reader */
modalContent.setAttribute('role', 'dialog');
modalContent.setAttribute('aria-modal', 'true');
modalContent.setAttribute('aria-labelledby', 'modal-title');

let lastTrigger = null;   /* دکمه‌ی مبدا — برای بازگرداندن فوکوس بعد از بستن */

const FOCUSABLE_SELECTOR = 'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])';

function getFocusable(container) {
    return [...container.querySelectorAll(FOCUSABLE_SELECTOR)]
        .filter(n => n.getClientRects().length > 0);
}

function el(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
}

function openModalFromCard(card) {
    const tags = (card.dataset.tags || '').split(',').filter(Boolean);
    const stats = [
        { l: 'زمان', v: card.dataset.duration },
        { l: 'نقش', v: card.dataset.role },
        { l: 'وضعیت', v: card.dataset.status }
    ].filter(s => s.v);

    const closeBtn = el('button', 'modal-close', '✕');
    closeBtn.setAttribute('aria-label', 'بستن');

    const statsWrap = el('div', 'modal-stats');
    stats.forEach(s => {
        const stat = el('div', 'modal-stat');
        stat.appendChild(el('div', 'modal-stat-label', s.l));
        stat.appendChild(el('div', 'modal-stat-value', s.v));
        statsWrap.appendChild(stat);
    });

    const techWrap = el('div', 'modal-tech');
    tags.forEach(t => techWrap.appendChild(el('span', 'project-tag', t)));

    const githubLink = el('a', 'btn btn-primary', 'مشاهده کد منبع ↗');
    if (card.dataset.github) {
        githubLink.href = card.dataset.github;
        githubLink.target = '_blank';
        githubLink.rel = 'noopener';
    }

    const children = [closeBtn];
    if (card.dataset.cover) {
        const cover = el('img', 'modal-cover');
        cover.src = card.dataset.cover;
        cover.alt = card.dataset.title;
        children.push(cover);
    } else {
        /* U2: آیکون SVG کارت را در مودال کلون می‌کنیم (بدون ایموجی و بدون innerHTML) */
        const cardIcon = card.querySelector('.project-visual-icon svg');
        if (cardIcon) {
            const iconWrap = el('div', 'modal-icon');
            iconWrap.appendChild(cardIcon.cloneNode(true));
            children.push(iconWrap);
        } else {
            children.push(el('div', 'modal-icon', card.dataset.icon));
        }
    }
    const title = el('h3', 'modal-title', card.dataset.title);
    title.id = 'modal-title';   /* U3: هدف aria-labelledby مودال */
    children.push(
        title,
        el('p', 'modal-category', card.dataset.cat),
        el('p', 'modal-desc', card.dataset.desc),
        statsWrap,
        techWrap,
        githubLink
    );
    modalContent.replaceChildren(...children);

    /* U3: دکمه‌ی مبدا را برای بازگرداندن فوکوس نگه می‌داریم */
    lastTrigger = card.querySelector('button.project-link') || card;

    modalOverlay.classList.add('open');
    lockScroll();

    /* U3: فوکوس اولیه روی دکمه‌ی بستن */
    closeBtn.focus();
}

function closeModal() {
    modalOverlay.classList.remove('open');
    unlockScroll();
    /* U3: بازگرداندن فوکوس به دکمه‌ی مبدا */
    if (lastTrigger) {
        lastTrigger.focus();
        lastTrigger = null;
    }
}

function isModalOpen() {
    return modalOverlay.classList.contains('open');
}

/* رویدادهای مودال — delegation به‌جای onclick اینلاین */
document.addEventListener('click', (e) => {
    /* دکمه‌ی «جزئیات ←» داخل کارت (نه لینک GitHub) */
    const trigger = e.target.closest('.project-card button.project-link');
    if (trigger) { openModalFromCard(trigger.closest('.project-card')); return; }
    if (e.target.closest('.modal-close') || e.target === modalOverlay) closeModal();
});

/* U3: کیبورد — Esc برای بستن + Focus trap با Tab/Shift+Tab */
document.addEventListener('keydown', (e) => {
    if (!isModalOpen()) return;

    if (e.key === 'Escape') { closeModal(); return; }

    if (e.key === 'Tab') {
        const items = getFocusable(modalContent);
        if (!items.length) { e.preventDefault(); return; }
        const first = items[0];
        const last = items[items.length - 1];

        if (!modalContent.contains(document.activeElement)) {
            /* فوکوس بیرون از مودال افتاده → به داخل برمی‌گردانیم */
            e.preventDefault();
            (e.shiftKey ? last : first).focus();
        } else if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first.focus();
        }
    }
});
