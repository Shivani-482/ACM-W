import os
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
TEMPLATE_FOLDER = 'templates'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TEMPLATE_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def predict_with_model(image_path):
    try:
        print(f"Processing image at: {image_path}")
        if "cat" in image_path.lower():
            return {"prediction": "This looks like a cat.", "confidence": 0.95}
        elif "dog" in image_path.lower():
            return {"prediction": "This looks like a dog.", "confidence": 0.90}
        else:
            return {"prediction": "Cannot determine. It's a generic image.", "confidence": 0.50}
    except Exception as e:
        print(f"Error during prediction: {e}")
        return {"prediction": "Error during prediction.", "confidence": 0.0}

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request."}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        prediction_result = predict_with_model(filepath)

        os.remove(filepath)

        return jsonify(prediction_result), 200
    
    return jsonify({"error": "Invalid file type."}), 400

if __name__ == '__main__':
    app.run(debug=True)