# Group-1-CS112

# ClinicCare-Lite

ClinicCare-Lite is a Flask-based clinic administration and communication system for clinicians and patients.

The system is strictly administrative and does not diagnose patients, recommend treatments, or interpret medical information.

## Main Features

### Clinician
- Register and log in
- Create and assign health tasks
- View patient submissions
- Download submitted files
- Review submissions
- Send and receive messages
- Create clinic announcements
- Create patient appointments
- View basic operational analytics

### Patient
- Register and log in
- View assigned health tasks
- Upload TXT, CSV, and PDF submissions
- View clinician review outcomes and notes
- Send and receive messages
- View clinic announcements
- View appointments
- View private engagement points
- Choose colorful or dark theme

## Installation

Open a terminal inside the `cliniccare_lite` folder.

Create a virtual environment:

```bash
python -m venv venv


## Testing

ClinicCare-Lite was tested using both manual testing and automated unit tests.

The automated tests were created with Python's built-in `unittest` framework and cover:

- Valid and invalid patient IDs
- Valid and invalid clinician IDs
- Strong and weak passwords
- Unauthorized access to the clinician dashboard

A total of 7 automated tests were run successfully.

To run the automated tests, open a terminal inside the `cliniccare_lite` folder and run:

```bash
python -m unittest discover -s tests -v



## Important Notice

ClinicCare-Lite is an academic prototype designed for administrative and communication purposes only.

It does not diagnose patients, interpret symptoms, recommend treatment, prescribe medication, or replace professional clinical judgement.

Real email notifications are not currently configured. Notifications are provided through the in-app messaging system.