import logging
import logging.handlers

LOG_FILENAME = 'RotatingLog.log'
# Set up a specific logger with our desired output level
my_logger = logging.getLogger('RotatingLog')
my_logger.setLevel(logging.DEBUG)

# Add the log message handler to the logger
handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=200, backupCount=2)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s", '%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

# add handler to logger
my_logger.addHandler(handler)

# Log some messages
for i in range(20):
	my_logger.debug('i = %d' % i)
