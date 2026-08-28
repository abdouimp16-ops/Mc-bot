from apscheduler.schedulers.blocking import BlockingScheduler
import config
from main import run_daily


sched = BlockingScheduler(timezone="UTC")
sched.add_job(run_daily, "cron", hour=config.SIGNAL_HOUR_UTC, minute=0, id="daily_signal")


if __name__ == "__main__":
    print(f"⏰ إشارة يومية عند {config.SIGNAL_HOUR_UTC}:00 UTC")
    run_daily()
    sched.start()
