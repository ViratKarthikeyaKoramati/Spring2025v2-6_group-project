from flask import Flask
import os
import pandas as pd

app = Flask(__name__)

# Define paths for Excel database
DATABASE_PATH = 'G:/project code january/EVENT MANAGEMENT SYSTEM/database/college_event_management.xlsx'

# Create initial Excel database if it doesn't exist
def create_initial_database():
    if not os.path.exists(DATABASE_PATH):
        # Create initial empty DataFrames for each table
        user_df = pd.DataFrame(columns=['id', 'username', 'password', 'role'])
        event_df = pd.DataFrame(columns=['id', 'title', 'description', 'category', 'sub_category', 'date', 'location', 'max_participants', 'user_id'])
        registration_df = pd.DataFrame(columns=['id', 'event_id', 'student_id'])
        feedback_df = pd.DataFrame(columns=['id', 'event_id', 'student_id', 'rating', 'feedback_text'])

        # Write DataFrames to Excel file
        with pd.ExcelWriter(DATABASE_PATH) as writer:
            user_df.to_excel(writer, sheet_name='User', index=False)
            event_df.to_excel(writer, sheet_name='Event', index=False)
            registration_df.to_excel(writer, sheet_name='Registration', index=False)
            feedback_df.to_excel(writer, sheet_name='Feedback', index=False)
        print("Excel database created successfully.")

# Create the database when running the script
if __name__ == '__main__':
    create_initial_database()
    app.run(debug=True)
