from flask import Flask, request, jsonify, send_from_directory, Response
from datetime import datetime
import mysql.connector
from twilio.rest import Client
import os

app = Flask(__name__)

# Database connection
def get_db_connection():
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',         # <-- Set your MySQL user
        password='', # <-- Set your MySQL password
        database='prayer_time_db'
    )
    return conn

# Twilio configuration (use environment variables in production)
account_sid = ''
auth_token = ''
client = Client(account_sid, auth_token)
twilio_whatsapp_number = ''

@app.route('/get-prayer-times', methods=['GET'])
def get_prayer_times():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_prayer_times WHERE user_id = 1")
    user_prayer_times = cursor.fetchone()
    cursor.close()
    conn.close()

    def safe_str(val):
        if val is None:
            return ""
        if isinstance(val, str):
            return val
        return val.strftime("%H:%M")

    if user_prayer_times:
        return jsonify({
            "fajr_start": safe_str(user_prayer_times[1]),
            "fajr_end": safe_str(user_prayer_times[2]),
            "zohar_start": safe_str(user_prayer_times[3]),
            "zohar_end": safe_str(user_prayer_times[4]),
            "asar_start": safe_str(user_prayer_times[5]),
            "asar_end": safe_str(user_prayer_times[6]),
            "maghrib_start": safe_str(user_prayer_times[7]),
            "maghrib_end": safe_str(user_prayer_times[8]),
            "esha_start": safe_str(user_prayer_times[9]),
            "esha_end": safe_str(user_prayer_times[10]),
        })
    else:
        return jsonify({})

@app.route('/update-prayer-times', methods=['POST'])
def update_prayer_times():
    conn = get_db_connection()
    cursor = conn.cursor()
    prayers = ['fajr', 'zohar', 'asar', 'maghrib', 'esha']
    cursor.execute("SELECT id FROM user_prayer_times WHERE user_id = 1")
    exists = cursor.fetchone()
    if exists:
        # Update all columns in one query
        update_query = """
            UPDATE user_prayer_times SET
                fajr_start = %s, fajr_end = %s,
                zohar_start = %s, zohar_end = %s,
                asar_start = %s, asar_end = %s,
                maghrib_start = %s, maghrib_end = %s,
                esha_start = %s, esha_end = %s
            WHERE user_id = 1
        """
        values = []
        for prayer in prayers:
            values.append(request.form.get(f"{prayer}_start", None))
            values.append(request.form.get(f"{prayer}_end", None))
        cursor.execute(update_query, tuple(values))
    else:
        # Insert new row
        insert_query = """
            INSERT INTO user_prayer_times (
                user_id, fajr_start, fajr_end,
                zohar_start, zohar_end,
                asar_start, asar_end,
                maghrib_start, maghrib_end,
                esha_start, esha_end
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = [1]
        for prayer in prayers:
            values.append(request.form.get(f"{prayer}_start", None))
            values.append(request.form.get(f"{prayer}_end", None))
        cursor.execute(insert_query, tuple(values))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": "Prayer times updated successfully!"})

@app.route('/current-prayer-time', methods=['GET'])
def current_prayer_time():
    current_time = datetime.now().strftime("%H:%M")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_prayer_times WHERE user_id = 1")
    user_prayer_times = cursor.fetchone()

    cursor.close()
    conn.close()

    def safe_str(val):
        if val is None:
            return ""
        if isinstance(val, str):
            return val
        return val.strftime("%H:%M")

    if user_prayer_times:
        prayer_times = {
            "Fajr": (user_prayer_times[1], user_prayer_times[2]),
            "Zohar": (user_prayer_times[3], user_prayer_times[4]),
            "Asar": (user_prayer_times[5], user_prayer_times[6]),
            "Maghrib": (user_prayer_times[7], user_prayer_times[8]),
            "Esha": (user_prayer_times[9], user_prayer_times[10]),
        }

        for prayer, (start, end) in prayer_times.items():
            if start and end and time_to_datetime(start) <= time_to_datetime(current_time) <= time_to_datetime(end):
                return jsonify({
                    "prayer": prayer,
                    "start": safe_str(start),
                    "end": safe_str(end)
                })

    return jsonify({"prayer": "No prayer time at the moment", "start": "", "end": ""})

def time_to_datetime(time_str):
    return datetime.strptime(time_str, "%H:%M")

def reject_call(call_sid):
    client.calls(call_sid).update(status='completed')
    print("Call rejected!")

def send_whatsapp_message(to, message):
    client.messages.create(
        body=message,
        from_=twilio_whatsapp_number,
        to=to
    )
    print(f"Message sent: {message}")

@app.route('/delete-prayer-time', methods=['POST'])
def delete_prayer_time():
    prayer = request.json.get('prayer')
    if prayer not in ['fajr', 'zohar', 'asar', 'maghrib', 'esha']:
        return jsonify({"message": "Invalid prayer name"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE user_prayer_times SET {prayer}_start = NULL, {prayer}_end = NULL WHERE user_id = 1")
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"message": f"{prayer.capitalize()} time deleted!"})

@app.route('/twilio-webhook', methods=['POST'])
def twilio_webhook():
    from_number = request.form.get('From')
    # Check if it's WhatsApp (Twilio sends 'whatsapp:+1234567890')
    if not from_number or not from_number.startswith('whatsapp:'):
        return Response(status=400)

    # Check if it's prayer time
    current_time = datetime.now().strftime("%H:%M")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user_prayer_times WHERE user_id = 1")
    user_prayer_times = cursor.fetchone()
    cursor.close()
    conn.close()

    def is_prayer_time():
        if user_prayer_times:
            prayer_times = [
                (user_prayer_times[1], user_prayer_times[2]),  # Fajr
                (user_prayer_times[3], user_prayer_times[4]),  # Zohar
                (user_prayer_times[5], user_prayer_times[6]),  # Asar
                (user_prayer_times[7], user_prayer_times[8]),  # Maghrib
                (user_prayer_times[9], user_prayer_times[10])  # Esha
            ]
            now = time_to_datetime(current_time)
            for start, end in prayer_times:
                if start and end:
                    if time_to_datetime(start) <= now <= time_to_datetime(end):
                        return True
        return False

    if is_prayer_time():
        send_whatsapp_message(from_number, "I'm busy in prayer right now. I will get back to you soon, InshaAllah.")
    return Response(status=200)

@app.route('/')
def serve_prayer_times():
    return send_from_directory('.', 'prayer_times.html')

if __name__ == "__main__":
    app.run(debug=True)
