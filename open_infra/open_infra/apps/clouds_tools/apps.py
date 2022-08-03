from django.apps import AppConfig

import datetime
from clouds_tools.resources.scan_thread import ScanThreadTools
from open_infra.utils.common import runserver_executor
from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler


class CloudsToolsConfig(AppConfig):
    name = 'clouds_tools'
    _scheduler = BackgroundScheduler()

    @classmethod
    def _start_thread(cls):
        cls._scheduler.add_job(ScanThreadTools.clear_yaml, 'date', run_date=datetime.datetime.now())
        cls._scheduler.add_job(ScanThreadTools.scan_obs, 'date', run_date=datetime.datetime.now())
        cls._scheduler.add_job(ScanThreadTools.scan_port, 'date', run_date=datetime.datetime.now())
        cls._scheduler.add_job(ScanThreadTools.clear_yaml, 'cron', hour='0')
        cls._scheduler.add_job(ScanThreadTools.scan_obs, 'cron', hour='1')
        cls._scheduler.add_job(ScanThreadTools.scan_port, 'cron', hour='2')
        cls._scheduler.start()

    def start_thread(self):
        th = Thread(target=self._start_thread)
        th.start()

    @runserver_executor
    def ready(self):
        self.start_thread()
