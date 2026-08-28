import os
import sys
import unittest

# Allow tests to import app.py
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import app, valid_user_id, valid_password


class ClinicCareTests(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    # User ID tests
    def test_valid_patient_id(self):
        self.assertTrue(valid_user_id("12342024", "patient"))

    def test_invalid_patient_id(self):
        self.assertFalse(valid_user_id("12342030", "patient"))

    def test_valid_clinician_id(self):
        self.assertTrue(valid_user_id("12340000", "clinician"))

    def test_invalid_clinician_id(self):
        self.assertFalse(valid_user_id("12345678", "clinician"))

    # Password tests
    def test_valid_password(self):
        self.assertTrue(valid_password("Test@123"))

    def test_weak_password(self):
        self.assertFalse(valid_password("password"))

    # Access-control test
    def test_clinician_dashboard_requires_login(self):
        response = self.client.get("/clinician-dashboard")

        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()