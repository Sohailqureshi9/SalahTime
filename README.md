Prayer Time App
This project is a web-based application that allows users to manage their daily prayer times. It provides functionality to set, view, and update prayer times through a simple web interface. The app also supports sending automated messages via WhatsApp through Twilio when a user attempts to call during prayer times.

Features
View Prayer Times: Displays the current prayer times for a user.

Update Prayer Times: Allows users to update their prayer start and end times.

Delete Prayer Times: Allows users to delete individual prayer times.

Current Prayer: Displays the current prayer time, highlighting which prayer is active.

Twilio Integration: Automatically rejects calls and sends WhatsApp messages during prayer times.

Requirements
Python 3.7+

MySQL Database

Twilio Account (for WhatsApp messaging)

Flask Web Framework

mysql-connector Python library for MySQL connection

twilio Python library for Twilio integration

Installation
1. Install Python Dependencies
Clone the repository to your local machine and install the required dependencies.

bash
Copy
git clone https://github.com/your-repo-url.git
cd your-repo-directory
Create a Python virtual environment (optional but recommended):

bash
Copy
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
Install the required libraries using pip:

bash
Copy
pip install -r requirements.txt
Alternatively, if you don't have a requirements.txt, you can manually install the libraries with:

bash
Copy
pip install flask mysql-connector twilio
2. Set Up MySQL Database
Make sure you have MySQL running and set up a database for the app. You can create a database using the following command:

sql
Copy
CREATE DATABASE prayer_time_db;
Run the following SQL scripts to create the necessary tables in your database:

sql
Copy
CREATE TABLE user_prayer_times (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    fajr_start TIME,
    fajr_end TIME,
    zohar_start TIME,
    zohar_end TIME,
    asar_start TIME,
    asar_end TIME,
    maghrib_start TIME,
    maghrib_end TIME,
    esha_start TIME,
    esha_end TIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE call_message_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    prayer_time VARCHAR(50),
    message_sent TEXT,
    call_rejected BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
3. Configure Twilio
Sign up for a Twilio account at Twilio. After creating your account, get your Twilio account_sid, auth_token, and a WhatsApp-enabled Twilio phone number.

Set your account_sid, auth_token, and twilio_whatsapp_number in the app.py:

python
Copy
account_sid = 'your_twilio_account_sid'
auth_token = 'your_twilio_auth_token'
twilio_whatsapp_number = 'your_twilio_whatsapp_number'
4. Configure Your Database Connection
In the app.py, configure your MySQL connection details:

python
Copy
conn = mysql.connector.connect(
    host='127.0.0.1',
    user='root',         # MySQL user
    password='',         # MySQL password
    database='prayer_time_db'
)
5. Run the Application
Run the Flask app:

bash
Copy
python app.py
The app will be available at http://127.0.0.1:5000.

Required Libraries
Here are the key Python libraries and tools used in this project:

1. Flask
Flask is a micro web framework for Python used to build web applications. In this project, Flask handles HTTP requests and serves the web interface.

Install it with:

bash
Copy
pip install flask
2. mysql-connector-python
This library is used to interact with MySQL databases from Python. It allows the app to connect to a MySQL database, run queries, and fetch results.

Install it with:

bash
Copy
pip install mysql-connector
3. Twilio
Twilio provides cloud communication APIs for sending SMS, making phone calls, and sending WhatsApp messages. This project uses Twilio to send WhatsApp messages when users attempt to call during prayer times.

Install it with:

bash
Copy
pip install twilio
Endpoints
1. /get-prayer-times (GET)
Returns the user's stored prayer times.

Response:
json
Copy
{
    "fajr_start": "05:00",
    "fajr_end": "05:30",
    "zohar_start": "12:00",
    "zohar_end": "12:30",
    "asar_start": "15:00",
    "asar_end": "15:30",
    "maghrib_start": "18:00",
    "maghrib_end": "18:30",
    "esha_start": "19:30",
    "esha_end": "20:00"
}
2. /update-prayer-times (POST)
Updates the user's prayer times.

Request Body:
json
Copy
{
    "fajr_start": "05:00",
    "fajr_end": "05:30",
    "zohar_start": "12:00",
    "zohar_end": "12:30",
    "asar_start": "15:00",
    "asar_end": "15:30",
    "maghrib_start": "18:00",
    "maghrib_end": "18:30",
    "esha_start": "19:30",
    "esha_end": "20:00"
}
Response:
json
Copy
{
    "message": "Prayer times updated successfully!"
}
3. /current-prayer-time (GET)
Returns the current active prayer time.

Response:
json
Copy
{
    "prayer": "Fajr",
    "start": "05:00",
    "end": "05:30"
}
4. /delete-prayer-time (POST)
Deletes a specific prayer time.

Request Body:
json
Copy
{
    "prayer": "fajr"
}
Response:
json
Copy
{
    "message": "Fajr time deleted!"
}
5. /twilio-webhook (POST)
Handles incoming calls/messages via Twilio. Sends a WhatsApp message when the user tries to contact during a prayer time.

How it Works
Frontend: The user can input and edit prayer times using an interactive form. The times are stored in the MySQL database.

Backend: The Flask app handles API requests for setting, updating, and retrieving prayer times. It also checks the current time to determine if a prayer time is active and rejects calls during that time.

Twilio Integration: If a call or message comes in during prayer time, the app will send a WhatsApp message notifying the caller that the user is busy praying.

Screenshots
Prayer Time Settings: Allows users to input and update their prayer times.

Current Prayer Time: Displays the active prayer time.

Stored Prayer Times: Shows the stored prayer times and allows users to delete or edit individual times.

License
This project is open-source and available under the MIT License.
