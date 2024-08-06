from flask import Flask, request, jsonify, render_template
import cv2
import numpy as np
from skimage.feature import hog
from sklearn.metrics.pairwise import cosine_similarity
import base64

app = Flask(__name__)

def preprocess_image(image):
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized_image = cv2.resize(grayscale_image, (200, 100))
    denoised_image = cv2.GaussianBlur(resized_image, (5, 5), 0)
    return denoised_image

def extract_hog_features(image):
    features = hog(image, orientations=9, pixels_per_cell=(8, 8),
                   cells_per_block=(2, 2), visualize=False)
    return features

def verify_signature(original_signature, forged_signature):
    preprocessed_original = preprocess_image(original_signature)
    preprocessed_forged = preprocess_image(forged_signature)
    
    original_features = extract_hog_features(preprocessed_original).reshape(1, -1)
    forged_features = extract_hog_features(preprocessed_forged).reshape(1, -1)
    
    similarity_score = cosine_similarity(original_features, forged_features)[0][0]
    
    threshold = 0.9
    
    if similarity_score > threshold:
        return "Signature verified as genuine."
    else:
        return "Signature is possibly forged."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verify', methods=['POST'])
def verify():
    data = request.json
    original_signature_data = data['originalSignature'].split(',')[1]
    forged_signature_data = data['forgedSignature'].split(',')[1]
    
    original_signature = cv2.imdecode(np.frombuffer(base64.b64decode(original_signature_data), np.uint8), -1)
    forged_signature = cv2.imdecode(np.frombuffer(base64.b64decode(forged_signature_data), np.uint8), -1)
    
    result = verify_signature(original_signature, forged_signature)
    
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
