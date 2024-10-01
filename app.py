from flask import Flask, request, jsonify, send_file, render_template
import face_recognition
import pandas as pd
import os
import pickle
from datetime import datetime
from PIL import Image, ImageDraw

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

    attendance_records = {}
    uncertain_students = []
    marked_images = []

    for image in images:
        try:
            image_data = face_recognition.load_image_file(image)
            face_locations = face_recognition.face_locations(image_data)
            face_encodings = face_recognition.face_encodings(image_data, face_locations)

            # Open the image with Pillow to allow drawing later
            pil_image = Image.fromarray(image_data)
            draw = ImageDraw.Draw(pil_image)

            if len(face_locations) == 0:
                uncertain_students.append(f"No faces detected in image: {image.filename}")

            for face_encoding, face_location in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]

                # Mark the attendance if the student is not already recorded
                if name != "Unknown" and name not in attendance_records:
                    attendance_records[name] = {
                        'roll_number': name,
                        'student_name': name,
                        'date': datetime.now().strftime('%Y-%m-%d'),
                        'status': 'P'
                    }

                # Draw rectangle around faces in the image
                top, right, bottom, left = face_location
                if name == "Unknown":
                    draw.rectangle(((left, top), (right, bottom)), outline=(255, 0, 0))  # Red box for unknown faces
                    uncertain_students.append(f"Uncertain face detected in image: {image.filename}")
                else:
                    draw.rectangle(((left, top), (right, bottom)), outline=(0, 255, 0))  # Green box for recognized faces

            # Save the marked image
            marked_image_path = f'static/marked_{image.filename}'
            pil_image.save(marked_image_path)
            marked_images.append(marked_image_path)

        except Exception as e:
            return jsonify({'message': 'Error processing image', 'error': str(e)}), 500

    # Convert the attendance records to a list for DataFrame creation
    attendance_data = list(attendance_records.values())

    # Create Excel file
    df_attendance = pd.DataFrame(attendance_data)
    df_attendance.to_excel('attendance.xlsx', index=False)

    return jsonify({
        'message': 'Attendance Marked',
        'uncertain_students': uncertain_students,
        'marked_images': marked_images
    }), 200

@app.route('/download_excel')
def download_excel():
    return send_file('attendance.xlsx', as_attachment=True)

<<<<<<< HEAD
@app.route('/download_image/<image_filename>')
def download_image(image_filename):
    return send_file(f'static/{image_filename}', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
=======
# if __name__ == '__main__':
#     app.run(debug=True)
>>>>>>> 278facea17b6e5b05bfcdda3ce66fa8fa3b73b7c
