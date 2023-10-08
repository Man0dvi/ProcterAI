import cv2
import dlib
import os
import numpy as np


encodings_dir = "encodings"
detected_faces_dir = "detected_faces"
pose_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_encoder = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')
recognized_faces = []
stored_encodings = {}


def encodings(img,face_locations,pose_predictor,face_encoder):
    predictors = [pose_predictor(img, face_location) for face_location in face_locations]
    return [np.array(face_encoder.compute_face_descriptor(img, predictor, 1)) for predictor in predictors]


# Load stored encodings
for user_id_folder in os.listdir(encodings_dir):
    user_id = int(user_id_folder.split('_')[1])
    stored_encodings[user_id] = []

    # Load each encoding file for the user
    for encoding_filename in os.listdir(os.path.join(encodings_dir, user_id_folder)):
        if encoding_filename.startswith("encoding_") and encoding_filename.endswith(".npy"):
            encoding_path = os.path.join(encodings_dir, user_id_folder, encoding_filename)
            encoding = np.load(encoding_path)
            stored_encodings[user_id].append(encoding)

for user_id in stored_encodings:
    stored_encodings[user_id] = np.array(stored_encodings[user_id])


def dlib_detector(img):
    dlib_face_detector = dlib.get_frontal_face_detector()
    dlib_face_locations = dlib_face_detector(img)
    return dlib_face_locations


def save_detected_faces(img, face_locations):
    for i, face_location in enumerate(face_locations):
        top, right, bottom, left = face_location.top(), face_location.right(), face_location.bottom(), face_location.left()
        face_image = img[top:bottom, left:right]
        cv2.imwrite(f"{detected_faces_dir}/detected{i + 1}.jpg", face_image)


def calculate_recognized_users(detected_face_encodings):

    recognized_faces = []
    for detected_face_name, detected_encoding in detected_face_encodings.items():
        min_distance = float('inf')
        recognized_user = None

        # Iterate through stored encodings for each user
        for user_id, stored_user_encodings in stored_encodings.items():
            # Calculate the Euclidean distance between detected encoding and each stored encoding
            distances = np.linalg.norm(detected_encoding - stored_user_encodings, axis=1)
            print(distances)
            avg_distance = np.mean(distances)

            # Check if this is the minimum distance so far
            if avg_distance < min_distance:
                min_distance = avg_distance
                recognized_user = user_id
                detected_face = detected_face_name

        if min_distance < 0.1:  # Adjust the threshold as needed
            recognized_faces.append(
                {"detected_face": detected_face, "recognized_user": recognized_user, "distance": min_distance})
        else:
            recognized_faces.append(
                {"detected_face": detected_face, "recognized_user": None, "distance": min_distance})

    return recognized_faces


# Create detected_faces directory if it doesn't exist
os.makedirs(detected_faces_dir, exist_ok=True)

# Capturing real-time video stream. 0 for built-in web-cams, 0 or -1 for external web-cams
video_capture = cv2.VideoCapture(0)

# Initialize a flag to determine when to stop processing faces
save_faces = True

# Initialize a dictionary to store encodings for each detected face
detected_face_encodings = {}

while True:
    _, img = video_capture.read()
    cv2.imshow("face detection", img)
    # Call method we defined above
    face_locations = dlib_detector(img)

    if len(face_locations) > 0 and save_faces:

        save_detected_faces(img, face_locations)

        # Iterate through each detected face
        for i, face_location in enumerate(face_locations):

            face_image = img[face_location.top():face_location.bottom(), face_location.left():face_location.right()]
            # Get the face encodings for the detected face
            encoding = encodings(face_image, [face_location], pose_predictor, face_encoder)[
                0]  # Assuming a single face is detected
            # Store the encoding in the dictionary
            detected_face_encodings[f"detected{i + 1}"] = encoding

        save_faces = False  # Stop saving faces after this frame
        print("Detected face encodings:")
        for key, encoding in detected_face_encodings.items():
            print(f"{key}: {encoding}")

        # Writing processed image in a new window
        recognized_faces = calculate_recognized_users(detected_face_encodings)
        print("Recognized users:", recognized_faces)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# releasing web-cam
video_capture.release()
# Destroying the output window
cv2.destroyAllWindows()





