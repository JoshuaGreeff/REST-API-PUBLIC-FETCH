"""Focused tests for the required NHTSA filter and external-service error path."""

import unittest
from unittest.mock import Mock, patch

import requests

from app import app


class VehicleVariableApiTests(unittest.TestCase):
    """Use Flask's test client without calling the public API during every test."""

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("app.requests.get")
    def test_items_returns_only_active_safety_system_variables(self, mock_get):
        """The assignment filter keeps matching GroupName values and removes others."""
        remote_response = Mock()
        remote_response.json.return_value = {
            "Results": [
                {"ID": 86, "Name": "ABS", "GroupName": "Active Safety System"},
                {"ID": 1, "Name": "Make", "GroupName": "General"},
            ]
        }
        remote_response.raise_for_status.return_value = None
        mock_get.return_value = remote_response

        response = self.client.get("/items")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [
            {"ID": 86, "Name": "ABS", "GroupName": "Active Safety System"}
        ])

    @patch("app.requests.get", side_effect=requests.exceptions.Timeout("timed out"))
    def test_items_returns_503_when_external_api_times_out(self, mock_get):
        """A temporary external outage returns JSON and a useful 503 status code."""
        response = self.client.get("/items")

        self.assertEqual(response.status_code, 503)
        self.assertIn("Unable to reach NHTSA", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()
