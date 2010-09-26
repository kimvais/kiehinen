import logging

def xxx(s):
    pass

logging.basicConfig(level=logging.DEBUG)
LEVELS = ("ERROR","WARN","NOTICE","INFO","DEBUG","XXX")
facilities = (
        logging.error,    # 0
        logging.warn,     # 1
        logging.info,     # 2
        logging.debug,    # 3
        xxx               # 4
        )

def LOG(level,s):
    import sys
    """Helper function to print log messages"""
    #sys.stderr.write("%s: %s\n" % (LEVELS[level],s))
    facilities[level](s)
