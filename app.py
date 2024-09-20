import os
from flask import Flask, request, jsonify, render_template, send_file
import openpyxl
from openpyxl import Workbook
import tempfile

app = Flask(__name__)

# Set a file size limit of 16 MB for uploads
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Error handler for file size exceeding limit
@app.errorhandler(413)
def handle_large_file(error):
    return jsonify({'error': 'File size exceeds the 16MB limit'}), 413

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save_to_excel', methods=['POST'])
def save_to_excel():
    data = request.json
    if 'words' not in data:
        return jsonify({'error': 'No words provided'}), 400

    words = data['words']
    combined_words = " ".join(words)

    # Create a new Excel workbook in a temporary file
    with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as tmp_file:
        excel_file_path = tmp_file.name

        wb = Workbook()
        ws = wb.active
        ws.title = "Extracted Words"
        ws.cell(row=1, column=1, value=combined_words)

        wb.save(excel_file_path)

    response = send_file(excel_file_path, as_attachment=True, download_name="extracted_words.xlsx")
    
    # Delete the file after sending it to avoid storage accumulation
    os.remove(excel_file_path)

    return response

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5001)
