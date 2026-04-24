from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

# 🔽 Load JSON data
with open("data.json") as f:
    tourism_data = json.load(f)

# 🔽 Initialize DB
def init_db():
    conn = sqlite3.connect("trips.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        people INTEGER,
        place TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# 🔽 Home
@app.route("/")
def home():
    return "Backend is running 🚀"

# 🔽 Chat API
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").lower()

    if message in tourism_data:
        city = tourism_data[message]

        reply = f"""
📍 Places:
{", ".join(city['places'])}

🏨 Hotels:
{", ".join(city['hotels'])}

🍛 Food:
{", ".join(city['food'])}

👉 Type 'plan trip' to book!
"""
    elif "plan trip" in message:
        reply = "🧳 Fill the form to plan your trip!"
    else:
        reply = "❌ City not found. Try: pune, mumbai, nagpur"

    return jsonify({"reply": reply})

# 🔽 Plan Trip API
@app.route("/plan", methods=["POST"])
def plan_trip():
    data = request.get_json()

    name = data.get("name")
    people = data.get("people")
    place = data.get("place")

    conn = sqlite3.connect("trips.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO trips (name, people, place) VALUES (?, ?, ?)",
        (name, people, place)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": f"✅ Trip booked for {name} to {place} for {people} people!"
    })

# 🔽 View Trips
@app.route("/trips", methods=["GET"])
def get_trips():
    conn = sqlite3.connect("trips.db")
    c = conn.cursor()

    c.execute("SELECT * FROM trips")
    data = c.fetchall()

    conn.close()

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)