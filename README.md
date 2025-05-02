# CECS 327 - Assignment 8: End-to-End IoT System

## Author
**Namra Chaklashiya**  
Student ID: 030698185

---

## Project Structure
```
├── client.py                 # TCP client that handles user queries
├── server.py                 # TCP server that connects to NeonDB and processes queries
├── README.md                 # Project overview and setup instructions
```

---

## Objective
This project implements an end-to-end IoT system that:
- Connects a TCP client to a TCP server
- Processes user queries
- Fetches and computes data from IoT sensors stored in NeonDB
- Uses metadata from Dataniz devices
- Returns results in PST and imperial units

---

## Queries Supported
The client accepts only these three exact queries:

1. `What is the average moisture inside my kitchen fridge in the past three hours?`
2. `What is the average water consumption per cycle in my smart dishwasher?`
3. `Which device consumed more electricity among my three IoT devices?`

Invalid queries are rejected with a friendly message.

---

## Dataniz Devices
- **Smart Refrigerator 1** (UID: `8uv-u2u-crs-6cy`)
- **Smart Refrigerator 2** (UID: `4c53a4fe-ae58-4edf-9709-c112c551f184`)
- **Smart Dishwasher** (UID: `k3e-14y-75v-mes`)

Each device has sensors with names:
- `Fridge Moisture Sensor`
- `Fridge Ammeter`
- `Dishwasher Water Sensor`
- `Dishwasher Ammeter`

---

## PostgreSQL (NeonDB) Configuration
- **Database Name**: `smarthome_data`
- **Tables Used**:
  - `smart_refrigerator_data_virtual`
  - `smart_refrigerator_2_data_virtual`
  - `smart_dishwasher_data_virtual`

Ensure these tables are populated with data from Dataniz.

---

## Setup Instructions

### 1. Install Required Packages
```bash
pip install psycopg2-binary pytz
```

### 2. Start the Server
```bash
python server.py
# Enter port: 9999
```

### 3. Start the Client (in a new terminal)
```bash
python client.py
# Enter IP: 127.0.0.1
# Enter port: 9999
```

### 4. Enter Queries
Copy and paste one of the 3 supported queries.  
Type `exit` to close the client.  
Press `Ctrl + C` to stop the server.

---

## Notes
- All timestamps are handled in PST.
- Moisture readings are reported as RH%.
- Water usage is reported in gallons.
- Electricity consumption is converted to kWh (using 120V).
- Queries are case- and punctuation-sensitive.

---

## Submission Checklist
- [x] TCP client and server work correctly
- [x] Client accepts only 3 queries
- [x] Server connects to NeonDB and fetches data from correct tables
- [x] Queries return results with correct units and time zones
- [x] Metadata (UIDs and sensor names) from Dataniz is used

---

## Status: COMPLETED
This system has been tested locally and is functioning as expected.
