# make a simple flask upload server for testing purposes only

from psutil import disk_usage
from flask import Flask, request, redirect, url_for, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from ftplib import FTP
import shutil
from time import time
import self_img_test
import folder_funcs

from psutil import disk_usage
from time import time
import logging
import ftplib
import urllib

# Configuration
#==========================================
#== If Start from Crontab - wrong path ===
UPLOAD_FOLDER = Path('./Upload').resolve()
ROOT = Path("./static").resolve()
DEFAULT_IMGS_FOLDER = Path("./default_image_folder").resolve()
#==========================================
#== Use instead absolute path =============
#UPLOAD_FOLDER = Path('/home/arkhan/Andrey/ai_ftp/Upload').resolve()
#ROOT = Path('/home/arkhan/Andrey/ai_ftp/static').resolve()
#DEFAULT_IMGS_FOLDER = Path('/home/arkhan/Andrey/ai_ftp/default_image_folder').resolve()
#==========================================
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'webp', 'mp4', 'mp3', 'ogg', 'm4a', 'avi', 'mov', 'zip', 'rar', '7z', 'tar', 'gz', 'iso', 'apk', 'exe', 'msi', 'deb', 'pkg', 'dmg', 'bin', 'bat', 'sh', 'py', 'c', 'cpp',
                         'java', 'js', 'html', 'htm', 'css', 'scss', 'json', 'xml', 'csv', 'xls', 'xlsx', 'doc', 'docx', 'ppt', 'pptx', 'pdf', 'csv', 'db', 'dbf', 'log', 'mdb', 'sav', 'sql', 'tar', 'xml', 'apk', 'bat', 'bin', 'com', 'exe', 'jar', 'ai'])
SIZE_UNITS = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
DOWNLOAD_INTERVAL = 0

#error = "<html><head><title>{status}</title></head><body><center><h1>{status}</h1></center><hr><center>{server}</center></body></html>"

app = Flask(__name__, template_folder=ROOT)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#=========================================================
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
#=========================================================

def get_files(path, sort_by='mtime'):
    """
    Returns a list of all files in the specified directory
    and its subdirectories, including their full paths,
    that are not currently being modified.
    """
    files = []
    current_time = time()
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            stat = os.stat(full_path)
            modified_time = stat.st_mtime if sort_by == 'mtime' else stat.st_ctime
            if (current_time - modified_time) > DOWNLOAD_INTERVAL:
                files.append((full_path, modified_time))
    return sorted(files, key=lambda x: x[1], reverse= True)
#=========================================================

def get_readable_file_size(size_in_bytes):
    if size_in_bytes is None:
        return '0B'
    index = 0
    while size_in_bytes >= 1024:
        size_in_bytes /= 1024
        index += 1
    try:
        return f'{round(size_in_bytes, 2)} {SIZE_UNITS[index]}'
    except IndexError:
        return 'File too large'
#=========================================================

@app.route('/')
def index():
    return (ROOT / 'index.html').resolve().read_bytes() 
#=========================================================

@app.route('/', methods=['POST', 'PUT'])
def upload():
    uploaded_files = request.files.getlist('file')  # Получаем список файлов

    for f in uploaded_files:
        if f.filename == '':
            continue  # Пропускаем пустые файлы

        save_path = UPLOAD_FOLDER / f.filename
        f.save(save_path)

    return redirect("/")    
#=========================================================

@app.route('/', methods=['GET'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded successfully'

#=========================================================

@app.route('/list')
def list_files():
    total, used, free , disk = disk_usage('/')
    files = get_files(UPLOAD_FOLDER, sort_by='mtime')
    file_links = []
    file_names = []
    file_path = []
    file_size = []
    for file in files:
        file_path.append(file[0])
        file_links.append(url_for('download', filename=os.path.basename(file[0])))
        file_names.append(os.path.basename(file[0]))
        size = os.path.getsize(file[0])
        size = get_readable_file_size(size)
        file_size.append(size)
    Avail_Files = len(file_names)
    Avail_Storage = get_readable_file_size(free)
    data = zip(file_names, file_links, file_path, file_size)
    return render_template('list.html', data=data, Avail_Files = Avail_Files, Avail_Storage = Avail_Storage)
#=========================================================

@app.route('/download/<path:filename>', methods=['GET'])
def download(filename):
    """Download a file."""
    logging.info('Downloading file= [%s]', filename)
    logging.info(app.root_path)
    full_path = os.path.join(app.root_path, UPLOAD_FOLDER)
    logging.info(full_path)
    return send_from_directory(full_path, filename, as_attachment=True)
#=========================================================

# @app.route('/delete', methods=['POST'])
# def delete_files():
#     exclude_f_name = 'README.md' #'0.png'
#     file_names = request.form.getlist('delete_file')
#     print('file_names = ', file_names)
#     for file_name in file_names:
#         filepath = Path(file_name)
#         if filepath.isdir(filepath):
#             shutil.rmtree(filepath)
#         else:
#             filepath.unlink()
#     return redirect(url_for('list_files'))

@app.route('/delete', methods=['POST'])
def delete_files():
    exclude_f_name = 'README.md'  # '0.png'
    file_names = request.form.getlist('delete_file')
    print('file_names = ', file_names)
    for file_name in file_names:
        filepath = Path(file_name)
        if filepath.is_dir():
            shutil.rmtree(filepath)
        else:
            filepath.unlink()
    return redirect(url_for('list_files'))    
#=========================================================

@app.route('/delete_all')
def delete_all_files():
    folder_funcs.delete_all_files_in_folder(UPLOAD_FOLDER)
    return redirect(url_for('list_files'))
    #return render_template('list.html')
#=========================================================

@app.route('/restore_default')
def restore_default_images():
    src_folder = DEFAULT_IMGS_FOLDER
    dst_folder = UPLOAD_FOLDER
    copy_folder_contents(src_folder, dst_folder)
    return redirect(url_for('list_files'))  
#=========================================================

@app.route('/assets/<path:filename>')
def send_assets(filename):

    file=ROOT / 'assets' /filename
    if file.exists():
        return file.read_bytes()
    else:
        return error.format(status="404", server=request.url), 404
#=========================================================

@app.route('/test_images')
def test_uploaded_images():
    self_img_test.main() 
    return redirect(url_for('list_files'))
#=========================================================

def copy_folder_contents(src_folder, dst_folder):
    """
    Копирует содержимое из одной указанной папки в другую.

    :param src_folder: Путь к исходной папке.
    :param dst_folder: Путь к целевой папке.
    """
    try:
        if not os.path.exists(dst_folder):
            os.makedirs(dst_folder)

        for item in os.listdir(src_folder):
            src_path = os.path.join(src_folder, item)
            dst_path = os.path.join(dst_folder, item)
            
            if os.path.isdir(src_path):
                shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
            else:
                shutil.copy2(src_path, dst_path)
        
        print('Содержимое успешно скопировано.')
    except Exception as e:
        print(f'Произошла ошибка при копировании содержимого: {e}')
#=========================================================

@app.route('/preview')
def preview():
    file_path = request.args.get('path')
    if not file_path or not Path(file_path).exists():
        return jsonify({'success': False, 'url': ''})

    file_ext = Path(file_path).suffix.lower()
    if file_ext in {'.png', '.jpg', '.jpeg', '.gif', '.webp'}:
        file_url = url_for('download', filename=os.path.basename(file_path))
        return jsonify({'success': True, 'url': file_url})
    else:
        return jsonify({'success': False, 'url': ''})
#=========================================================

def set_working_directory():
    # Определяем путь к директории, в которой находится текущий скрипт
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_directory)
#=========================================================

if __name__ == '__main__':

    set_working_directory()
    # Ваш основной код здесь
    current_directory = os.getcwd()
    print(f"Current directory: {current_directory}")

    app.run(host='0.0.0.0', port=5000, threaded=True, debug=True)
    #app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)
#=========================================================
