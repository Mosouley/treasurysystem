import subprocess

def run_migrations():
    subprocess.run(['python', 'manage.py', 'makemigrations', 'my_app'])
    subprocess.run(['python', 'manage.py', 'migrate'])
