import config


def build_trade(setup: dict):
    if not setup:
        return None

    price, a = setup["price"], setup["atr"]

    if a <= 0:
        return None

    if setup["side"] == "LONG":
        entry = price
        sl = price - config.ATR_SL_MULT * a
        tps = [price + m * a for m in (1.6, 3.2, 5.0)]
    else:
        entry = price
        sl = price + config.ATR_SL_MULT * a
        tps = [price - m * a for m in (1.6, 3.2, 5.0)]

    risk = abs(entry - sl)
    rr = abs(tps[1] - entry) / risk

    if rr < config.MIN_RR:
        return None

    risk_cash = config.ACCOUNT_BALANCE * config.RISK_PERCENT / 100
    size = risk_cash / risk

    return {
        **setup,
        "entry": entry,
        "sl": sl,
        "tp": tps,
        "rr": round(rr, 2),
        "size": size,
        "risk_cash": round(risk_cash, 2),
    }


def fmt(x: float) -> str:
    if x >= 100:
        return f"{x:,.2f}"
    if x >= 1:
        return f"{x:,.4f}"
    return f"{x:.6f}"
