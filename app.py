from flask import Flask, request, jsonify, send_file, render_template
import face_recognition
import pandas as pd
import os
import pickle
from datetime import datetime

app = Flask(__name__)

# Load pre-trained face encodings
with open('face_encodings.pickle', 'rb') as f:
    known_face_encodings = pickle.load(f)
    known_face_names = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'image' not in request.files:
        return jsonify({'message': 'No image uploaded!'}), 400

    images = request.files.getlist('image')

    if not images:
        return jsonify({'message': 'No images found!'}), 400

    attendance_data = []
    uncertain_students = []

    for image in images:
        try:
            image_data = face_recognition.load_image_file(image)
            face_locations = face_recognition.face_locations(image_data)
            face_encodings = face_recognition.face_encodings(image_data, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                attendance_data.append({
                    'roll_number': name if name != "Unknown" else "N/A",
                    'student_name': name,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'status': 'P' if name != "Unknown" else ''
                })

                if name == "Unknown":
                    uncertain_students.append(name)
                    
        except Exception as e:
            return jsonify({'message': 'Error processing image', 'error': str(e)}), 500

    # Create Excel file
    df_attendance = pd.DataFrame(attendance_data)
    df_attendance.to_excel('attendance.xlsx', index=False)

    return jsonify({'message': 'Attendance recorded!', 'uncertain_students': uncertain_students}), 200

@app.route('/download_excel')
def download_excel():
    return send_file('attendance.xlsx', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
