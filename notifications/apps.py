import os
from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        import os
        import sys
        import socket
        
        # Prevent starting the scheduler during management commands (except runserver)
        is_manage_py = any('manage.py' in arg for arg in sys.argv)
        is_runserver = 'runserver' in sys.argv
        
        if is_manage_py and not is_runserver:
            return

        try:
            # Bind to a dedicated port to ensure only one worker starts the scheduler
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", 47200))
            # Keep the socket open to hold the lock
            self.scheduler_lock_socket = sock
            
            from .scheduler import start_scheduler
            start_scheduler()
        except socket.error:
            # Port already in use; another worker has started the scheduler
            pass
