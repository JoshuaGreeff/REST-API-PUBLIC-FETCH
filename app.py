"""Fetch and display selected NHTSA vehicle-variable data with Flask."""

from flask import Flask, jsonify, render_template
import requests


app = Flask(__name__)

# The assignment provides this public endpoint. Keeping it in one variable makes
# the external source easy to find and change if its address is updated later.
NHTSA_URL = "https://vpic.nhtsa.dot.gov/api/vehicles/GetVehicleVariableList?format=json"
TARGET_GROUP = "Active Safety System"


@app.route("/", methods=["GET"])
def home():
    """Serve the small browser page that demonstrates asynchronous Fetch."""
    return render_template("index.html")


@app.route("/items", methods=["GET"])
def get_items():
    """Fetch NHTSA data, keep the required group, and return JSON."""
    try:
        # This GET request calls the required public API and avoids waiting forever
        # if the third-party service is unavailable.
        response = requests.get(NHTSA_URL, timeout=10)
        response.raise_for_status()
        payload = response.json()

        # The NHTSA response stores the list in Results. This filter is the required
        # assignment change: only Active Safety System variables are returned.
        results = payload.get("Results", [])
        filtered_items = [
            item for item in results if item.get("GroupName") == TARGET_GROUP
        ]
        return jsonify(filtered_items), 200

    except requests.exceptions.HTTPError as error:
        # If NHTSA returns an HTTP error, pass a useful status and JSON message back
        # to the browser instead of letting Flask return an unhandled traceback.
        status_code = error.response.status_code if error.response is not None else 502
        return jsonify(error=f"NHTSA returned an HTTP error: {error}"), status_code
    except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as error:
        # A temporary network problem is reported as 503 because the external service
        # cannot be reached right now.
        return jsonify(error=f"Unable to reach NHTSA: {error}"), 503
    except (requests.exceptions.RequestException, ValueError) as error:
        # This catches other request failures and invalid JSON from the public API.
        return jsonify(error=f"Unable to retrieve vehicle data: {error}"), 502


if __name__ == "__main__":
    # One command, python app.py, starts the local application on port 5000.
    app.run(debug=True, port=5000)
