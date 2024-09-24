from flask import render_template, request, flash
from werkzeug.utils import secure_filename

from app import routes_logger
from app import upload_service

def route():
    results = []
    if request.method == 'POST':
        enable_encryption = 'enableEncryption' in request.form
        files = request.files.getlist('files')
        for file in files:
            clean_filename = secure_filename(file.filename)
            try:
                if upload_service.verify(clean_filename):
                    upload_service.upload(file, clean_filename)
                    results.append(f'File successfully uploaded: {clean_filename}')
                else:
                    results.append(f'File type not allowed: {file.filename}')
            except:
                results.append(f"Failed to upload file: {file.filename}")
    return render_template('upload.html', results=results, encryption_enabled=upload_service.encryption_enabled,
                           upload_service_name=type(upload_service).__name__)