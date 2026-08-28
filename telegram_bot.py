import requests
import config
from risk import fmt

API = f"https://api.telegram.org/bot{config.TELEGRAM_TOKEN}"


def send(text: str, chat_id: str | None = None):
    r = requests.post(f"{API}/sendMessage", json={
        "chat_id": chat_id or config.CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }, timeout=20)

    if not r.ok:
        print("Telegram error:", r.text)

    return r.ok


def format_signal(t: dict) -> str:
    arrow = "🟢 شراء LONG" if t["side"] == "LONG" else "🔴 بيع SHORT"
    reasons = "\n".join(f" ✓ {r}" for r in t["reasons"])

    return (
        f"<b>⚡ صفقة اليوم — {t['symbol']}</b>\n"
        f"{arrow} | فريم 4H\n"
        f"────────────────────\n"
        f"🎯 <b>الدخول:</b> {fmt(t['entry'])}\n"
        f"🛑 <b>وقف الخسارة:</b> {fmt(t['sl'])}\n"
        f"🏁 <b>هدف 1:</b> {fmt(t['tp'][0])} (اخرج 40%)\n"
        f"🏁 <b>هدف 2:</b> {fmt(t['tp'][1])} (اخرج 40%)\n"
        f"🏁 <b>هدف 3:</b> {fmt(t['tp'][2])} (اترك 20% + وقف متحرك)\n"
        f"────────────────────\n"
        f"📊 نقاط الجودة: <b>{t['score']}/100</b> | R:R = <b>1:{t['rr']}</b>\n"
        f"📈 ADX {t['adx']} | RSI {t['rsi']}\n"
        f"💰 حجم المركز المقترح: {t['size']:.4f} (مخاطرة {t['risk_cash']}$)\n"
        f"────────────────────\n"
        f"<b>أسباب الدخول:</b>\n{reasons}\n\n"
        f"🔒 القاعدة: حرّك الوقف إلى نقطة الدخول بعد الهدف 1.\n"
        f"<i>ليست نصيحة مالية — إدارة المخاطر مسؤوليتك.</i>"
    )


def format_no_trade(top5: list) -> str:
    rows = "\n".join(
        f"{i+1}. {r['symbol']} — {r['score']}/100 ({r['side']})"
        for i, r in enumerate(top5)
    ) or "لا مرشحين"

    return (
        "<b>🕓 تقرير اليوم: لا صفقة</b>\n"
        "لم تتحقق شروط الجودة الكاملة، والانتظار قرار رابح.\n\n"
        f"<b>أقرب المرشحين:</b>\n{rows}"
    )
