/* ============================================================
   Nexify - تماس با ما (contact.html)
   سلکت سفارشی + FAQ + اعتبارسنجی فرم
   ارسال واقعی به سرور جنگو انجام می‌شود (CSRF + هانی‌پات سمت سرور)
   ============================================================ */

(function () {
    /* --- سلکت سفارشی --- */
    const selectGroup = document.getElementById('customSelectGroup');
    const hiddenSelect = document.getElementById('id_request_type');
    const selectOptions = document.querySelectorAll('.select-option');
    const selectTrigger = document.getElementById('customSelectTrigger');
    const selectPlaceholder = selectTrigger ? selectTrigger.querySelector('.select-placeholder') : null;

    if (selectGroup && hiddenSelect && selectTrigger && selectOptions.length) {

        function renderSelected(option, setValue) {
            selectOptions.forEach(function (o) { o.classList.remove('selected'); });
            option.classList.add('selected');
            selectPlaceholder.style.display = 'none';
            const existing = selectTrigger.querySelector('.selected-display');
            if (existing) existing.remove();
            const display = document.createElement('span');
            display.className = 'selected-display';
            display.style.cssText = 'display:flex;align-items:center;gap:8px;color:var(--text);';
            /* U2: آیکون SVG از data-svg (سرویس‌ساید — نه ایموجی) */
            const iconSpan = document.createElement('span');
            iconSpan.className = 'select-option-icon';
            if (option.dataset.svg) {
                iconSpan.innerHTML = option.dataset.svg;
            } else {
                iconSpan.textContent = option.dataset.icon;
            }
            display.appendChild(iconSpan);
            display.appendChild(document.createTextNode(' ' + option.dataset.text));
            selectTrigger.insertBefore(display, selectTrigger.querySelector('.select-arrow'));
            if (setValue) hiddenSelect.value = option.dataset.value;
        }

        selectTrigger.addEventListener('click', function (e) {
            e.stopPropagation();
            selectGroup.classList.toggle('open');
        });

        selectOptions.forEach(function (option) {
            option.addEventListener('click', function (e) {
                e.stopPropagation();
                renderSelected(option, true);
                selectGroup.classList.remove('open');
            });
        });

        document.addEventListener('click', function () { selectGroup.classList.remove('open'); });

        /* اگر پس از خطای سرور مقداری انتخاب شده، نمایش آن را همگام کن */
        if (hiddenSelect.value) {
            const selected = Array.from(selectOptions).find(o => o.dataset.value === hiddenSelect.value);
            if (selected) renderSelected(selected, false);
        }
    }

    /* --- روش تماس: تلفن یا تلگرام (فقط یکی نمایش داده می‌شود) --- */
    const methodRadios = document.querySelectorAll('.method-radio');
    const phoneGroup = document.getElementById('phoneGroup');
    const telegramGroup = document.getElementById('telegramGroup');

    function syncMethodGroups() {
        const selected = document.querySelector('.method-radio:checked');
        if (!selected || !phoneGroup || !telegramGroup) return;
        const isTelegram = selected.value === 'telegram';
        phoneGroup.hidden = isTelegram;
        telegramGroup.hidden = !isTelegram;
        /* فیلد متناظر با روش انتخاب‌شده الزامی می‌شود */
        const tgInput = telegramGroup.querySelector('input[name="telegram_id"]');
        const phInput = phoneGroup.querySelector('input[name="phone"]');
        if (tgInput) tgInput.required = isTelegram;
        if (phInput) phInput.required = !isTelegram;
    }

    if (methodRadios.length) {
        methodRadios.forEach(function (r) { r.addEventListener('change', syncMethodGroups); });
        syncMethodGroups();
    }

    /* --- درخشش دنبال‌کننده‌ی موس روی انتخاب‌گر روش تماس (rAF throttle) --- */
    const methodGroupEl = document.getElementById('contactMethodGroup');
    const methodSpotEl = methodGroupEl ? methodGroupEl.querySelector('.method-spot') : null;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const noHover = window.matchMedia('(hover: none)').matches;
    if (methodGroupEl && methodSpotEl && !reduceMotion && !noHover) {
        let rafId = null;
        methodGroupEl.addEventListener('pointermove', function (e) {
            if (rafId !== null) return;
            rafId = requestAnimationFrame(function () {
                const rect = methodGroupEl.getBoundingClientRect();
                methodSpotEl.style.setProperty('--mx', (e.clientX - rect.left) + 'px');
                methodSpotEl.style.setProperty('--my', (e.clientY - rect.top) + 'px');
                rafId = null;
            });
        });
    }

    /* --- FAQ (آکاردئون) ---
       فقط یک کارت می‌تواند باز باشد. بسته‌ها با اتریبیوت hidden (display:none واقعی)
       کاملاً از صفحه/درخت دسترس‌پذیری حذف می‌شوند — در هیچ مرورگری محتوای بسته دیده نمی‌شود. */
    const faqGrid = document.getElementById('faqGrid');
    if (faqGrid) {
        faqGrid.addEventListener('click', function (e) {
            const btn = e.target.closest('.faq-question-btn');
            if (!btn) return;
            const card = btn.closest('.faq-card');
            const wasOpen = card.classList.contains('open');
            /* بستن بقیه‌ی کارت‌ها (با تأخیر تا انیمیشن بستن کامل شود، بعد hidden) */
            document.querySelectorAll('.faq-card.open').forEach(function (c) {
                if (c === card) return;
                c.classList.remove('open');
                const ob = c.querySelector('.faq-question-btn');
                if (ob) ob.setAttribute('aria-expanded', 'false');
                const og = c.querySelector('.faq-answer-grid');
                if (og) setTimeout(function () { if (!c.classList.contains('open')) og.hidden = true; }, 480);
            });
            if (wasOpen) {
                card.classList.remove('open');
                btn.setAttribute('aria-expanded', 'false');
                const grid = card.querySelector('.faq-answer-grid');
                if (grid) setTimeout(function () { if (!card.classList.contains('open')) grid.hidden = true; }, 480);
            } else {
                const grid = card.querySelector('.faq-answer-grid');
                if (grid) {
                    grid.hidden = false;
                    void grid.offsetHeight; /* force reflow تا انیمیشن باز شدن اجرا شود */
                }
                card.classList.add('open');
                btn.setAttribute('aria-expanded', 'true');
            }
        });
    }

    /* --- فرم تماس: اعتبارسنجی قبل از ارسال واقعی به سرور --- */
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function (e) {
            /* هانی‌پات: ربات فیلد مخفی را پر کرده → ساکت رد کن */
            const honeypot = document.getElementById('hpWebsite');
            if (honeypot && honeypot.value.trim() !== '') {
                e.preventDefault();
                return false;
            }
            /* سلکت سفارشی پر نشده → خطا نمایش بده */
            if (hiddenSelect && !hiddenSelect.value) {
                e.preventDefault();
                selectGroup.classList.add('open');
                selectTrigger.style.borderColor = '#ef4444';
                setTimeout(function () { selectTrigger.style.borderColor = ''; }, 2000);
                return false;
            }
            /* اعتبارسنجی مرورگر (minlength, email, ...) */
            if (!contactForm.checkValidity()) {
                e.preventDefault();
                contactForm.reportValidity();
                return false;
            }
            /* در غیر این صورت اجازه بده به سرور جنگو ارسال شود (POST با CSRF) */
        });
    }
})();
