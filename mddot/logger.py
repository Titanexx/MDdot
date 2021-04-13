import logging

import coloredlogs
import verboselogs

verboselogs.install()
logger = logging.getLogger("mddot")

LEVELS = ["INFO","VERBOSE","DEBUG","SPAM"]

def init_logger(lvl=0):
	coloredlogs.install(level=LEVELS[lvl], logger=logger)

	# # Some examples.
	# logger.spam("this is a spam message")
	# logger.debug("this is a debugging message")
	# logger.verbose("this is a verbose message")
	# logger.info("this is an informational message")
	# logger.warning("this is a warning message")
	# logger.error("this is an error message")
	# logger.critical("this is a critical message")
