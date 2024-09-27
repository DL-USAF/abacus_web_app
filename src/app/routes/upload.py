from flask import render_template, request, flash
from werkzeug.utils import secure_filename

from app import routes_logger
from app import upload_service


def route():
    results = []
    enable_encryption_selected = 'enableEncryption' in request.form
    datatype = request.form['datatype'] if 'datatype' in request.form else None
    routes_logger.debug(f"{datatype} selected as datatype.")
    routes_logger.debug(f"Encryption Enabled: {enable_encryption_selected}")

    if request.method == 'POST':
        # TODO currently, the enable encryption variable is not utilized
        # I will create a story to implement this with dynamic encryption algorithms
        files = request.files.getlist('files')
        for file in files:
            clean_filename = secure_filename(file.filename)
            try:
                if upload_service.verify(clean_filename):
                    upload_service.upload(file, clean_filename, datatype)
                    results.append(f'File successfully uploaded: {clean_filename}')
                else:
                    results.append(f'File type not allowed: {file.filename}')
            except Exception as e:
                results.append(f"Failed to upload file: {file.filename}")
                routes_logger.error(e)
    return render_template('upload.html',
                           datatypes=upload_service.get_list_of_datatypes(),
                           datatype=datatype,
                           results=results, encryption_enabled=upload_service.encryption_enabled,
                           upload_service_name=type(upload_service).__name__,
                           encryption_selected=enable_encryption_selected)