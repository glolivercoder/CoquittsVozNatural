import customtkinter as ctk
from gui.main_window import MainWindow
import sys
import os

# Configuração do CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def main():
    try:
        app = MainWindow()
        app.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 