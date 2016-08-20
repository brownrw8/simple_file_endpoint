from flask import Flask, request, redirect, render_template, send_from_directory
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)
app.config['API_VERSION'] = '1.0.0'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'storage')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx', 'doc', 'xls', 'xlsx'}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/', methods=['GET'])
def default_documentation():
    return render_template('html/docs.html',
                           version=app.config['API_VERSION']
                           )


@app.route('/config', methods=['GET'])
def config():
    return render_template('html/config.html',
                           version=app.config['API_VERSION'],
                           uploadFolder=app.config['UPLOAD_FOLDER'],
                           maxContentLength=str(app.config['MAX_CONTENT_LENGTH']),
                           allowedExtensions=str(app.config['ALLOWED_EXTENSIONS'])
                           )


@app.route('/ping', methods=['GET'])
def ping():
    return 'Application up and running...'


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'GET':
        return render_template('html/upload.html',
                               version=app.config['API_VERSION']
                               )
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        f = request.files['file']
        if f.filename == '':
            return redirect(request.url)
        if f and allowed_file(f.filename):
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
            return "File uploaded successfully"
        return "An error has occurred while uploading the file"


@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(directory=app.config['UPLOAD_FOLDER'], filename=filename)

