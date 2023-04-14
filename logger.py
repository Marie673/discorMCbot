import yaml
import logging.config
from logging import getLogger
log_config = 'logger.yaml'
logging.config.dictConfig(yaml.load(open(log_config).read(), Loader=yaml.SafeLoader))
logger = getLogger('develop')
