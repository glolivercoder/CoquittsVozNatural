import customtkinter as ctk
from gui.main_window import MainWindow
import sys
import os
import traceback

def setup_customtkinter():
    # Configuração do CustomTkinter
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Garantir que o diretório de trabalho está correto
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))
    os.chdir(application_path)

def main():
    try:
        setup_customtkinter()
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        print("Detalhes do erro:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 