# test_env.py
import os
from pathlib import Path
from dotenv import load_dotenv

# Caminhos
BASE_DIR = Path(__file__).parent / 'django_rest_main'
env_path = BASE_DIR / 'dotenv_files' / '.env'

print(f"BASE_DIR: {BASE_DIR}")
print(f"env_path: {env_path}")
print(f"Arquivo existe: {env_path.exists()}")

if env_path.exists():
    print("\n--- LENDO ARQUIVO .env ---")
    with open(env_path, 'r') as f:
        print(f.read())
    
    # Carrega o .env
    load_dotenv(env_path, override=True)
    
    print("\n--- VARIÁVEIS CARREGADAS ---")
    print(f"DEBUG: '{os.getenv('DEBUG')}'")
    print(f"SECRET_KEY: '{os.getenv('SECRET_KEY')[:20]}...'")
    print(f"ALLOWED_HOSTS: '{os.getenv('ALLOWED_HOSTS')}'")
    
    # Testa conversão
    debug_value = bool(int(os.getenv('DEBUG', 0)))
    print(f"\nDEBUG convertido: {debug_value}")
    
else:
    print("ERRO: .env não encontrado!")
    # Lista o diretório
    import subprocess
    subprocess.run(['dir', str(BASE_DIR / 'dotenv_files')], shell=True)