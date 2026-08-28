from datetime import datetime, timezone
import config
import telegram_bot as tg
from strategy import best_setup
from risk import build_trade


def run_daily():
    print("scan:", datetime.now(timezone.utc))
    setup, top5 = best_setup()
    trade = build_trade(setup) if setup else None

    if trade:
        tg.send(tg.format_signal(trade))
        with open("journal.md", "a", encoding="utf-8") as f:
            f.write(f"| {datetime.now(timezone.utc):%Y-%m-%d} | {trade['symbol']} | "
                    f"{trade['side']} | {trade['entry']:.6f} | {trade['sl']:.6f} | "
                    f"{trade['tp'][1]:.6f} | {trade['score']} | |\n")
    else:
        tg.send(tg.format_no_trade(top5))


if __name__ == "__main__":
    run_daily()
