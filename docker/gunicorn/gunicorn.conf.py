# docker/gunicorn/gunicorn.prod.conf.py

# Production specific settings
import multiprocessing
import os

# ============================================
# Server Socket
# ============================================
bind = "unix:/tmp/gunicorn.sock"  # Unix socket for better performance
backlog = 2048

# ============================================
# Workers
# ============================================
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gevent"  # Better for high concurrency
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 120
graceful_timeout = 30
keepalive = 5

# ============================================
# Logging
# ============================================
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "warning"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# ============================================
# Security
# ============================================
user = "www-data"
group = "www-data"
umask = 0o022

# ============================================
# Preload
# ============================================
preload_app = True