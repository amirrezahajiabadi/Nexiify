// پنل ادمین — اسکریپت‌های کمکی (CSP-safe: بدون inline handler)
(function () {
    "use strict";

    // تأیید قبل از حذف — فرم‌هایی با کلاس confirm-form
    document.querySelectorAll("form.confirm-form").forEach(function (form) {
        form.addEventListener("submit", function (e) {
            var msg = form.getAttribute("data-confirm") || "آیا مطمئن هستید؟";
            if (!window.confirm(msg)) {
                e.preventDefault();
            }
        });
    });

    // بستن خودکار پیام‌های موفقیت بعد از ۴ ثانیه
    document.querySelectorAll(".panel-alert").forEach(function (alert) {
        setTimeout(function () {
            alert.classList.add("panel-alert-hide");
            setTimeout(function () { alert.remove(); }, 400);
        }, 4000);
    });

    // پیش‌نمایش زنده‌ی تصویر شاخص (مقالات/پروژه‌ها) — CSP-safe
    document.querySelectorAll("input[type='file']").forEach(function (input) {
        input.addEventListener("change", function () {
            var file = input.files && input.files[0];
            var preview = document.getElementById("coverPreview");
            if (!preview || !file) return;
            var img = preview.querySelector(".cover-preview-img");
            var ph = preview.querySelector(".cover-preview-placeholder");
            if (!img || !file.type.startsWith("image/")) return;
            img.src = URL.createObjectURL(file);
            img.hidden = false;
            img.removeAttribute("data-current");
            if (ph) ph.hidden = true;
        });
    });
})();
