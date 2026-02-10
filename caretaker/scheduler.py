from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os

from caretaker.core.config import get_username
from caretaker.core.github_client import GitHubClient
from caretaker.core.config import get_token, get_base_url
from caretaker.plugins import load_plugins, CareContext
from caretaker.core.reporting import write_json

def start():
    client = GitHubClient(get_token(), get_base_url())
    ctx = CareContext(client, get_username())
    scheduler = BackgroundScheduler()

    def job():
        for p in load_plugins():
            data = p.run(ctx)
            write_json(os.path.join(os.getcwd(), "reports"), f"scheduled_{p.name}", data)

    scheduler.add_job(job, "cron", hour=3)
    scheduler.start()
    return scheduler

