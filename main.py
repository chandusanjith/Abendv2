import os
from django.core.management import execute_from_command_line

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.settings")

print('type `manage.py help` for help, or hit enter to start server')

while True:
  cmd = input()

  if not cmd:
    cmd = 'manage.py runserver 0.0.0.0:8000'
    execute_from_command_line(cmd.split())
    
  execute_from_command_line(cmd.split())

  print('type a command, hit enter to start server')
