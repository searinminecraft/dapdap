import json
from helper import log

def init():
    global token
    global accentcolor
    global errorcolor
    global owners
    global prefix
    global actuallyShutdown
    global verboselog
    global stealthmode

    with open('config.json', 'r') as f:
        config = json.load(f)

    verboselog = config['verboselog']
    log.verbose('config', 'Initializing globals')
    token = config['token']
    accentcolor = config['accentcolor']
    errorcolor = config['error_accentcolor']
    owners = config['owners']
    prefix = config['prefix']
    stealthmode = config['stealthmode']
    actuallyShutdown = False
