import pandas as pd
import config
from data import fetch_ohlcv
from indicators import enrich


def score_symbol(symbol: str):
    d1 = enrich(fetch_ohlcv(symbol, config.TREND_TF, 300))
    h4 = enrich(fetch_ohlcv(symbol, config.ENTRY_TF, config.CANDLES))

    if len(d1) < 210 or len(h4) < 210:
        return None

    D, H = d1.iloc[-2], h4.iloc[-2]
    Hp = h4.iloc[-3]

    long_bias = D["close"] > D["ema200"] and D["ema50"] > D["ema200"]
    short_bias = D["close"] < D["ema200"] and D["ema50"] < D["ema200"]

    if not (long_bias or short_bias):
        return None

    side = "LONG" if long_bias else "SHORT"
    checks = {}

    if side == "LONG":
        checks["اتجاه يومي صاعد"] = (D["close"] > D["ema200"], 18)
        checks["سعر فوق EMA50 (4h)"] = (H["close"] > H["ema50"], 12)
        checks["تقاطع/زخم MACD"] = (H["macd"] > H["macd_sig"] and H["macd_hist"] > Hp["macd_hist"], 15)
        checks["RSI في نطاق صحي 45-68"] = (45 <= H["rsi"] <= 68, 12)
        checks["RSI اليومي > 50"] = (D["rsi"] > 50, 8)
        checks["اختراق قمة 20 شمعة"] = (H["close"] >= Hp["swing_high"] * 0.995, 10)
    else:
        checks["اتجاه يومي هابط"] = (D["close"] < D["ema200"], 18)
        checks["سعر تحت EMA50 (4h)"] = (H["close"] < H["ema50"], 12)
        checks["تقاطع/زخم MACD هابط"] = (H["macd"] < H["macd_sig"] and H["macd_hist"] < Hp["macd_hist"], 15)
        checks["RSI في نطاق 32-55"] = (32 <= H["rsi"] <= 55, 12)
        checks["RSI اليومي < 50"] = (D["rsi"] < 50, 8)
        checks["كسر قاع 20 شمعة"] = (H["close"] <= Hp["swing_low"] * 1.005, 10)

    checks["قوة اتجاه ADX > 22"] = (H["adx"] > 22, 13)
    checks["حجم أعلى من المتوسط"] = (H["volume"] > (H["vol_ma"] or 0), 12)

    score = sum(w for ok, w in checks.values() if ok)
    passed = [k for k, (ok, _) in checks.items() if ok]

    return {
        "symbol": symbol,
        "side": side,
        "score": round(score, 1),
        "price": float(H["close"]),
        "atr": float(H["atr"]),
        "adx": round(float(H["adx"]), 1),
        "rsi": round(float(H["rsi"]), 1),
        "reasons": passed,
    }


def best_setup():
    results = []
    for sym in config.SYMBOLS:
        try:
            r = score_symbol(sym)
            if r:
                results.append(r)
        except Exception as e:
            print(f"[skip] {sym}: {e}")

    if not results:
        return None, []

    results.sort(key=lambda x: x["score"], reverse=True)
    top = results[0]
    return (top if top["score"] >= config.MIN_SCORE else None), results[:5]
