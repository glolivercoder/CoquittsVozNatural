import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if not (3.9 <= sys.version_info.major + sys.version_info.minor/10 < 3.12):
        print("Erro: Python 3.9, 3.10 ou 3.11 é necessário")
        print(f"Versão atual: Python {sys.version_info.major}.{sys.version_info.minor}")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detectado")

def install_espeak():
    """Instala o espeak-ng no sistema"""
    system = platform.system().lower()
    
    if system == "windows":
        print("No Windows, você precisa instalar o espeak-ng manualmente:")
        print("1. Baixe o instalador em: https://github.com/espeak-ng/espeak-ng/releases")
        print("2. Execute o instalador")
        print("3. Adicione o diretório de instalação ao PATH do sistema")
        input("Pressione Enter após instalar o espeak-ng...")
    elif system == "linux":
        subprocess.run(["sudo", "apt-get", "install", "-y", "espeak-ng"], check=True)
    else:
        print(f"Sistema {system} não suportado para instalação automática do espeak-ng")
        print("Por favor, instale manualmente o espeak-ng")

def setup_environment():
    """Configura o ambiente Python"""
    check_python_version()
    
    print("\nInstalando dependências...")
    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    print("\nInstalando espeak-ng...")
    install_espeak()
    
    print("\nAmbiente configurado com sucesso!")

if __name__ == "__main__":
    setup_environment() 