# Namra Chaklashiya
# 030698185
# CECS 327 - Assignment 8

import socket
import time
import psycopg2
from datetime import datetime
import pytz

# Device UIDs
FRIDGE1_UID = '8uv-u2u-crs-6cy'
FRIDGE2_UID = '4c53a4fe-ae58-4edf-9709-c112c551f184'
DISHWASHER_UID = 'k3e-14y-75v-mes'

# Sensor keys
MOISTURE_SENSOR = 'Fridge Moisture Sensor'
WATER_SENSOR = 'Dishwasher Water Sensor'
FRIDGE_AMMETER = 'Fridge Ammeter'
DISHWASHER_AMMETER = 'Dishwasher Ammeter'

def get_avg_moisture(conn):
    cur = conn.cursor()
    three_hrs_ago = int(time.time()) - 3 * 3600
    cur.execute(f"""
        SELECT AVG((payload ->> %s)::NUMERIC)
        FROM smart_refrigerator_data_virtual
        WHERE payload->>'parent_asset_uid' = %s
        AND (payload->>'timestamp')::BIGINT >= %s
    """, (MOISTURE_SENSOR, FRIDGE1_UID, three_hrs_ago))
    avg = cur.fetchone()[0]
    if avg is None:
        return "No moisture data available in the past three hours."
    return f"Average Moisture in the fridge 1 for the past 3 hours is: {avg:.2f}% RH (PST)"

def get_avg_water_cycle(conn):
    cur = conn.cursor()
    cur.execute(f"""
        SELECT AVG((payload ->> %s)::NUMERIC)
        FROM smart_dishwasher_data_virtual
        WHERE payload->>'parent_asset_uid' = %s
    """, (WATER_SENSOR, DISHWASHER_UID))
    avg_liters = cur.fetchone()[0]
    if avg_liters is None:
        return "No water consumption data available."
    gallons = float(avg_liters) * 0.264172
    return f"Average water consumption per cycle: {gallons:.2f} gallons"

def compare_electricity(conn):
    cur = conn.cursor()
    energy_data = {}

    # Fridge 1
    cur.execute(f"""
        SELECT SUM((payload ->> %s)::NUMERIC)
        FROM smart_refrigerator_data_virtual
        WHERE payload->>'parent_asset_uid' = %s
    """, (FRIDGE_AMMETER, FRIDGE1_UID))
    fridge1_amps = cur.fetchone()[0] or 0

    # Fridge 2
    cur.execute(f"""
        SELECT SUM((payload ->> %s)::NUMERIC)
        FROM smart_refrigerator_2_data_virtual
        WHERE payload->>'parent_asset_uid' = %s
    """, (FRIDGE_AMMETER, FRIDGE2_UID))
    fridge2_amps = cur.fetchone()[0] or 0

    # Dishwasher
    cur.execute(f"""
        SELECT SUM((payload ->> %s)::NUMERIC)
        FROM smart_dishwasher_data_virtual
        WHERE payload->>'parent_asset_uid' = %s
    """, (DISHWASHER_AMMETER, DISHWASHER_UID))
    dishwasher_amps = cur.fetchone()[0] or 0

    # Convert to kWh
    voltage = 120.0
    energy_data["Fridge 1"] = (float(fridge1_amps) / 3600) * voltage / 1000
    energy_data["Fridge 2"] = (float(fridge2_amps) / 3600) * voltage / 1000
    energy_data["Smart Dishwasher"] = (float(dishwasher_amps) / 3600) * voltage / 1000

    max_device = max(energy_data, key=energy_data.get)
    max_kwh = energy_data[max_device]

    return f"The device that consumed the most energy is '{max_device}' with {max_kwh:.3f} kWh."

def handle_query(query, conn):
    if "average moisture" in query:
        return get_avg_moisture(conn)
    elif "average water consumption" in query:
        return get_avg_water_cycle(conn)
    elif "consumed more electricity" in query:
        return compare_electricity(conn)
    else:
        return "Invalid query."

def start_server():
    host = "0.0.0.0"
    port = int(input("Enter the port number to bind the server: "))

    try:
        db_conn = psycopg2.connect("postgresql://smarthome_data_owner:npg_jyhbTsVN6a5J@ep-steep-meadow-a4e4b3r9-pooler.us-east-1.aws.neon.tech/smarthome_data?sslmode=require")
        print("Connected to NeonDB.")
    except Exception as e:
        print("Database connection failed:", e)
        return

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Server listening on port {port}...")
        conn, addr = server_socket.accept()
        with conn:
            print("Connected by", addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                query = data.decode()
                response = handle_query(query, db_conn)
                conn.sendall(response.encode())

if __name__ == "__main__":
    start_server()
