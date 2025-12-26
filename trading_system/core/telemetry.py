import sys
from loguru import logger
from pathlib import Path

# Configure Loguru
def setup_logging(log_level="INFO"):
    logger.remove()  # Remove default handler
    
    # Console handler
    logger.add(
        sys.stderr, 
        level=log_level, 
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # File handler (Rotation 100 MB, Retention 10 days)
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logger.add(
        "logs/trading_system.log", 
        rotation="100 MB", 
        retention="10 days", 
        level="DEBUG",
        compression="zip"
    )

    logger.info("Logging initialized")

if __name__ == "__main__":
    setup_logging()
    logger.info("Test log message")
