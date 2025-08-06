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
prayer_time_dbprayer_time_db