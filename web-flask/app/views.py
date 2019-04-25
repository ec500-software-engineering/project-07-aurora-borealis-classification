import os

import cv2
from flask import request, url_for
from flask_login import login_required
from werkzeug.urls import url_parse

from app import app
ALLOWED_EXTENSIONS = set(['png','jpg'])

import time
from datetime import timedelta
app.send_file_max_age_default = timedelta(seconds=5)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

'''
    main page
'''
@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template("index.html")

@app.route('/upload')
def upload():
   return render_template("upload.html")

'''
    upload images
'''

@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      file = request.files['file']
      if file and allowed_file(file.filename):
          filename = file.filename
          basepath = os.path.dirname(__file__)
          filepath = os.path.join(basepath,app.config['UPLOAD_FOLDER'])
          if not os.path.exists(filepath):
              os.mkdir(filepath)
          upload_path = os.path.join(filepath, filename)
          file.save(os.path.join(filepath, filename))
          img = cv2.imread(upload_path)
          testpath = os.path.join(filepath, 'test')
          if not os.path.exists(testpath):
              os.mkdir(testpath)
          cv2.imwrite(os.path.join(testpath,'test.jpg'), img)

          return render_template("uploadsuccess.html",val1=time.time())
      else:
          return "fail"


from app import app
from app.form import LoginForm

'''
    log in function
'''
from flask import render_template, flash, redirect
from flask_login import current_user, login_user
from app.models import User

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


'''
    log out
'''
from flask_login import logout_user

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


from app import db
from app.form import RegistrationForm

# ...

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

