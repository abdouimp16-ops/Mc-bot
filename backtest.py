import pandas as pd
import config
from data import fetch_ohlcv
from indicators import enrich

LOOKAHEAD = 60


def backtest(symbol: str):
    h4 = enrich(fetch_ohlcv(symbol, "4h", 1000))
    trades = []
    i = 210

    while i < len(h4) - LOOKAHEAD - 1:
        c, p = h4.iloc[i], h4.iloc[i - 1]

        long_ok = (
            c["close"] > c["ema200"]
            and c["close"] > c["ema50"]
            and c["macd"] > c["macd_sig"]
            and c["macd_hist"] > p["macd_hist"]
            and 45 <= c["rsi"] <= 68
            and c["adx"] > 22
            and c["volume"] > (c["vol_ma"] or 0)
        )

        if long_ok and c["atr"] > 0:
            entry = c["close"]
            sl = entry - config.ATR_SL_MULT * c["atr"]
            tp = entry + 3.2 * c["atr"]
            outcome = 0

            for j in range(i + 1, i + LOOKAHEAD):
                if h4.iloc[j]["low"] <= sl:
                    outcome = -1
                    break
                if h4.iloc[j]["high"] >= tp:
                    outcome = 1
                    break

            trades.append(outcome)
            i += 12

        i += 1

    return trades


if __name__ == "__main__":
    allt = []

    for s in config.SYMBOLS:
        try:
            t = backtest(s)
            allt += t
            print(f"{s:12} صفقات={len(t):3} رابحة={t.count(1):3}")
        except Exception as e:
            print(s, "error", e)

    w, l = allt.count(1), allt.count(-1)
    total = w + l

    if total:
        wr = w / total * 100
        R = 3.2 / config.ATR_SL_MULT
        exp = (wr / 100) * R - (1 - wr / 100)
        print(f"\nالإجمالي: {total} | نسبة النجاح: {wr:.1f}% | R لكل هدف: {R:.2f}")
        print(f"التوقع الرياضي لكل صفقة: {exp:.2f}R → "
              f"{'مربح ✅' if exp > 0 else 'خاسر ❌'}")
