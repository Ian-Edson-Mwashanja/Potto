from flask import Flask, jsonify, request
from flask_cors import CORS
from db import get_connection
app = Flask(__name__)
CORS(app)
# HOME
@app.route("/")
def home():
    return jsonify({
        "message": "Welcome to Potto API",
        "status": "running"
    })
# HEALTH CHECK
@app.route("/api/health")
def health():
    return jsonify({
        "status": "healthy"
    })
# GET ALL ANOMALIES
@app.route("/api/anomalies", methods=["GET"])
def get_anomalies():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            type,
            severity,
            confidence,
            latitude,
            longitude,
            detected_at,
            device_id
        FROM RoadAnomalies
        ORDER BY detected_at DESC
    """)

    rows = cursor.fetchall()

    anomalies = []

    for row in rows:

        anomalies.append({
            "id": row.id,
            "type": row.type,
            "severity": row.severity,
            "confidence": float(row.confidence),
            "latitude": float(row.latitude),
            "longitude": float(row.longitude),
            "detected_at": str(row.detected_at),
            "device_id": row.device_id
        })

    cursor.close()
    connection.close()

    return jsonify(anomalies)
# CREATE NEW ANOMALY
@app.route("/api/anomalies", methods=["POST"])
def create_anomaly():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "No JSON data received"
        }), 400

    required_fields = [
        "type",
        "severity",
        "confidence",
        "latitude",
        "longitude"
    ]

    for field in required_fields:

        if field not in data:
            return jsonify({
                "error": f"Missing field: {field}"
            }), 400
    # Validate severity

    valid_severities = [
        "severe",
        "moderate",
        "low"
    ]

    if data["severity"] not in valid_severities:

        return jsonify({
            "error": "Invalid severity"
        }), 400
    # Validate confidence
    try:
        confidence = float(data["confidence"])

    except (TypeError, ValueError):

        return jsonify({
            "error": "Confidence must be a number"
        }), 400

    if confidence < 0 or confidence > 1:

        return jsonify({
            "error": "Confidence must be between 0 and 1"
        }), 400
    # Validate latitude
    try:
        latitude = float(data["latitude"])

    except (TypeError, ValueError):

        return jsonify({
            "error": "Latitude must be a number"
        }), 400

    if latitude < -90 or latitude > 90:

        return jsonify({
            "error": "Invalid latitude"
        }), 400
    # Validate longitude
    try:
        longitude = float(data["longitude"])

    except (TypeError, ValueError):

        return jsonify({
            "error": "Longitude must be a number"
        }), 400

    if longitude < -180 or longitude > 180:

        return jsonify({
            "error": "Invalid longitude"
        }), 400
    # Device ID
    device_id = data.get(
        "device_id",
        "POTTO-001"
    )
    # Save to database
    try:

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO RoadAnomalies
            (
                type,
                severity,
                confidence,
                latitude,
                longitude,
                detected_at,
                device_id
            )
            VALUES (?, ?, ?, ?, ?, GETDATE(), ?)
        """,
            data["type"],
            data["severity"],
            confidence,
            latitude,
            longitude,
            device_id
        )

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({
            "message": "Anomaly successfully saved",
            "type": data["type"],
            "severity": data["severity"],
            "confidence": confidence,
            "latitude": latitude,
            "longitude": longitude,
            "device_id": device_id
        }), 201

    except Exception as error:

        print("Database error:", error)

        return jsonify({
            "error": "Failed to save anomaly"
        }), 500
# ANALYTICS
@app.route("/api/analytics", methods=["GET"])
def get_analytics():

    connection = get_connection()
    cursor = connection.cursor()

    # Total detections
    cursor.execute("""
        SELECT COUNT(*)
        FROM RoadAnomalies
    """)

    total = cursor.fetchone()[0]
    # Severe detections
    cursor.execute("""
        SELECT COUNT(*)
        FROM RoadAnomalies
        WHERE severity = 'severe'
    """)

    severe = cursor.fetchone()[0]
    # Moderate detections
    cursor.execute("""
        SELECT COUNT(*)
        FROM RoadAnomalies
        WHERE severity = 'moderate'
    """)

    moderate = cursor.fetchone()[0]
    # Low detections
    cursor.execute("""
        SELECT COUNT(*)
        FROM RoadAnomalies
        WHERE severity = 'low'
    """)

    low = cursor.fetchone()[0]
    # Detections by type
    cursor.execute("""
        SELECT
            type,
            COUNT(*) AS total
        FROM RoadAnomalies
        GROUP BY type
        ORDER BY total DESC
    """)
    type_rows = cursor.fetchall()

    by_type = []

    for row in type_rows:

        by_type.append({
            "type": row.type,
            "total": row.total
        })
    cursor.close()
    connection.close()

    return jsonify({
        "total": total,
        "severity": {
            "severe": severe,
            "moderate": moderate,
            "low": low
        },
        "by_type": by_type
    })
# REPAIR PRIORITIES
@app.route("/api/priorities", methods=["GET"])
def get_priorities():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            type,
            severity,
            confidence,
            latitude,
            longitude,
            detected_at,
            device_id
        FROM RoadAnomalies
    """)

    rows = cursor.fetchall()

    priorities = []

    # Severity points used by our prototype
    severity_points = {
        "severe": 3,
        "moderate": 2,
        "low": 1
    }
    for row in rows:

        points = severity_points.get(row.severity, 1)

        priority_score = (
            points * float(row.confidence) * 100
        )
        if priority_score >= 200:
            priority = "HIGH"

        elif priority_score >= 100:
            priority = "MEDIUM"

        else:
            priority = "LOW"
        priorities.append({
            "id": row.id,
            "type": row.type,
            "severity": row.severity,
            "confidence": float(row.confidence),
            "latitude": float(row.latitude),
            "longitude": float(row.longitude),
            "detected_at": str(row.detected_at),
            "device_id": row.device_id,
            "priority_score": round(priority_score, 2),
            "priority": priority
        })
    cursor.close()
    connection.close()

    # Highest priority first
    priorities.sort(
        key=lambda x: x["priority_score"],
        reverse=True
    )
    return jsonify(priorities)
@app.errorhandler(404)
def not_found(error):

    return jsonify({
        "error": "Endpoint not found"
    }), 404
@app.errorhandler(500)
def internal_error(error):

    return jsonify({
        "error": "Internal server error"
    }), 500
# START SERVER
if __name__ == "__main__":
    app.run(debug=True)
