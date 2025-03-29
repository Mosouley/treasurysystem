import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

def load_settings():
    """Load appropriate environment settings based on DJANGO_ENV"""
    env_mode = os.getenv('DJANGO_ENV', 'development')
    
    if env_mode == 'production':
        env_file = 'env.supabase'
    else:
        env_file = 'env.dev'
    
    env_path = os.path.join(BASE_DIR, env_file)
    load_dotenv(dotenv_path=env_path)
    
    return env_mode
