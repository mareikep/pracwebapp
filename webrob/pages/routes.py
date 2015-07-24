from pracWEB.pracinit import pracApp
import os
from os.path import expanduser
import jinja2
import logging
from logging import FileHandler

def register_routes():
    print 'Registering PRAC routes...'
    from webrob.app_and_db import app
    
    pracApp.app = app
    # use html templates from prac app
    prac_loader = jinja2.ChoiceLoader([
        pracApp.app.jinja_loader,
        jinja2.FileSystemLoader(['/opt/practools/tools/prac/pracGUI/pracWEB/templates']),
    ])
    pracApp.app.jinja_loader = prac_loader
    pracApp.app.secret_key = 'so secret!'
    pracApp.app.config['PRAC_STATIC_PATH'] = '/opt/practools/tools/prac/pracGUI/pracWEB/build'

    # settings for fileuploads and logging
    home = expanduser("~")
    pracApp.app.config['ALLOWED_EXTENSIONS'] = set(['mln','db','pracmln'])
    pracApp.app.config['UPLOAD_FOLDER'] = os.path.join(home, 'pracfiles')
    pracApp.app.config['LOG_FOLDER'] = os.path.join(pracApp.app.config['UPLOAD_FOLDER'], 'logs')
    if not os.path.exists(pracApp.app.config['UPLOAD_FOLDER']):
       os.mkdir(pracApp.app.config['UPLOAD_FOLDER'])

    if not os.path.exists(pracApp.app.config['LOG_FOLDER']):
       os.mkdir(pracApp.app.config['LOG_FOLDER'])

    ulog = logging.getLogger('userstats')
    ulog.setLevel(logging.INFO)
    formatter = logging.Formatter("%(message)s,")
    filelogger = FileHandler(os.path.join(pracApp.app.config['LOG_FOLDER'], "userstats.json"))
    filelogger.setFormatter(formatter)
    ulog.addHandler(filelogger)


    from webrob.pages import log
    from pracWEB.pages import inference
    from pracWEB.pages import views
    from pracWEB.pages import utils
