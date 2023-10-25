from flask import Flask, render_template, request, jsonify
import mysql.connector
import subprocess  # For triggering face recognition
import os
# from flask_sse import sse


# os.chdir('/')

app = Flask(__name__)

# Establish MySQL connection
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='students_db'
)
cursor = db_connection.cursor()

# Counter for captured images
captured_image_count = 0

# Route for registering a student
@app.route('/', methods=['GET', 'POST'])
def register_student():
    global captured_image_count  # Use the global variable for image count

    if request.method == 'POST':
        # Get data from the form
        student_name = request.form['studentName']
        student_id = request.form['studentID']
        password = request.form['password']

        # Insert the data into the database
        cursor.execute("INSERT INTO students (name, student_id, password) VALUES (%s, %s, %s)", (student_name, student_id, password))
        db_connection.commit()

        return "Student registered successfully!"

    return render_template('register.html')

# Add a new route for processing the captured image
# @app.route('/process_image', methods=['POST'])
# def process_image():
#     global captured_image_count  # Use the global variable for image count
#     image_data = request.json.get('image')
#
#     # Process the image data as needed (e.g., face recognition)
#     # You can add your face recognition logic here
#
#     # Example: increment the image count and trigger face recognition after 20 images
#     captured_image_count += 1
#     if captured_image_count >= 20:
#         # Reset the image count for the next student
#         captured_image_count = 0
#         # Trigger face recognition using subprocess
#         subprocess.run(["python", "face_recognition.py"])  # Adjust the command as needed
#
#     return jsonify({'result': 'Image processed successfully'})
@app.route('/run_training', methods=['POST'])
def run_training():
    # Define the path to your Python executable within the virtual environment
    python_path = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\venv\Scripts\python.exe"


    # Define the path to your training_data.py script
    script_path = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\training_data.py"

    try:
        # Run the training_data.py script using the specified Python executable
        result = subprocess.run([python_path, script_path], capture_output=True, text=True, check=True)

        # Print the script's output
        print(result.stdout)
        return "Training script executed successfully."
    except subprocess.CalledProcessError as e:
        # If there's an error running the script, print the error message
        print(e.stderr)
        return "Error executing the training script."


@app.route('/finish', methods=['POST'])
def finish():
    # Define the path to your Python executable within the virtual environment
    python_path = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\venv\Scripts\python.exe"


    # Define the path to your training_data.py script
    script_path = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\face_recognition.py"

    try:
        # Run the training_data.py script using the specified Python executable
        result = subprocess.run([python_path, script_path], capture_output=True, text=True, check=True)

        # Print the script's output
        print(result.stdout)
        return "Recognition script executed successfully."
    except subprocess.CalledProcessError as e:
        # If there's an error running the script, print the error message
        print(e.stderr)
        return "Error executing the training script."
if __name__ == '__main__':
    app.run(debug=True)

# Close the database cursor and connection
cursor.close()
db_connection.close()
