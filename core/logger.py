import logging
import os
from datetime import datetime

class Logger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        self.ensure_log_dir()
        self.setup_logger()
    
    def ensure_log_dir(self):
        """Garante que o diretório de logs existe"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def setup_logger(self):
        """Configura o logger com formato e handlers apropriados"""
        # Nome do arquivo de log com data
        log_file = os.path.join(
            self.log_dir,
            f"coqui_tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        )
        
        # Configuração básica do logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler()  # Para também mostrar no console
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info("Sistema de logging iniciado")
    
    def debug(self, message):
        """Registra mensagem de debug"""
        self.logger.debug(message)
    
    def info(self, message):
        """Registra mensagem informativa"""
        self.logger.info(message)
    
    def warning(self, message):
        """Registra mensagem de aviso"""
        self.logger.warning(message)
    
    def error(self, message, exc_info=None):
        """Registra mensagem de erro"""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message, exc_info=None):
        """Registra mensagem crítica"""
        self.logger.critical(message, exc_info=exc_info)

# Instância global do logger
app_logger = Logger() 