from flask import Flask, request, jsonify, send_from_directory
import subprocess
import os
import tempfile
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

@app.route('/swagger.json')
def serve_swagger():
    return send_from_directory('.', 'swagger.json')

# Swagger UI Blueprint Configuration
SWAGGER_URL = '/swagger'
API_URL = '/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Pandoc API"
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/convert', methods=['POST'])
def convert():
    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file and allowed_file(file.filename):
        input_format = request.form['input_format']
        output_format = request.form['output_format']

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{input_format}") as temp:
            temp.write(file.read())
            temp_path = temp.name
        
        command = [
            "pandoc",
            "--self-contained", "--standalone",
            "-f", input_format,
            "-t", output_format,
            temp_path
        ]
        
        result = subprocess.run(command, capture_output=True, text=True)

        # Clean up the temporary file
        os.unlink(temp_path)

        if result.returncode != 0:
            return jsonify({"error": str(result.stderr)}), 500

        return jsonify({"converted_content": result.stdout})
    else:
        return jsonify({"error": "Invalid file format: " + file.filename}), 415

def allowed_file(filename):
    # Define allowed file extensions
    ALLOWED_EXTENSIONS = {'doc', 'docx','md', 'pdf', 'htm', 'html', 'txt'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)