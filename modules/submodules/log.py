import logging
import logging.handlers

# Loglama yapılandırması
logger = logging.getLogger("MeteoKitLogger")
logger.setLevel(logging.DEBUG)

# Konsol Handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Dosya Handler
file_handler = logging.handlers.RotatingFileHandler(
    ".log", maxBytes=5 * 1024 * 1024, backupCount=2
)
file_handler.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(message)s"
)
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Logger'a Handler'ları ekle
# logger.addHandler(console_handler)
logger.addHandler(file_handler)
