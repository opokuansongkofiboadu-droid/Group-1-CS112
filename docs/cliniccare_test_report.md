# ClinicCare-Lite Test Report

## Introduction

This report summarizes the tests carried out on ClinicCare-Lite to make sure the main features of the system work as expected. The testing focused on registration, login, role-based access, task assignment, file submission, messaging, clinician review, notifications, appointments, announcements, analytics, and other important parts of the system.

Most of the tests were done manually by using the system as both a patient and a clinician. Some basic automated tests were also created using Python's `unittest` module.

---

## 1. Registration and Login Testing

We first tested whether patients and clinicians could register and log in correctly. We also tested invalid IDs and weak passwords to make sure the system rejects incorrect information.

| Test | Input | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| Valid patient registration | 12342024 | Patient account should be created | Account was created successfully | PASS |
| Valid clinician registration | 12340000 | Clinician account should be created | Account was created successfully | PASS |
| Invalid clinician ID | 12345678 | System should reject the ID | Invalid ID message was displayed | PASS |
| Invalid patient ID | 12342030 | System should reject the ID | Invalid ID message was displayed | PASS |
| Weak password | password | System should reject the password | Password requirement message was displayed | PASS |
| Incorrect login password | Incorrect password | Login should fail | User was not allowed to log in | PASS |

---

## 2. Role-Based Access Testing

We also tested whether patients and clinicians could only access the pages meant for their role.

| Test | Expected Result | Actual Result | Status |
|---|---|---|---|
| Patient tries to access clinician dashboard | Access should be blocked | Patient was redirected to the login page | PASS |
| Clinician logs in | Clinician dashboard should appear | Dashboard opened correctly | PASS |
| Patient logs in | Patient dashboard should appear | Dashboard opened correctly | PASS |

This helped confirm that the role-based access system was working correctly.

---

## 3. Health Task Testing

The task feature was tested by logging in as a clinician, creating a task, and assigning it to a patient.

| Test | Expected Result | Actual Result | Status |
|---|---|---|---|
| Clinician creates a task | Task should be saved | Task was successfully saved | PASS |
| Patient views assigned task | Task should appear on dashboard | Task appeared correctly | PASS |

The patient was able to see the task title, description, due date, and status.

---

## 4. File Submission Testing

Different types of files were used to test the upload system.

| Test | Expected Result | Actual Result | Status |
|---|---|---|---|
| Upload TXT file | File should be accepted | File uploaded successfully | PASS |
| Upload JPG file | File should be rejected | Unsupported file message appeared | PASS |
| Upload file larger than 5 MB | File should be rejected | File too large message appeared | PASS |
| Submit the same task twice | Duplicate should be blocked | Second submission was rejected | PASS |
| TXT completeness check | System should check the file | Completeness result was displayed | PASS |

The system correctly accepted the supported file types and rejected unsupported or oversized files.

---

## 5. Clinician Review Testing

After the patient submitted a file, the clinician review process was tested.

| Test | Expected Result | Actual Result | Status |
|---|---|---|---|
| Clinician views submission | Submission should appear | Submission appeared on dashboard | PASS |
| Clinician reviews submission | Review should be saved | Review was saved successfully | PASS |
| Patient views review | Review outcome and notes should appear | Patient could see the review | PASS |

The clinician was able to choose a review outcome and add notes. The patient could then see the outcome on their dashboard.

---

## 6. Messaging and Notification Testing

Messaging was tested in both directions between the patient and clinician.

| Test | Expected Result | Actual Result | Status |
|---|---|---|---|
| Patient sends clinician a message | Clinician should receive it | Message appeared in clinician inbox | PASS |
| Clinician replies to patient | Patient should receive it | Reply appeared in patient inbox | PASS |
| Patient submits a task | Clinician should receive notification | Notification appeared | PASS |
| Clinician reviews a submission | Patient should receive notification | Notification appeared | PASS |

The system also displays a warning that the messaging feature is not meant for emergencies.

---

## 7. Other Feature Testing

Other parts of the system were tested to make sure the complete workflow worked properly.

| Test | Expected Result | Actual Result | Status |
|---|---|---|---|
| Clinician creates announcement | Patient should see it | Announcement appeared | PASS |
| Clinician creates appointment | Patient should see it | Appointment appeared | PASS |
| Engagement points | Patient should see their own points | Points were displayed | PASS |
| Theme selection | Patient should be able to change theme | Colorful and dark themes worked | PASS |
| Clinician analytics | Statistics should appear | Analytics were displayed | PASS |
| Submission download | Clinician should download patient file | Download worked successfully | PASS |

---

## 8. Automated Testing

In addition to the manual testing, seven automated tests were created using Python's built-in `unittest` framework.

The automated tests checked:

- a valid patient ID
- an invalid patient ID
- a valid clinician ID
- an invalid clinician ID
- a strong password
- a weak password
- access to the clinician dashboard without logging in

All seven automated tests passed successfully.

---

## Problems Found and Corrections Made

A few issues were found during development and testing.

One issue was with the file size validation. Large files were initially being accepted instead of being rejected. The file size checking method was changed so that the uploaded file is read first and its size is measured before saving it. After this change, files larger than 5 MB were correctly rejected.

There was also an indentation problem in the task submission function, which affected the automatic notification feature. The notification code was moved into the correct part of the function and tested again. After the correction, clinicians received a notification whenever a patient submitted a task.

The review notification was also tested to make sure patients received a message after their submission had been reviewed.

---

## Known Limitations

ClinicCare-Lite is currently an academic prototype, so there are still some features that could be improved.

Real email notifications have not been configured. At the moment, notifications are sent through the system's in-app messaging feature.

The file completeness checker only checks the basic structure of uploaded files. It does not interpret medical information or make any medical decisions.

ClinicCare-Lite is designed only for administrative and communication purposes. It does not diagnose patients, recommend treatment, or replace the judgement of a healthcare professional.

---

## Conclusion

Overall, the main ClinicCare-Lite workflow worked successfully during testing. Clinicians could assign tasks, review patient submissions, create appointments and announcements, communicate with patients, and view basic analytics. Patients could view their assigned tasks, submit files, receive reviews, communicate with clinicians, and view their own engagement information.

The manual and automated tests helped confirm that the major features were working correctly while also helping us identify and fix problems during development.