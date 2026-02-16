"""
Gunicorn configuration file for goodhare Flask application.
"""

import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "/home/ubuntu/goodhare/_work/goodhare/goodhare/logs/gunicorn_access.log"
errorlog = "/home/ubuntu/goodhare/_work/goodhare/goodhare/logs/gunicorn_error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "goodhare"

# Server mechanics
daemon = False
pidfile = "/home/ubuntu/goodhare/_work/goodhare/goodhare/gunicorn.pid"
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed in future)
# keyfile = None
# certfile = None

