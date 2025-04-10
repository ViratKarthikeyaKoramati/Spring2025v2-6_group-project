import smtplib
import sqlite3
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import pandas as pd
from pathlib import Path
from chat import get_response
import pandas as pd
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, session
USERS_FILE = "users.xlsx"
app = Flask(__name__)
app.secret_key = 'super_secret_key'
ENROLLMENTS_FILE = "enrollments.xlsx"
import pandas as pd
from pathlib import Path

if Path("events.xlsx").exists():
    df = pd.read_excel("events.xlsx")
    print(df.head())  # Check the content
else:
    print("events.xlsx does not exist.")
class Database:

    excel_file = "events.xlsx"
    events_file = "events.xlsx"
    enrollments_file = "enrollments.xlsx"
    feedbacks_file = "feedbacks.xlsx"

    @staticmethod
    def init_files():
        """
        Initialize required Excel files if they don't exist.
        """
        files = {
            "events.xlsx": ["id", "event_title", "event_description", "category", "date", "location",
                            "max_participants"],
            "enrollments.xlsx": ["event_title", "name", "college_name", "college_year", "email"],
            "feedbacks.xlsx": ["Name", "Feedback"],
            "users.xlsx": ["username", "password", "role"],
        }
        for file, columns in files.items():
            if not Path(file).exists():
                pd.DataFrame(columns=columns).to_excel(file, index=False)

    @staticmethod
    def get_data(file_path):
        """
        Load data from an Excel file into a Pandas DataFrame.
        """
        try:
            if Path(file_path).exists():
                return pd.read_excel(file_path)
            else:
                return pd.DataFrame()
        except Exception as e:
            print(f"Error loading data from {file_path}: {e}")
            return pd.DataFrame()

    @staticmethod
    def save_data(file_path, data):
        """
        Save a Pandas DataFrame to an Excel file.
        """
        try:
            data.to_excel(file_path, index=False)
        except Exception as e:
            print(f"Error saving data to {file_path}: {e}")
            raise

    @staticmethod
    def init_files():
        # Ensure events.xlsx exists
        if not Path(Database.events_file).is_file():
            pd.DataFrame(columns=["id", "event_title", "event_description", "category", "date", "location",
                                  "max_participants"]).to_excel(Database.events_file, index=False)

        # Ensure enrollments.xlsx exists
        if not Path(Database.enrollments_file).is_file():
            pd.DataFrame(columns=["event_title", "student_name", "college_name", "college_year", "email"]).to_excel(
                Database.enrollments_file, index=False)

        # Ensure feedbacks.xlsx exists
        if not Path(Database.feedbacks_file).is_file():
            pd.DataFrame(columns=["Feedback"]).to_excel(Database.feedbacks_file, index=False)

    @staticmethod
    def init_db():
        # Ensure the Excel file exists and has the correct structure
        if not Path(Database.excel_file).is_file():
            df = pd.DataFrame(columns=["id", "event_title", "event_description", "category", "date", "location", "max_participants"])
            df.to_excel(Database.excel_file, index=False)



    @staticmethod
    def find_user(username, password):
        try:
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            conn.close()
            return user
        except sqlite3.Error as e:
            print(f"Error finding user: {e}")
            return None

    @staticmethod
    def update_event(updated_event):
        try:
            # Load the Excel file into a DataFrame
            df = pd.read_excel(Database.excel_file)

            # Find the row with the matching ID and update it
            index = df[df['id'] == updated_event['id']].index[0]
            df.at[index, 'event_title'] = updated_event['event_title']
            df.at[index, 'event_description'] = updated_event['event_description']
            df.at[index, 'category'] = updated_event['category']
            df.at[index, 'date'] = updated_event['date']
            df.at[index, 'location'] = updated_event['location']
            df.at[index, 'max_participants'] = updated_event['max_participants']

            # Save the updated DataFrame back to Excel
            df.to_excel(Database.excel_file, index=False)
        except Exception as e:
            print(f"Error updating event: {e}")

    @staticmethod
    def save_event(event_title, event_description, category, date, location, max_participants, created_by='organizer'):
        try:
            # Read existing events or create a new DataFrame
            if Path(Database.excel_file).is_file():
                df = pd.read_excel(Database.excel_file)
            else:
                df = pd.DataFrame(columns=["id", "event_title", "event_description", "category", "date", "location",
                                           "max_participants", "created_by"])

            # Determine the new ID for the event
            new_id = df["id"].max() + 1 if not df.empty else 1

            # Create a new event record as a DataFrame
            new_event = pd.DataFrame([{
                "id": new_id,
                "event_title": event_title,
                "event_description": event_description,
                "category": category,
                "date": date,
                "location": location,
                "max_participants": int(max_participants),
                "created_by": created_by
            }])

            # Concatenate the new event with the existing DataFrame
            df = pd.concat([df, new_event], ignore_index=True)

            # Save the updated DataFrame back to Excel
            df.to_excel(Database.excel_file, index=False)
            return True, "Event created successfully!"
        except Exception as e:
            print(f"Error saving event to Excel: {e}")
            return False, str(e)

    def get_all_enrollments():
        try:
            if Path(Database.enrollments_file).exists():
                return pd.read_excel(Database.enrollments_file).to_dict(orient='records')
            return []
        except Exception as e:
            print(f"Error reading enrollments.xlsx: {e}")
            return []

    @staticmethod
    def get_all_feedback():
        try:
            if Path(Database.feedbacks_file).exists():
                return pd.read_excel(Database.feedbacks_file).to_dict(orient='records')
            return []
        except Exception as e:
            print(f"Error reading feedbacks.xlsx: {e}")
            return []

    @staticmethod
    def get_events():
        try:
            if Path(Database.excel_file).is_file():
                df = pd.read_excel(Database.excel_file)
                print(df)  # Debug print to ensure events are loaded
                return df.to_dict(orient="records")
            else:
                return []
        except Exception as e:
            print(f"Error reading Excel file: {e}")
            return []

def send_thank_you_email(email, event_title):
    try:
        # Email credentials
        sender_email = "sathiyabenin@gmail.com"
        sender_password = "csui gngo phbx byln"
        subject = "Thank You for Enrolling!"

        # Email content
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = email
        message["Subject"] = subject

        body = f"""
        Dear Participant,

        Thank you for enrolling in the event "{event_title}".
        We are thrilled to have you join us!

        Best Regards,
        Event Management Team
        """
        message.attach(MIMEText(body, "plain"))

        # Sending the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        print(f"Email sent successfully to {email}")
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    # Fetch the event details
    events = Database.get_events()
    event = next((e for e in events if e['id'] == event_id), None)

    if not event:
        flash('Event not found.', 'danger')
        return redirect(url_for('manage_events'))

    if request.method == 'POST':
        # Update the event details
        updated_event = {
            'id': event_id,
            'event_title': request.form.get('title'),
            'event_description': request.form.get('description'),
            'category': request.form.get('category'),
            'date': request.form.get('date'),
            'location': request.form.get('location'),
            'max_participants': int(request.form.get('max_participants')),
        }

        Database.update_event(updated_event)
        flash('Event updated successfully.', 'success')
        return redirect(url_for('manage_events'))

    return render_template('edit_event.html', event=event)
@app.route('/enroll_event', methods=['POST'])
def enroll_event():
    event_title = request.form.get('event_title')  # Get event title from the form
    name = request.form.get('name')  # Get the user's name
    college_name = request.form.get('college_name')
    college_year = request.form.get('college_year')
    email = request.form.get('email')  # Get the user's email

    try:
        # Save enrollment data to enrollments.xlsx
        enrollment_data = {
            "event_title": event_title,
            "name": name,
            "college_name": college_name,
            "college_year": college_year,
            "email": email,
        }
        enrollments_file = "enrollments.xlsx"
        df = pd.read_excel(enrollments_file) if Path(enrollments_file).exists() else pd.DataFrame(
            columns=["event_title", "name", "college_name", "college_year", "email"]
        )
        df = pd.concat([df, pd.DataFrame([enrollment_data])], ignore_index=True)
        df.to_excel(enrollments_file, index=False)

        # Send Thank You email
        email_status, email_message = send_thank_you_email(email, event_title)

        if email_status:
            flash(f'Thank you for enrolling in "{event_title}". A confirmation email has been sent to {email}.', 'success')
        else:
            flash(f'Enrollment successful, but the confirmation email failed to send: {email_message}', 'warning')

    except Exception as e:
        flash(f"Error during enrollment: {e}", "danger")

    return redirect(url_for('student_dashboard'))


@app.route('/submit_feedback', methods=['GET', 'POST'])
def submit_feedback():
    return render_template('submit_feedback.html')

@app.route('/save_feedback', methods=['POST'])
def save_feedback():
    name = request.form.get('name')
    feedback = request.form.get('feedback')
    feedback_file = "feedbacks.xlsx"

    try:
        # Load or create the feedback DataFrame
        if Path(feedback_file).exists():
            df = pd.read_excel(feedback_file)
        else:
            df = pd.DataFrame(columns=["Name", "Feedback"])

        # Create a new feedback entry as a DataFrame
        new_feedback = pd.DataFrame([{"Name": name, "Feedback": feedback}])

        # Concatenate the new feedback with the existing DataFrame
        df = pd.concat([df, new_feedback], ignore_index=True)

        # Save back to Excel
        df.to_excel(feedback_file, index=False)
        flash('Thank you for your feedback!', 'success')
    except Exception as e:
        flash(f'Error saving feedback: {e}', 'danger')

    return redirect(url_for('student_dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        try:
            # Load or create the users DataFrame
            df = Database.get_data(USERS_FILE)
            print(f"Loaded DataFrame:\n{df}")

            # Check if the username already exists
            if not df.empty and username in df['username'].values:
                flash('Username already exists. Please choose another.', 'danger')
                return redirect(url_for('register'))

            # Append new user data
            new_user = pd.DataFrame([{"username": username, "password": password, "role": role}])
            df = pd.concat([df, new_user], ignore_index=True)
            print(f"Updated DataFrame:\n{df}")

            # Save updated DataFrame back to the file
            Database.save_data(USERS_FILE, df)
            flash('Registration successful! You can now log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error during registration: {e}", 'danger')
            print(f"Error details: {e}")

    return render_template('register.html')



@app.route('/student_dashboard')
def student_dashboard():
    try:
        if Path(Database.excel_file).is_file():
            events = pd.read_excel(Database.excel_file).to_dict(orient='records')
            print(events)  # Debug log
        else:
            events = []
    except Exception as e:
        print(f"Error reading events.xlsx: {e}")
        events = []

    return render_template('student_dashboard.html', events=events)
@app.route('/view_events')
def view_events():
    events = Database.get_events()
    return render_template('view_events.html', events=events)
@app.route('/view_enrolled_students')
def view_enrolled_students():
    try:
        enrollments_file = "enrollments.xlsx"
        if Path(enrollments_file).exists():
            enrollments = pd.read_excel(enrollments_file).to_dict(orient='records')
        else:
            enrollments = []
    except Exception as e:
        flash(f"Error loading enrollments: {e}", "danger")
        enrollments = []

    return render_template('view_enrolled_students.html', enrollments=enrollments)

@app.route('/apply_event')
def apply_event():
    events = Database.get_events()
    return render_template('apply_event.html', events=events)
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Super Admin Login
        if username == "admin" and password == "admin":
            session['user_id'] = "superadmin"
            session['role'] = "superadmin"
            return redirect(url_for('super_admin_dashboard'))

        # User Login (Excel-Based)
        users_file = "users.xlsx"
        if Path(users_file).is_file():
            df = pd.read_excel(users_file)
            user = df[(df['username'] == username) & (df['password'] == password)]
            if not user.empty:
                session['user_id'] = user.iloc[0]['username']
                session['role'] = user.iloc[0]['role']
                if session['role'] == "organizer":
                    return redirect(url_for('dashboard'))
                elif session['role'] == "student":
                    return redirect(url_for('student_dashboard'))
            else:
                flash("Invalid credentials. Please try again.", "danger")
        else:
            flash("No user database found.", "danger")
    return render_template('login.html')
@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")  # Chatbot interface

@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = get_response(text)  # Get response from the chatbot logic
    return jsonify({"answer": response})

@app.route('/dashboard')
def dashboard():
    if 'role' not in session:
        return redirect(url_for('login'))
    role = session['role']
    if role == 'admin':
        return render_template('admin_dashboard.html')
    if role == 'organizer':
        return render_template('organizer_dashboard.html', user_id=session['user_id'])
    if role == 'student':
        return render_template('student_dashboard.html', user_id=session['user_id'])
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))


@app.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        event_title = request.form.get('title')
        event_description = request.form.get('description')
        event_category = request.form.get('category')
        event_date = request.form.get('date')
        event_location = request.form.get('location')
        event_max_participants = request.form.get('max_participants')

        success, message = Database.save_event(
            event_title,
            event_description,
            event_category,
            event_date,
            event_location,
            event_max_participants
        )
        if success:
            flash(message, 'success')
            return redirect(url_for('manage_events'))
        else:
            flash(message, 'danger')
    return render_template('create_event.html')


@app.route('/manage_events')
def manage_events():
    events = Database.get_events()  # Fetch events from the Excel file
    return render_template('manage_events.html', events=events)


@app.route('/view_feedback')
def view_feedback():
    try:
        feedbacks = Database.get_all_feedback()  # Ensure it reads both Name and Feedback
        return render_template('view_feedback.html', feedbacks=feedbacks)
    except Exception as e:
        flash(f"Error loading feedback: {e}", "danger")
        return render_template('view_feedback.html', feedbacks=[])

@app.route('/super_admin_dashboard')
def super_admin_dashboard():
    if session.get('role') != "superadmin":
        flash("Access denied.", "danger")
        return redirect(url_for('login'))

    try:
        events = Database.get_events()
        enrollments = Database.get_all_enrollments()
        feedbacks = Database.get_all_feedback()

    except Exception as e:
        events, enrollments, feedbacks = [], [], []
        flash(f"Error loading data: {e}", "danger")

    return render_template('super_admin_dashboard.html', events=events, enrollments=enrollments, feedbacks=feedbacks)

@app.route('/view_enrollments')
def view_enrollments():
    """Route to view all enrollments."""
    if 'role' not in session or session['role'] != 'superadmin':  # Corrected role check
        flash('Unauthorized access. Please log in.', 'danger')
        return redirect(url_for('login'))
    try:
        if Path(ENROLLMENTS_FILE).exists():
            enrollments = pd.read_excel(ENROLLMENTS_FILE).to_dict(orient='records')
        else:
            enrollments = []
    except Exception as e:
        flash(f"Error loading enrollments: {e}", "danger")
        enrollments = []

    return render_template('view_enrollment.html', enrollments=enrollments)
@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        feedback_text = request.form['feedback']
        try:
            df = pd.read_excel(Database.feedbacks_file) if Path(Database.feedbacks_file).exists() else pd.DataFrame(columns=["Feedback"])
            df = df.append({"Feedback": feedback_text}, ignore_index=True)
            df.to_excel(Database.feedbacks_file, index=False)
            flash('Feedback submitted successfully.', 'success')
        except Exception as e:
            flash(f"Error saving feedback: {e}", 'danger')
        return redirect(url_for('student_dashboard'))

    return render_template('feedback.html')

if __name__ == '__main__':
    Database.init_db()
    Database.init_files()
    app.run(debug=True)

