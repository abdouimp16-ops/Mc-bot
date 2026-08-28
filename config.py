import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

ACCOUNT_BALANCE = float(os.getenv("ACCOUNT_BALANCE", 1000))
RISK_PERCENT = float(os.getenv("RISK_PERCENT", 1.5))

EXCHANGE = "binance"
QUOTE = "USDT"

SYMBOLS = [
    "BTC/USDT",
    "ETH/USDT",
    "SOL/USDT",
    "BNB/USDT",
    "XRP/USDT",
    "ADA/USDT",
    "AVAX/USDT",
    "LINK/USDT",
    "DOGE/USDT",
    "TON/USDT",
    "DOT/USDT",
    "NEAR/USDT",
    "ARB/USDT",
    "OP/USDT",
    "INJ/USDT",
    "SUI/USDT",
    "APT/USDT",
    "LTC/USDT",
    "ATOM/USDT",
    "FIL/USDT",
]

ENTRY_TF = "4h"
TREND_TF = "1d"
CANDLES = 400

MIN_SCORE = 72
MIN_RR = 2.5
ATR_SL_MULT = 1.6
SIGNAL_HOUR_UTC = 8
