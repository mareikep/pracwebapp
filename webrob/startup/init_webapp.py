from pracweb.gui.app import pracApp
import os
import jinja2
import logging
from logging import FileHandler


def ulogger(name): return logging.getLogger('userstats')

def init_webapp(app, db):
    print 'Initializing PRAC webapp...'

    pracApp.app = app
    # use html templates from prac app
    prac_loader = jinja2.ChoiceLoader([
        pracApp.app.jinja_loader,
        jinja2.FileSystemLoader(['/opt/practools/tools/prac/pracweb/gui/templates']),
    ])
    pracApp.app.jinja_loader = prac_loader
    pracApp.app.config['PRAC_STATIC_PATH'] = '/opt/practools/tools/prac/pracweb/gui/build'

    # settings for fileuploads and logging
    pracApp.app.config['ALLOWED_EXTENSIONS'] = {'mln', 'db', 'pracmln', 'emln'}
    pracApp.app.config['UPLOAD_FOLDER'] = '/home/ros/pracfiles'
    pracApp.app.config['PRAC_ROOT_PATH'] = '/opt/practools/tools/prac'
    pracApp.app.config['LOG_FOLDER'] = os.path.join('/home/ros/pracfiles/prac', 'log')

    if not os.path.exists(pracApp.app.config['LOG_FOLDER']):
        os.mkdir(pracApp.app.config['LOG_FOLDER'])

    # separate logger for user statistics
    root_logger = logging.getLogger('userstats')
    handler = FileHandler(os.path.join(pracApp.app.config['LOG_FOLDER'], "userstats.json"))
    formatter = logging.Formatter("%(message)s,")
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    print 'Registering PRAC routes...'
    from pracweb.gui.pages import inference
    from pracweb.gui.pages import views
    from pracweb.gui.pages import utils