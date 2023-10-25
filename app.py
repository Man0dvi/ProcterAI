from flask import Flask, render_template, request, jsonify
import mysql.connector
import subprocess  # For triggering face recognition

app = Flask(__name__)

# Establish MySQL connection
db_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password='123456',
    database='students_db'
)
cursor = db_connection.cursor()

# Route for registering a student
@app.route('/', methods=['GET', 'POST'])
def register_student():

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


@app.route('/teacher')
def teacher_interface():
    return render_template('teacher.html')

# Route for marking attendance
@app.route('/mark_attendance', methods=['POST'])
def mark_attendance():
    # Define the path to your Python executable within the virtual environment
    python_path = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\venv\Scripts\python.exe"

    # Define the path to your training_data.py script
    script_path = r"C:\Users\mandv\PycharmProjects\AutomatedAttendace\ProcterAI\real_time.py"

    try:
        # Run the training_data.py script using the specified Python executable
        result = subprocess.run([python_path, script_path], capture_output=True, text=True, check=True)

        # Print the script's output
        print(result.stdout)
        return "Real_time script executed successfully."
    except subprocess.CalledProcessError as e:
        # If there's an error running the script, print the error message
        print(e.stderr)
        return "Error executing the real_time script."


if __name__ == '__main__':
    app.run(debug=True)

# Close the database cursor and connection
cursor.close()
db_connection.close()
