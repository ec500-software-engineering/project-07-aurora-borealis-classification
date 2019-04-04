from flask import Flask,render_template,request
import os

UPLOAD_FOLDER = "data"
ALLOWED_EXTENSIONS = set(['png','jpg'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload')
def upload():
   return render_template('upload.html')

@app.route('/uploaded', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      file = request.files['file']
      if file and allowed_file(file.filename):
          filename = file.filename
          file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
          return 'file uploaded successfully'
      else:
          return "fail"



if __name__ == '__main__':
    app.run(port=5000, debug=True)
