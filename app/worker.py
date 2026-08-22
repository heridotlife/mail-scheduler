# -*- coding: utf-8 -*-
"""RQ worker entrypoint.

Replaces the Flask-RQ2 CLI (``flask rq worker``) with a plain RQ worker.
Jobs are executed inside a Flask application context because the job
functions in :mod:`app.event.jobs` use the database session and the
Flask-Mail instance at runtime.

Run with ``python -m app.worker``.
"""

import os

from redis import Redis
from rq import Queue, Worker

from app import config, create_app

settings = os.environ.get("APP_SETTINGS", "DevelopmentConfig")
conf = getattr(config, settings, config.DevelopmentConfig)
app = create_app(conf)

with app.app_context():
    connection = Redis.from_url(app.config["RQ_REDIS_URL"])
    queues = [Queue("default", connection=connection)]
    worker = Worker(queues, connection=connection)
    worker.work()
