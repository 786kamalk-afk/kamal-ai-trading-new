import logging, sys
from logging.handlers import RotatingFileHandler

def configure_logging(level=logging.INFO, logfile: str | None = 'logs/app.log'):
    fmt = '%(asctime)s %(levelname)s [%(name)s] %(message)s'
    root = logging.getLogger()
    root.setLevel(level)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(logging.Formatter(fmt))
    root.addHandler(ch)
    if logfile:
        fh = RotatingFileHandler(logfile, maxBytes=10_000_000, backupCount=5)
        fh.setLevel(level)
        fh.setFormatter(logging.Formatter(fmt))
        root.addHandler(fh)
