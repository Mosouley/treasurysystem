import os
import socket
import threading
import time
from pathlib import Path
from dotenv import load_dotenv

class EnvironmentManager:
    _instance = None
    _lock = threading.Lock()
    _last_check = 0
    _is_online = True
    CHECK_INTERVAL = 300  # seconds
    
    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.supabase_env_path = os.path.join(self.base_dir, 'env.supabase')
        self.dev_env_path = os.path.join(self.base_dir, 'env.dev')
        self.current_env = None
        self.load_env_file()
    
    def check_connectivity(self):
        """Check if we can connect to Supabase host"""
        current_time = time.time()
        if current_time - self._last_check < self.CHECK_INTERVAL:
            return self._is_online
        
        # Get the Supabase host from env.supabase
        temp_env_path = os.path.join(self.base_dir, 'env.supabase')
        if os.path.exists(temp_env_path):
            load_dotenv(temp_env_path, override=True)
            host = os.getenv('POSTGRES_HOST')
            port = int(os.getenv('POSTGRES_PORT', '6543'))
            
            if host:
                try:
                    # Try to establish a socket connection to check connectivity
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(3)  # 3 second timeout
                    result = sock.connect_ex((host, port))
                    sock.close()
                    self._is_online = (result == 0)
                except Exception:
                    self._is_online = False
            else:
                self._is_online = False
        else:
            self._is_online = False
        
        self._last_check = current_time
        return self._is_online
    
    def load_env_file(self):
        """Load the appropriate environment file based on connectivity"""
        is_online = self.check_connectivity()
        
        if is_online:
            # Use Supabase environment
            env_path = self.supabase_env_path
            self.current_env = 'production'
        else:
            # Use Dev environment
            env_path = self.dev_env_path
            self.current_env = 'development'
        
        # Load the environment variables
        if os.path.exists(env_path):
            load_dotenv(env_path, override=True)
            print(f"Loaded environment from {env_path}")
        else:
            print(f"Warning: Environment file {env_path} not found")
        
        return self.current_env

def load_env_file():
    """Load the appropriate environment file and return the environment mode"""
    env_manager = EnvironmentManager.get_instance()
    return env_manager.load_env_file()

def load_settings():
    """Load settings based on the current environment"""
    env_manager = EnvironmentManager.get_instance()
    return env_manager.current_env
