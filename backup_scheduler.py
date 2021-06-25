from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import date, datetime
import os
import hashlib


def start_backup():
    date_now = datetime.now()
    date_now = date_now.strftime("%d/%m/%Y %H:%M:%S")
    
    print('=================================================')

    print('Back up started on: ', date_now)

    exec(open('./backup_v2.py').read()) # Read and execute the back up scrip
    

scheduler = BlockingScheduler()
scheduler.add_job(start_backup, 'cron', year = '*', month = '*', day = '*', hour= '13', minute = '11', second = '20')
scheduler.start()
