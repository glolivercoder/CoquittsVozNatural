from core.tts_engine import TTSEngine
import logging

# Configurar logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_model_loading():
    """Testa o carregamento de diferentes modelos"""
    try:
        engine = TTSEngine()
        
        # Testar VITS
        logger.info("Testando carregamento do modelo VITS (pt-br)")
        success = engine.load_model("VITS", "pt-br")
        logger.info(f"VITS pt-br: {'Sucesso' if success else 'Falha'}")
        
        # Testar XTTS
        logger.info("Testando carregamento do modelo XTTS v2")
        success = engine.load_model("XTTS v2", "multilingual")
        logger.info(f"XTTS v2: {'Sucesso' if success else 'Falha'}")
        
    except Exception as e:
        logger.error(f"Erro durante teste: {e}", exc_info=True)

if __name__ == "__main__":
    test_model_loading() 