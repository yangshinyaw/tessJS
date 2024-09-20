from flask import Flask, request, jsonify, render_template
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import io

app = Flask(__name__)

# Initialize TrOCR model
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-handwritten")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-base-handwritten")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_text():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    img = Image.open(io.BytesIO(file.read())).convert("RGB")

    # Process the image using TrOCR
    pixel_values = processor(images=img, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    predicted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    return jsonify({'text': predicted_text})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, port=5001)
