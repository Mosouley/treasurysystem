import os
import socket
from dotenv import load_dotenv

def is_online():
    try:
        # Try to connect to Supabase
        socket.create_connection(("aws-0-eu-central-1.pooler.supabase.com", 6543), timeout=3)
        return True
    except OSError:
        return False

def load_settings():
    # Always try to load Supabase settings first
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env.supabase')
    
    if not is_online():
        # Fall back to local development settings if offline
        env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env.dev')
        
    load_dotenv(env_file)
    return 'production' if is_online() else 'development'
