from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'

# Load the YOLO model
model = YOLO('model/weight_airnav3_all.pt')

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Perform prediction
            img = cv2.imread(file_path)
            results = model(img)
            bboxes = results[0].boxes.xyxy.cpu().numpy()

            # Draw bounding boxes without labels or probabilities
            for bbox in bboxes:
                x1, y1, x2, y2 = map(int, bbox)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

            # Save the result image
            result_path = os.path.join(app.config['UPLOAD_FOLDER'], 'result_' + filename)
            cv2.imwrite(result_path, img)
            
            return render_template('index.html', result_image=result_path)

    return render_template('index.html', result_image=None)

if __name__ == '__main__':
    app.run(debug=True)
