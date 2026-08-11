/* ============================================================
   Nexify - مقالات (blog_list.html)
   فرم خبرنامه (فعلاً ظاهری — در فاز ۴ به بک‌اند جنگو متصل می‌شود)
   ============================================================ */

const newsletterForm = document.getElementById('newsletterForm');

if (newsletterForm) {
    const newsletterBtn = newsletterForm.querySelector('.btn');
    const newsletterInput = newsletterForm.querySelector('.newsletter-input');

    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();

        if (!newsletterBtn) return;

        const prevText = newsletterBtn.textContent;

        newsletterBtn.textContent = '✓ ثبت شد';
        newsletterBtn.classList.add('btn-success');

        if (newsletterInput) {
            newsletterInput.value = '';
        }

        setTimeout(() => {
            newsletterBtn.textContent = prevText;
            newsletterBtn.classList.remove('btn-success');
        }, 3000);
    });
}
