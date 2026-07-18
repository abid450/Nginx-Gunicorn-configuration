import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'inventory.settings')

app = Celery('inventory')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Debug Task --------------------------------------------------------
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
    return f'Task executed successfully with id: {self.request.id}'


"""
# Periodic tasks (Celery Beat)
app.conf.beat_schedule = {
    'cleanup-old-tasks': {
        'task': 'Payment.tasks.cleanup_old_tasks',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
        'options': {
            'expires': 3600,
        },
    },
    
    # Send pending payment reminders (optional)
    'send-pending-reminders': {
        'task': 'Payment.tasks.send_pending_reminder',
        'schedule': crontab(hour=10, minute=0),  # সকাল ১০টা
        'options': {
            'expires': 1800,
        },
    },
}


# Task routes (বিভিন্ন queue তে পাঠানোর জন্য)
app.conf.task_routes = {
    'Payment.tasks.send_payment_confirmation_email': {'queue': 'email'},
    'Payment.tasks.send_pending_reminder': {'queue': 'email'},
    'Payment.tasks.cleanup_expired_transactions': {'queue': 'default'},
    'Payment.tasks.*': {'queue': 'default'},
}
"""

# ============================================================
# TASK QUEUES
# ============================================================

app.conf.task_queues = {
    'default': {
        'exchange': 'default',
        'routing_key': 'default',
    },
    'email': {
        'exchange': 'email',
        'routing_key': 'email',
    },
}


# ============================================================
# TASK SETTINGS
# ============================================================

app.conf.task_time_limit = 30 * 60  # 30 minutes
app.conf.task_soft_time_limit = 25 * 60  # 25 minutes
app.conf.task_max_retries = 3
app.conf.task_default_retry_delay = 60  # 1 minute
app.conf.task_acks_late = True
app.conf.task_track_started = True
app.conf.task_send_sent_event = True