import face_recognition
import os
import pickle

# Directory where student images are stored
student_images_dir = 'student_images/'

known_face_encodings = []
known_face_names = []

# Loop through each student's folder
for student_folder in os.listdir(student_images_dir):
    student_path = os.path.join(student_images_dir, student_folder)
    for image_file in os.listdir(student_path):
        image_path = os.path.join(student_path, image_file)
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)

        if face_encoding:
            known_face_encodings.append(face_encoding[0])
            known_face_names.append(student_folder)  # Assuming folder name is the roll number

# Save face encodings to a pickle file
with open('face_encodings.pickle', 'wb') as f:
    pickle.dump(known_face_encodings, f)
    pickle.dump(known_face_names, f)
