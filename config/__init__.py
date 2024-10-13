from .config import Config
from .local import LocalConfig
from .development import DevelopmentConfig
from .production import ProductionConfig

config = {
    'local': LocalConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    
    'default': Config
}
