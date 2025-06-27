import customtkinter as ctk
from tkinter import messagebox, filedialog
import threading
from core.tts_engine import TTSEngine
from core.model_manager import ModelManager
import os
import json
import pygame
import logging
from typing import Optional, Dict

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configuração de logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Configuração da janela
        self.title("Coqui TTS - Interface Gráfica")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Inicializar engines
        self.tts_engine = TTSEngine()
        self.model_manager = ModelManager()
        
        # Inicializar pygame para áudio
        pygame.mixer.init()
        
        # Estado da aplicação
        self.current_audio_file = None
        self.is_playing = False
        self.training_in_progress = False
        
        # Criar interface
        self.create_widgets()
        self.load_config()
        
    def create_widgets(self):
        # Criar notebook para abas
        self.tabview = ctk.CTkTabview(self, width=1150, height=750)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Criar abas
        self.create_tts_tab()
        self.create_training_tab()
        self.create_models_tab()
        self.create_settings_tab()
        
    def create_tts_tab(self):
        # Aba para síntese de voz
        tab_tts = self.tabview.add("Síntese TTS")
        
        # Frame para seleção de modelo
        model_frame = ctk.CTkFrame(tab_tts)
        model_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(model_frame, text="Modelo:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.model_var = ctk.StringVar()
        self.model_dropdown = ctk.CTkComboBox(
            model_frame,
            variable=self.model_var,
            values=self.get_available_models(),
            width=400,
            command=self.on_model_change
        )
        self.model_dropdown.pack(anchor="w", padx=10, pady=5)
        
        # Frame para clonagem de voz (XTTS)
        self.voice_clone_frame = ctk.CTkFrame(tab_tts)
        self.voice_clone_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(self.voice_clone_frame, text="Clonagem de Voz (XTTS):", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        voice_controls = ctk.CTkFrame(self.voice_clone_frame)
        voice_controls.pack(fill="x", padx=10, pady=5)
        
        self.voice_path_entry = ctk.CTkEntry(voice_controls, placeholder_text="Arquivo de voz para clonagem", width=400)
        self.voice_path_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(voice_controls, text="Procurar", command=self.browse_voice_file, width=100).pack(side="left", padx=5)
        
        # Frame para idioma
        lang_frame = ctk.CTkFrame(tab_tts)
        lang_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(lang_frame, text="Idioma:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.lang_var = ctk.StringVar(value="pt-br")
        lang_options = ctk.CTkFrame(lang_frame)
        lang_options.pack(anchor="w", padx=10, pady=5)
        
        ctk.CTkRadioButton(lang_options, text="Português BR", variable=self.lang_var, value="pt-br").pack(side="left", padx=10)
        ctk.CTkRadioButton(lang_options, text="Inglês", variable=self.lang_var, value="en").pack(side="left", padx=10)
        ctk.CTkRadioButton(lang_options, text="Espanhol", variable=self.lang_var, value="es").pack(side="left", padx=10)
        
        # Frame para texto
        text_frame = ctk.CTkFrame(tab_tts)
        text_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(text_frame, text="Texto para síntese:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.text_input = ctk.CTkTextbox(text_frame, height=150)
        self.text_input.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Frame para controles
        controls_frame = ctk.CTkFrame(tab_tts)
        controls_frame.pack(fill="x", padx=20, pady=10)
        
        # Botões de controle
        button_frame = ctk.CTkFrame(controls_frame)
        button_frame.pack(pady=10)
        
        self.generate_btn = ctk.CTkButton(button_frame, text="Gerar Áudio", command=self.generate_audio, width=120)
        self.generate_btn.pack(side="left", padx=10)
        
        self.play_btn = ctk.CTkButton(button_frame, text="Reproduzir", command=self.play_audio, width=120, state="disabled")
        self.play_btn.pack(side="left", padx=10)
        
        self.stop_btn = ctk.CTkButton(button_frame, text="Parar", command=self.stop_audio, width=120, state="disabled")
        self.stop_btn.pack(side="left", padx=10)
        
        self.save_btn = ctk.CTkButton(button_frame, text="Salvar", command=self.save_audio, width=120, state="disabled")
        self.save_btn.pack(side="left", padx=10)
        
        # Barra de progresso
        self.progress = ctk.CTkProgressBar(controls_frame, width=600)
        self.progress.pack(pady=10)
        self.progress.set(0)
        
        # Status
        self.status_label = ctk.CTkLabel(controls_frame, text="Pronto", font=("Arial", 12))
        self.status_label.pack(pady=5)
        
    def create_training_tab(self):
        # Aba para treinamento
        tab_training = self.tabview.add("Treinamento")
        
        # Frame para dataset
        dataset_frame = ctk.CTkFrame(tab_training)
        dataset_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(dataset_frame, text="Dataset:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Controles do dataset
        dataset_controls = ctk.CTkFrame(dataset_frame)
        dataset_controls.pack(fill="x", padx=10, pady=5)
        
        self.dataset_path = ctk.CTkEntry(dataset_controls, placeholder_text="Caminho do dataset", width=400)
        self.dataset_path.pack(side="left", padx=5)
        
        ctk.CTkButton(dataset_controls, text="Procurar", command=self.browse_dataset, width=100).pack(side="left", padx=5)
        ctk.CTkButton(dataset_controls, text="Validar", command=self.validate_dataset, width=100).pack(side="left", padx=5)
        
        # Frame para configurações de treinamento
        config_frame = ctk.CTkFrame(tab_training)
        config_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(config_frame, text="Configurações de Treinamento:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Grid de configurações
        config_grid = ctk.CTkFrame(config_frame)
        config_grid.pack(fill="x", padx=10, pady=5)
        
        # Modelo base
        ctk.CTkLabel(config_grid, text="Modelo Base:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.base_model_var = ctk.StringVar(value="VITS")
        self.base_model_dropdown = ctk.CTkComboBox(
            config_grid,
            variable=self.base_model_var,
            values=["VITS", "Tacotron2", "FastSpeech2", "XTTS"],
            width=150
        )
        self.base_model_dropdown.grid(row=0, column=1, padx=5, pady=5)
        
        # Epochs
        ctk.CTkLabel(config_grid, text="Epochs:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.epochs_entry = ctk.CTkEntry(config_grid, width=100)
        self.epochs_entry.insert(0, "1000")
        self.epochs_entry.grid(row=0, column=3, padx=5, pady=5)
        
        # Batch Size
        ctk.CTkLabel(config_grid, text="Batch Size:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.batch_size_entry = ctk.CTkEntry(config_grid, width=100)
        self.batch_size_entry.insert(0, "32")
        self.batch_size_entry.grid(row=1, column=1, padx=5, pady=5)
        
        # Learning Rate
        ctk.CTkLabel(config_grid, text="Learning Rate:").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.lr_entry = ctk.CTkEntry(config_grid, width=100)
        self.lr_entry.insert(0, "0.0002")
        self.lr_entry.grid(row=1, column=3, padx=5, pady=5)
        
        # Frame para controles de treinamento
        training_controls = ctk.CTkFrame(tab_training)
        training_controls.pack(fill="x", padx=20, pady=10)
        
        self.start_training_btn = ctk.CTkButton(
            training_controls,
            text="Iniciar Treinamento",
            command=self.start_training,
            width=150
        )
        self.start_training_btn.pack(side="left", padx=10, pady=10)
        
        self.stop_training_btn = ctk.CTkButton(
            training_controls,
            text="Parar Treinamento",
            command=self.stop_training,
            width=150,
            state="disabled"
        )
        self.stop_training_btn.pack(side="left", padx=10, pady=10)
        
        # Frame para log de treinamento
        log_frame = ctk.CTkFrame(tab_training)
        log_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(log_frame, text="Log de Treinamento:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        self.training_log = ctk.CTkTextbox(log_frame, height=200)
        self.training_log.pack(fill="both", expand=True, padx=10, pady=5)
        
    def create_models_tab(self):
        # Aba para gerenciar modelos
        tab_models = self.tabview.add("Modelos")
        
        # Frame para modelos disponíveis
        available_frame = ctk.CTkFrame(tab_models)
        available_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(available_frame, text="Modelos Disponíveis:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Lista de modelos
        self.models_listbox = ctk.CTkScrollableFrame(available_frame, height=300)
        self.models_listbox.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Botões de gerenciamento
        models_controls = ctk.CTkFrame(available_frame)
        models_controls.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkButton(models_controls, text="Baixar Modelo", command=self.download_model, width=120).pack(side="left", padx=5)
        ctk.CTkButton(models_controls, text="Remover Modelo", command=self.remove_model, width=120).pack(side="left", padx=5)
        ctk.CTkButton(models_controls, text="Atualizar Lista", command=self.refresh_models, width=120).pack(side="left", padx=5)
        
    def create_settings_tab(self):
        # Aba para configurações
        tab_settings = self.tabview.add("Configurações")
        
        # Frame para configurações gerais
        general_frame = ctk.CTkFrame(tab_settings)
        general_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(general_frame, text="Configurações Gerais:", font=("Arial", 14, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Diretórios
        dirs_frame = ctk.CTkFrame(general_frame)
        dirs_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(dirs_frame, text="Diretório de Modelos:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.models_dir_entry = ctk.CTkEntry(dirs_frame, width=300)
        self.models_dir_entry.grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkButton(dirs_frame, text="Procurar", command=self.browse_models_dir, width=80).grid(row=0, column=2, padx=5, pady=5)
        
        ctk.CTkLabel(dirs_frame, text="Diretório de Saída:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.output_dir_entry = ctk.CTkEntry(dirs_frame, width=300)
        self.output_dir_entry.grid(row=1, column=1, padx=5, pady=5)
        ctk.CTkButton(dirs_frame, text="Procurar", command=self.browse_output_dir, width=80).grid(row=1, column=2, padx=5, pady=5)
        
        # Botões de configuração
        settings_controls = ctk.CTkFrame(tab_settings)
        settings_controls.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkButton(settings_controls, text="Salvar Configurações", command=self.save_config, width=150).pack(side="left", padx=10)
        ctk.CTkButton(settings_controls, text="Carregar Configurações", command=self.load_config, width=150).pack(side="left", padx=10)
        ctk.CTkButton(settings_controls, text="Resetar", command=self.reset_config, width=100).pack(side="left", padx=10)
    
    # Métodos de funcionalidade
    def get_available_models(self):
        models = []
        for language, model_dict in self.tts_engine.list_available_models().items():
            for model_name in model_dict.keys():
                models.append(f"{model_name} ({language})")
        return models
    
    def on_model_change(self, choice):
        model_name = choice.split(" (")[0]
        model_info = self.tts_engine.get_model_info(model_name)
        
        # Atualizar visibilidade do frame de clonagem de voz
        if model_info.get("support_voice_cloning", False):
            self.voice_clone_frame.pack(fill="x", padx=20, pady=10)
        else:
            self.voice_clone_frame.pack_forget()
        
        self.status_label.configure(text=f"Modelo selecionado: {choice}")
    
    def generate_audio(self):
        text = self.text_input.get("1.0", "end-1c")
        if not text.strip():
            messagebox.showwarning("Aviso", "Digite um texto para síntese")
            return
        
        # Executar geração em thread separada
        thread = threading.Thread(target=self._generate_audio_thread, args=(text,))
        thread.daemon = True
        thread.start()
    
    def _generate_audio_thread(self, text):
        try:
            self.progress.set(0)
            self.status_label.configure(text="Gerando áudio...")
            self.generate_btn.configure(state="disabled")
            
            # Preparar parâmetros
            kwargs = {
                "text": text,
                "output_path": "output.wav",
                "language": self.lang_var.get()
            }
            
            # Adicionar arquivo de voz se necessário
            voice_path = self.voice_path_entry.get()
            if voice_path and os.path.exists(voice_path):
                kwargs["speaker_wav"] = voice_path
            
            # Gerar áudio
            self.current_audio_file = self.tts_engine.generate_speech(**kwargs)
            
            self.status_label.configure(text="Áudio gerado com sucesso!")
            self.play_btn.configure(state="normal")
            self.stop_btn.configure(state="normal")
            self.save_btn.configure(state="normal")
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar áudio: {e}")
            messagebox.showerror("Erro", str(e))
        finally:
            self.generate_btn.configure(state="normal")
            self.progress.set(0)
    
    def play_audio(self):
        if self.current_audio_file and os.path.exists(self.current_audio_file):
            try:
                pygame.mixer.music.load(self.current_audio_file)
                pygame.mixer.music.play()
                self.is_playing = True
                self.play_btn.configure(state="disabled")
                self.stop_btn.configure(state="normal")
            except Exception as e:
                self.logger.error(f"Erro ao reproduzir áudio: {e}")
                messagebox.showerror("Erro", str(e))
    
    def stop_audio(self):
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
            self.play_btn.configure(state="normal")
            self.stop_btn.configure(state="disabled")
    
    def save_audio(self):
        if not self.current_audio_file:
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".wav",
            filetypes=[("Arquivos WAV", "*.wav")],
            initialdir=os.path.dirname(self.current_audio_file)
        )
        
        if file_path:
            try:
                import shutil
                shutil.copy2(self.current_audio_file, file_path)
                self.status_label.configure(text=f"Áudio salvo em: {file_path}")
            except Exception as e:
                self.logger.error(f"Erro ao salvar áudio: {e}")
                messagebox.showerror("Erro", str(e))
    
    def browse_voice_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("Arquivos de Áudio", "*.wav *.mp3 *.ogg"),
                ("Todos os Arquivos", "*.*")
            ]
        )
        if file_path:
            self.voice_path_entry.delete(0, "end")
            self.voice_path_entry.insert(0, file_path)
    
    def browse_dataset(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.dataset_path.delete(0, "end")
            self.dataset_path.insert(0, dir_path)
    
    def validate_dataset(self):
        dataset_path = self.dataset_path.get()
        if not dataset_path:
            messagebox.showwarning("Aviso", "Selecione um diretório de dataset")
            return
            
        try:
            # Implementar validação do dataset
            self.training_log.insert("end", "Validando dataset...\n")
            # TODO: Implementar validação real do dataset
            messagebox.showinfo("Sucesso", "Dataset validado com sucesso!")
        except Exception as e:
            self.logger.error(f"Erro ao validar dataset: {e}")
            messagebox.showerror("Erro", str(e))
    
    def start_training(self):
        if not self.validate_training_params():
            return
            
        self.training_in_progress = True
        self.start_training_btn.configure(state="disabled")
        self.stop_training_btn.configure(state="normal")
        
        # Iniciar treinamento em thread separada
        thread = threading.Thread(target=self._training_thread)
        thread.daemon = True
        thread.start()
    
    def _training_thread(self):
        try:
            # TODO: Implementar treinamento real
            self.training_log.insert("end", "Iniciando treinamento...\n")
            # Simular progresso
            for i in range(10):
                if not self.training_in_progress:
                    break
                self.training_log.insert("end", f"Epoch {i+1}/10\n")
                self.training_log.see("end")
                threading.Event().wait(1.0)
        except Exception as e:
            self.logger.error(f"Erro no treinamento: {e}")
            messagebox.showerror("Erro", str(e))
        finally:
            self.training_in_progress = False
            self.start_training_btn.configure(state="normal")
            self.stop_training_btn.configure(state="disabled")
    
    def stop_training(self):
        self.training_in_progress = False
        self.training_log.insert("end", "Parando treinamento...\n")
    
    def validate_training_params(self) -> bool:
        """Valida parâmetros de treinamento"""
        try:
            epochs = int(self.epochs_entry.get())
            batch_size = int(self.batch_size_entry.get())
            lr = float(self.lr_entry.get())
            
            if epochs <= 0 or batch_size <= 0 or lr <= 0:
                raise ValueError("Valores devem ser positivos")
                
            return True
        except ValueError as e:
            messagebox.showerror("Erro", f"Parâmetros inválidos: {e}")
            return False
    
    def download_model(self):
        # TODO: Implementar download de modelo
        pass
    
    def remove_model(self):
        # TODO: Implementar remoção de modelo
        pass
    
    def refresh_models(self):
        # TODO: Implementar atualização da lista de modelos
        pass
    
    def browse_models_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.models_dir_entry.delete(0, "end")
            self.models_dir_entry.insert(0, dir_path)
    
    def browse_output_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.output_dir_entry.delete(0, "end")
            self.output_dir_entry.insert(0, dir_path)
    
    def save_config(self):
        config = {
            "models_dir": self.models_dir_entry.get(),
            "output_dir": self.output_dir_entry.get(),
            "default_language": self.lang_var.get(),
            "training": {
                "epochs": self.epochs_entry.get(),
                "batch_size": self.batch_size_entry.get(),
                "learning_rate": self.lr_entry.get(),
                "base_model": self.base_model_var.get()
            }
        }
        
        try:
            with open("config/config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            self.status_label.configure(text="Configurações salvas com sucesso!")
        except Exception as e:
            self.logger.error(f"Erro ao salvar configurações: {e}")
            messagebox.showerror("Erro", str(e))
    
    def load_config(self):
        try:
            with open("config/config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                
            self.models_dir_entry.delete(0, "end")
            self.models_dir_entry.insert(0, config.get("models_dir", ""))
            
            self.output_dir_entry.delete(0, "end")
            self.output_dir_entry.insert(0, config.get("output_dir", ""))
            
            self.lang_var.set(config.get("default_language", "pt-br"))
            
            training = config.get("training", {})
            self.epochs_entry.delete(0, "end")
            self.epochs_entry.insert(0, training.get("epochs", "1000"))
            
            self.batch_size_entry.delete(0, "end")
            self.batch_size_entry.insert(0, training.get("batch_size", "32"))
            
            self.lr_entry.delete(0, "end")
            self.lr_entry.insert(0, training.get("learning_rate", "0.0002"))
            
            self.base_model_var.set(training.get("base_model", "VITS"))
            
        except FileNotFoundError:
            self.logger.warning("Arquivo de configuração não encontrado")
        except Exception as e:
            self.logger.error(f"Erro ao carregar configurações: {e}")
            messagebox.showerror("Erro", str(e))
    
    def reset_config(self):
        if messagebox.askyesno("Confirmar", "Deseja resetar todas as configurações?"):
            self.models_dir_entry.delete(0, "end")
            self.output_dir_entry.delete(0, "end")
            self.lang_var.set("pt-br")
            self.epochs_entry.delete(0, "end")
            self.epochs_entry.insert(0, "1000")
            self.batch_size_entry.delete(0, "end")
            self.batch_size_entry.insert(0, "32")
            self.lr_entry.delete(0, "end")
            self.lr_entry.insert(0, "0.0002")
            self.base_model_var.set("VITS") 