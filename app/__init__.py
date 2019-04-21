import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel, lazy_gettext as _l
from config import Config
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
login.login_message = _l('Please log in to access this page.')
mail = Mail(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
babel = Babel(app)

admin = Admin(app)

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Microblog Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


@babel.localeselector          #locale selector 指header 選取器   呢個本生係babel入面已有既function,用呢個decorator等你可以加啲野落去個function
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])    #Flask 入面有個request object,object入面有個accept_languages,佢有client 所send request時 既accept languages header(類似咁Accept-Language: da, en-gb;q=0.8, en;q=0.7 個weight 愈大愈優先),佢係一個list 指出client 接受邊啲language 同邊種language最優先 best_match()就係取最優先language,佢係係browser既prefered language度set,預設佢係用你os個語言,所以就算一般人無set,佢都對應到client個language
                                                                            #(app.config['LANGUAGES'])係指當user未能提供個prefer language,你網站會以咩language 顯示

from app import routes, models, errors
