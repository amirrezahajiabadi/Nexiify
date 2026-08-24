#!/usr/bin/env bash
# ============================================================
# start_tunnel.sh — بالا آوردن خودکار تانل عمومی (pinggy)
# - سرور Django را روی :8471 چک می‌کند (اگه خاموش است بالا می‌آورد)
# - تانل pinggy می‌سازد (بدون ثبت‌نام — از ایران کار می‌کند؛ ngrok از این IP بلاک است)
# - URL عمومی را از لاگ می‌گیرد و نمایش می‌دهد
# نیازمندی: OpenSSH client (ویندوز ۱۰+ به‌صورت پیش‌فرض دارد) + سرور Django
# کاربرد:  ./start_tunnel.sh   (از داخل پوشه‌ی Nexify/)
# ============================================================
set -u
cd "$(dirname "$0")" || exit 1

PORT=8471
PINGGY_LOG="../.freebuff/pinggy.log"
PID_FILE="../.freebuff/pinggy.pid"
URL_RE='https://[a-z0-9-]+\.(run\.pinggy-free\.link|free\.pinggy\.net)'

get_urls() {
    grep -oE "$URL_RE" "$PINGGY_LOG" 2>/dev/null | sort -u
}

# ---------- ۱) مطمئن شو سرور Django بالا است ----------
if curl -s -o /dev/null --max-time 3 "http://127.0.0.1:$PORT/"; then
    echo "✅ Django از قبل روی :$PORT روشن است"
else
    echo "⏳ Django روشن نیست — شروع می‌کنم روی :$PORT ..."
    nohup python manage.py runserver 127.0.0.1:$PORT >> "$PINGGY_LOG" 2>&1 < /dev/null &
    for _ in $(seq 1 25); do
        sleep 1
        curl -s -o /dev/null --max-time 2 "http://127.0.0.1:$PORT/" && break
    done
fi
if curl -s -o /dev/null --max-time 3 "http://127.0.0.1:$PORT/"; then
    echo "✅ Django: فعال"
else
    echo "❌ Django بالا نیامد — خروجی را ببین: $PINGGY_LOG"
    exit 1
fi

# ---------- ۲) اگر تانل قبلی هنوز زنده است، همان را نشان بده ----------
EXISTING=$(get_urls)
if [ -n "$EXISTING" ]; then
    LIVE=""
    for u in $EXISTING; do
        if curl -s -o /dev/null --max-time 8 "$u/"; then LIVE="$u"; break; fi
    done
    if [ -n "$LIVE" ]; then
        echo ""
        echo "=============================================="
        echo " 🔁 تانل قبلی هنوز زنده است:"
        echo "     $LIVE"
        echo "=============================================="
        echo "⏳  مهلت ۶۰ دقیقه‌ای نسخه‌ی رایگان — در صورت نیاز دوباره اجرا کن."
        exit 0
    fi
    echo "⚠️  تانل قبلی مرده است — تازه می‌سازم..."
fi

# ---------- ۳) ساخت تانل تازه ----------
# PID واقعی ویندوز ssh را با مقایسه‌ی قبل/بعد می‌گیریم ($! در Git Bash PID مسی‌ای می‌دهد، نه ویندوزی)
ssh_pids() { tasklist 2>/dev/null | grep -i 'ssh\.exe' | awk '{print $2}' | tr -d '\r'; }
BEFORE_SSH=$(ssh_pids)
echo "🚀 شروع تانل pinggy روی :$PORT ..."
rm -f "$PINGGY_LOG"
nohup ssh -o StrictHostKeyChecking=no -o ServerAliveInterval=30 \
    -o ServerAliveCountMax=3 \
    -p 443 -R0:localhost:$PORT a.pinggy.io > "$PINGGY_LOG" 2>&1 < /dev/null &

NEW_PID=""
for _ in $(seq 1 10); do
    for p in $(ssh_pids); do
        if ! echo "$BEFORE_SSH" | grep -qx "$p"; then NEW_PID="$p"; break; fi
    done
    [ -n "$NEW_PID" ] && break
    sleep 1
done
if [ -n "$NEW_PID" ]; then
    echo "$NEW_PID" > "$PID_FILE"
else
    NEW_PID=$(ssh_pids | tail -1)
    [ -n "$NEW_PID" ] && echo "$NEW_PID" > "$PID_FILE"
fi

# ---------- ۴) صبر کن تا URL ظاهر شود ----------
URLS=""
for _ in $(seq 1 30); do
    sleep 1
    URLS=$(get_urls)
    [ -n "$URLS" ] && break
done

if [ -n "$URLS" ]; then
    echo ""
    echo "=============================================="
    echo " 🌐 تانل زنده است — این لینک را بفرست:"
    echo "$URLS" | sed 's/^/     /'
    echo "=============================================="
    echo "⏳  مهلت: ۶۰ دقیقه (نسخه‌ی رایگان) | آهسته‌تر از ngrok است"
    echo "🛑  بستن تانل:  taskkill //F //PID $(cat "$PID_FILE" 2>/dev/null)"
    echo "    (یا دوباره همین اسکریپت را اجرا کن تا وضعیت را ببینی)"
else
    echo "❌ URL ظاهر نشد — لاگ را ببین:"
    tail -8 "$PINGGY_LOG"
    exit 1
fi
