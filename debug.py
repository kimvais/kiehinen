def LOG(level,s):
    import sys
    """Helper function to print log messages"""
    LEVELS = ("ERROR","WARN","NOTICE","INFO","DEBUG","XXX")
    sys.stderr.write("%s: %s\n" % (LEVELS[level],s))
