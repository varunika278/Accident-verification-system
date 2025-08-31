import mysql.connector
from datetime import datetime

def read_status_report(filename="status_report.txt"):
    # Create a dictionary to store the latest values
    latest_values = {}
    
    with open(filename, "r") as file:
        for line in file:
            line = line.strip()
            # Skip empty lines
            if not line:
                continue
                
            # Check if the line contains the expected delimiter
            if ": " not in line:
                continue
                
            parts = line.split(": ", 1)  # Split only on the first occurrence of ": "
            if len(parts) < 2:
                continue
                
            key, value = parts
            # Store the latest value for each key, overwriting any previous values
            latest_values[key] = value
    
    # Return the values in the required format, using the latest values
    return (
        latest_values.get("car_number", "Unknown"),
        latest_values.get("Time_of_Drowsiness", datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
        latest_values.get("Cause of drowsiness", "Unknown"),
        "yes" if latest_values.get("Accident_or_not", "no") == "yes" else "no",
        "yes" if latest_values.get("Insurance Status", "Rejected") == "Approved" else "no"
    )

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",  # Change 'root' to 'localhost'
        user="root",  # Your MySQL username
        password="1234",  # Your MySQL password
    )

def setup_database():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS insurance")
    cursor.execute("USE insurance")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS claims (
            id INT AUTO_INCREMENT PRIMARY KEY,
            vehicle_number VARCHAR(20),
            accident_occured_time DATETIME,
            cause_of_accident VARCHAR(50),
            accident_occurred ENUM('yes', 'no'),
            insurance_claim ENUM('yes', 'no')
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def insert_data(vehicle_number, accident_occured_time, cause_of_accident, accident_occurred, insurance_claim):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("USE insurance")
    cursor.execute(
        "INSERT INTO claims (vehicle_number, accident_occured_time, cause_of_accident, accident_occurred, insurance_claim) VALUES (%s, %s, %s, %s, %s)",
        (vehicle_number, accident_occured_time, cause_of_accident, accident_occurred, insurance_claim)
    )
    conn.commit()
    cursor.close()
    conn.close()

def clear_status_report(filename="status_report.txt"):
    open(filename, "w").close()

if __name__ == "__main__":
    setup_database()
    data = read_status_report()
    insert_data(*data)
    clear_status_report()
    print("\nStored in the DB")