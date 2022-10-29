class BaseLogFormatter:
    log_fmt = f'%(asctime)s [%(levelname)s]  [%(name)s] %(message)s.  [%(filename)s: %(lineno)d]'
    log_datefmt = '%d-%m-%y %H:%M:%S'
