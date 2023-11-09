from datetime import datetime
import config
import sys

def info(x, y):
    print(f"{datetime.now()}   \033[44m\033[30mINFO\033[0m    \033[1m{x:12}:\033[0m {y}", flush=True)

def warn(x, y):
    print(f"{datetime.now()}   \033[43m\033[30mWARN\033[0m    \033[1m{x:12}:\033[0m {y}", flush=True)

def error(x, y):
    print(f"{datetime.now()}   \033[41m\033[30mERROR\033[0m   \033[1m{x:12}:\033[0m {y}", flush=True)

def fatal(x, y):
    print(f"{datetime.now()}   \033[45m\033[30mFATAL\033[0m   \033[1m{x:12}:\033[0m {y}", flush=True)
    sys.exit(1)

def verbose(x, y):
    if config.verboselog == False: return
    print(f"{datetime.now()}   \033[46m\033[30mVERBOSE\033[0m\033[1m {x:12}:\033[0m {y}", flush=True)



