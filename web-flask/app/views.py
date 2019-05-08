import os

import cv2
from flask import request, url_for
from flask_login import login_required
from werkzeug.urls import url_parse
import subprocess

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
          call_model()
          y_pred = predition()
          return render_template("uploadsuccess.html",val1=time.time(),li = y_pred)
      else:
          return "fail"

'''
    feature extraction
'''
def call_model():
    task = ['python3', '../tensorflow/TF_FeatureExtraction/example_feat_extract.py',
            '--network', 'inception_v4',
            '--checkpoint', '../tensorflow/checkpoints/inception_v4.ckpt',
            '--image_path', './app/static/images/test',
            '--out_file', './app/static/images/test/auroral_test.h5',
            '--layer_names', 'Logits']
    subprocess.call(task)

from sklearn.linear_model import RidgeClassifier

import h5py
import numpy as np
import pandas as pd


def predition():
    category ={}
    category[0] = 'arc --> one or multiple bands of aurora that stretch across the field-of-view'
    category[1] = 'diffuse --> show large patches of aurora'
    category[2] = 'discrete --> show auroral forms with well-defined, sharp edges,but not arc like'
    category[3] = 'cloudy --> The sky in these images is dominated by clouds'
    category[4] = 'moon --> The image is dominated by light from the Moon'
    category[5] = 'clear sky --> show a clearsky without the appearance of aurora'
    base_dir = "../oath/"
    # read classifications
    df = pd.read_csv(base_dir + "classifications/classifications.csv", skiprows=18)
    ndata = len(df["picNum"])

    f = h5py.File(base_dir + "features/auroral_feat.h5", "r")
    features = f["Logits"].value
    f.close()

    f_test = h5py.File("./app/static/images/test/auroral_test.h5", "r")
    features_test = f_test["Logits"].value
    f_test.close()

    alpha = 0.03

    idxs = np.loadtxt(base_dir + "classifications/train_test_split.csv", delimiter=",").astype(int)
    cnt = 0
    for idx in idxs:
        ntrain = int(np.round(0.7 * ndata))
        idx_train = idx[0:ntrain]

        X_train = features[idx_train, :]
        y_train = df["class6"][idx_train]

        clf = RidgeClassifier(random_state=10 * cnt, normalize=False, alpha=alpha)
        clf.fit(X_train, y_train)

    X_test = features_test
    y_pred = clf.predict(X_test)
    return category[y_pred[0]]


@app.route('/intro')
@login_required
def intro():
    return render_template("intro.html")

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

