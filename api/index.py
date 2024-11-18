# =============================== IMPORT PACKAGE ===============================
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import io
from PIL import Image
# =============================== IMPORT PACKAGE ===============================

# =============================== READ MODEL ===============================
model = load_model("model_cnn_paprika.h5")
# =============================== READ MODEL ===============================

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes and origins

@app.route('/')
def index():
    return 'Welcome to the model API!'

# =============================== PREDICT ROUTE ===============================
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Check if the image file is in the request
        if 'file' not in request.files:
           return jsonify({"error": "No file part in the request"}), 400

        # Get the file from the request
        file = request.files['file']
        if file.filename == '':
           return jsonify({"error": "No selected file"}), 400

        # Open the uploaded image file
        img = Image.open(io.BytesIO(file.read()))

        # Convert to RGB if the image has an alpha channel
        if img.mode == 'RGBA':
            img = img.convert('RGB')

        # Resize and preprocess the image as expected by the model
        img = img.resize((64,64)) # Resize to match model input size
        img_array = image.img_to_array(img) / 255.0  # Normalize the image
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        print("Image successfully processed")  # Debug: Confirm image processing

        # Make prediction
        prediction = model.predict(img_array)
        class_label = "Healthy" if prediction[0][0] > 0.5 else "Bacterial Spot"
        print(f"Prediction: {class_label}")
        print(f"Prediction value: {prediction[0][0]:.2f}")
        result = {'prediction': class_label,'prediction_value':f"{prediction[0][0]:.2f}"}
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# =============================== PREDICT ROUTE ===============================

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="3000")
