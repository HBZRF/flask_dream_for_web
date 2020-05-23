from flask import Flask,render_template,url_for,redirect,request,make_response,g,send_from_directory,flash
from functools import wraps
import time,datetime
from flask import session
#from flask_cors import CORS, cross_origin
from DBoperate import *
import os
import json,math
#from werkzeug import secure_filename
from flask import jsonify
import uuid
from flask import Blueprint

UPLOAD_FOLDER = '/home/python/bussise/static/uploadfile/pictures'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
SERVER_NAME = '0861.info'

bp = Blueprint('dreamapp', __name__,
                        template_folder='templates')
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PERMANENT_SESSION_LIFETIME']=datetime.timedelta(days=7)
app.secret_key = os.urandom(24)
#CORS(app, supports_credentials=True, resources=r'/*')
app.register_blueprint(bp, subdomain='m')


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=80,threaded=True,)

@bp.route
def mainpage():
    return 'dddddd'