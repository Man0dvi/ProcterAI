# from Embeddings import encodings
import cv2
import os
import dlib
import numpy as np


# Path to the directory where aligned faces are saved
aligned_faces_dir = "data/"

# Load aligned faces from the directory
aligned_faces = []
for filename in os.listdir(aligned_faces_dir):
    if filename.endswith(".jpg"):
        face_image = cv2.imread(os.path.join(aligned_faces_dir, filename))
        aligned_faces.append(face_image)

# Now, aligned_faces contains all the aligned faces

color = {"blue":(255,0,0), "red":(0,0,255), "green":(0,255,0), "white":(255,255,255)}
faceCascade = cv2.CascadeClassifier('frontalface.xml')
pose_predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')
face_encoder = dlib.face_recognition_model_v1('dlib_face_recognition_resnet_model_v1.dat')

encodings_dir = "encodings"

def dlib_detector(img):
    dlib_face_detector = dlib.get_frontal_face_detector()
    dlib_face_locations = dlib_face_detector(img)
    return dlib_face_locations


def encodings(img,face_locations,pose_predictor,face_encoder):
    predictors = [pose_predictor(img, face_location) for face_location in face_locations]
    return [np.array(face_encoder.compute_face_descriptor(img, predictor, 1)) for predictor in predictors]


def extract_user_image_ids(filename):
    parts = filename.split(".")
    if len(parts) >= 3:
        user_id = int(parts[1])
        img_id = int(parts[2])
        return user_id, img_id
    else:
        return None, None



user_image_count = {}

for filename in os.listdir(aligned_faces_dir):
    if filename.endswith(".jpg"):
        # Extract user ID and image ID from the filename
        user_id, img_id = extract_user_image_ids(filename)

        if user_id is not None and img_id is not None:
            # Update the image count for this user
            user_image_count[user_id] = user_image_count.get(user_id, 0) + 1

            # Load the image
            face_image = cv2.imread(os.path.join(aligned_faces_dir, filename))

            # Get the face locations
            face_locations = dlib_detector(face_image)

            # Ensure that face_locations is not empty before calling encodings
            if face_locations:
                # Call the encodings function for each image until image count reaches 20
                if user_image_count[user_id] <= 20:
                    # Call the encodings function
                    face_encodings = encodings(face_image, face_locations, pose_predictor, face_encoder)

                    # Create a directory for each user if it doesn't exist
                    user_dir = os.path.join(encodings_dir, f"user_{user_id}")
                    os.makedirs(user_dir, exist_ok=True)

                    # Save the encodings for this user and image
                    encoding_filename = f"encoding_{img_id}.npy"
                    encoding_path = os.path.join(user_dir, encoding_filename)
                    np.save(encoding_path, face_encodings)

                    print(f"Encoding saved for user {user_id}, image {img_id}.")

            else:
                print(f"No faces found in the image for user {user_id}.")

        else:
            print("Invalid filename format: ", filename)

