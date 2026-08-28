# ClinicCare-Lite Technical Report

## 1. Introduction

ClinicCare-Lite is a simple clinic administration and communication system that we developed as part of the CS 112 final project.

The main idea behind the system is to make communication and basic administrative activities between clinicians and patients easier. The system allows clinicians to assign tasks, review patient submissions, create appointments and announcements, and communicate with patients. Patients can also view their tasks, upload files, receive feedback, and send messages to clinicians.

It is important to note that ClinicCare-Lite is not a medical diagnosis system. It does not diagnose illnesses, interpret symptoms, recommend treatments, prescribe medication, or replace the judgement of a healthcare professional. Its purpose is strictly administrative and communication-based.

---

## 2. Main Users and Requirements

ClinicCare-Lite has two main types of users: clinicians and patients.

### Clinician

A clinician is able to:

- Register and log into the system
- Access a clinician dashboard
- Create and assign tasks to patients
- Add descriptions and due dates to tasks
- View files submitted by patients
- Download patient submissions
- Review submissions and leave notes
- Send and receive messages
- Receive notifications when a patient submits a task
- Create appointments
- Create clinic announcements
- View basic system analytics

### Patient

A patient is able to:

- Register and log into the system
- Access a patient dashboard
- View assigned tasks
- View task descriptions and due dates
- Upload approved files
- Check the status of submitted tasks
- View clinician feedback and review outcomes
- Send and receive messages
- Receive notifications after a clinician reviews a submission
- View appointments
- View clinic announcements
- See their own engagement points
- Choose between a colorful and dark dashboard theme

The main workflow of the system starts when a clinician creates a task for a patient. The patient completes the task and uploads a file, after which the clinician reviews the submission and provides feedback.

---

## 3. Technologies Used

We used the following technologies to build ClinicCare-Lite:

- **Python** for the main application logic
- **Flask** for the web application
- **HTML** for the structure of the webpages
- **CSS** for styling the system
- **Jinja** for displaying dynamic information on the webpages
- **JSON** for storing application data
- **bcrypt** for password hashing
- **python-dotenv** for managing environment variables
- **Git and GitHub** for version control and collaboration
- **Python unittest** for automated testing

Flask was chosen because it made it easier to create routes, handle forms, manage sessions, upload files, and create separate dashboards for patients and clinicians.

---

## 4. System Structure

ClinicCare-Lite follows a simple web application structure.

The user interacts with the system through a web browser. Flask handles the requests coming from the user, processes the information, and reads from or writes to the JSON files.

The basic structure is:

**User Browser → Flask Application → JSON Files / Uploaded Files**

The frontend of the application includes pages such as:

- `login.html`
- `register.html`
- `patient_dashboard.html`
- `clinician_dashboard.html`

The main backend logic is found in `app.py`.

This file handles functions such as registration, login, task creation, file submission, review, messaging, appointments, announcements, notifications, and analytics.

The system stores information in JSON files for:

- users
- tasks
- submissions
- messages
- appointments
- announcements

Uploaded patient files are stored separately inside the uploads folder.

JSON was used because it was simple to work with and was suitable for the size of this academic prototype.

---

## 5. Authentication and Security

Security was an important part of the system, especially because patients and clinicians should not have access to the same pages.

### User ID Validation

Clinician IDs must contain eight digits and end in `0000`.

Patient IDs must also contain eight digits, but the last four digits must represent a valid registration year between 2022 and 2028.

This helps prevent users from registering with IDs that do not follow the required format.

### Password Requirements

Passwords must:

- Be at least eight characters long
- Include an uppercase letter
- Include a lowercase letter
- Include a number
- Include a special character

Passwords are hashed using `bcrypt` before they are saved.

This means that the user's actual password is not stored directly in the JSON file.

### Role-Based Access

The system uses Flask sessions to keep track of the user who is currently logged in.

The user's role is also stored in the session.

This allows the system to prevent a patient from accessing pages meant only for clinicians and vice versa.

For example, when a patient tries to directly access the clinician dashboard, the system redirects them instead of allowing access.

### Environment Variables

The Flask secret key is stored inside a `.env` file.

The `.env` file is included in `.gitignore`, which prevents it from being uploaded to GitHub.

---

## 6. Task Assignment and File Submission

Clinicians can create tasks for patients from the clinician dashboard.

Each task contains information such as:

- Task ID
- Patient ID
- Clinician ID
- Task title
- Task description
- Due date
- Task status

Once the task is created, it appears on the assigned patient's dashboard.

The patient can then upload a file for the task.

The system accepts:

- `.txt`
- `.csv`
- `.pdf`

Files such as JPG images are rejected.

The system also rejects files larger than 5 MB and prevents a patient from submitting the same task more than once.

Uploaded files are renamed using the patient ID and task ID so that they can be easily connected to the correct user and task.

---

## 7. File Completeness Checking

ClinicCare-Lite also performs a simple completeness check on uploaded files.

For TXT files, the system checks whether the file is empty.

For CSV files, the system checks whether the file contains headings, data rows, and empty cells.

PDF files are accepted, but the system does not try to interpret what is inside them.

The completeness check only looks at basic file structure. It does not analyse medical information or decide whether a patient's information is medically normal or abnormal.

This was done intentionally to keep ClinicCare-Lite within its administrative purpose.

---

## 8. Clinician Review Process

After a patient uploads a file, the clinician can view the submission on the clinician dashboard.

The clinician can then select a review outcome and add notes.

The system records information such as:

- Reviewer ID
- Date and time of review
- Review outcome
- Review notes
- Notification status

After the clinician completes the review, the patient's task status is updated.

The patient can then see both the review outcome and the notes given by the clinician.

---

## 9. Messaging and Notifications

ClinicCare-Lite includes an in-app messaging feature.

Patients can send non-urgent messages to clinicians, and clinicians can reply to patients.

Each message stores:

- Message ID
- Sender ID
- Recipient ID
- Message content
- Timestamp
- Read status

The system also displays a warning that the messaging feature should not be used for emergencies.

We also implemented automatic in-app notifications.

When a patient submits a task, the clinician receives a notification.

When a clinician reviews a submission, the patient receives a notification.

At the moment, real email notifications have not been implemented.

---

## 10. Appointments and Announcements

Clinicians can create appointments for patients.

These appointments then appear on the patient's dashboard.

Clinicians can also create clinic announcements, which are displayed to patients.

These features help the clinic communicate important administrative information to patients without using the system to make medical decisions.

---

## 11. Engagement Tracking

Patients can earn private engagement points when they complete certain actions, such as submitting an assigned task.

The engagement points are only visible to the individual patient.

There is no public leaderboard or comparison between patients.

This was important because patient activity should remain private.

---

## 12. Operational Analytics

The clinician dashboard also contains some basic analytics.

These include:

- Total number of tasks
- Total submissions
- Number of reviewed submissions
- Number of pending reviews
- Task completion rate

These statistics are meant to help clinicians understand how the administrative system is being used.

They do not provide any medical or diagnostic information about patients.

---

## 13. User Interface

ClinicCare-Lite has separate dashboards for patients and clinicians.

The clinician dashboard uses a dark theme.

Patients can choose between a dark theme and a more colorful theme.

Forms are used throughout the application for actions such as:

- Registration
- Login
- Task creation
- File upload
- Submission review
- Messaging
- Appointment creation
- Announcement creation

We also added basic responsive styling to make the pages easier to use on smaller screens.

---

## 14. Testing

We tested ClinicCare-Lite manually and also created automated tests.

Manual testing included:

- Valid patient registration
- Valid clinician registration
- Invalid patient IDs
- Invalid clinician IDs
- Weak passwords
- Incorrect passwords
- Unauthorized access to dashboards
- Task creation
- Patient task viewing
- TXT file uploads
- Unsupported JPG uploads
- Files larger than 5 MB
- Duplicate submissions
- File completeness checks
- Clinician review
- Patient review display
- Patient-to-clinician messaging
- Clinician-to-patient messaging
- Submission notifications
- Review notifications
- Appointment creation
- Announcement creation
- Theme switching
- Engagement points
- Analytics
- File downloading

We also created seven automated tests using Python's `unittest` framework.

These tests checked:

1. Valid patient ID
2. Invalid patient ID
3. Valid clinician ID
4. Invalid clinician ID
5. Valid password
6. Weak password
7. Unauthorized access to the clinician dashboard

All seven automated tests passed.

More information about the testing can be found in:

`docs/cliniccare_test_report.md`

The problems found during testing and the corrections made are recorded in:

`docs/cliniccare_defect_log.md`

---

## 15. Problems We Encountered

We experienced a few problems while developing and testing the application.

### File Size Checking

At first, the system was allowing files larger than 5 MB to be submitted.

We changed the file upload logic so that the file is read and its size is calculated before it is saved.

After making the change, we tested the system again using a file larger than 5 MB, and it was correctly rejected.

### Submission Notification

We also had a problem where the clinician was not receiving an automatic notification after a patient submitted a task.

The problem was caused by the indentation of the notification code.

After correcting the indentation and testing again, the notification appeared correctly in the clinician's inbox.

### Patient Review Notification

The patient was also not receiving a notification after the clinician reviewed a submission.

We updated the review function so that a message is automatically created for the patient after the review.

After testing the feature again, the notification worked correctly.

These problems showed the importance of testing the application repeatedly during development.

---

## 16. Current Limitations

ClinicCare-Lite is still an academic prototype, so some parts of the full project specification have not been implemented.

Some current limitations are:

- Real email notifications have not been implemented
- Message searching is not available
- Conversation threading is limited
- Full read and unread message management is limited
- Automatic appointment reminders are not available
- Automatic task due-date reminders are not available
- Announcement expiry and automatic archiving are not available
- The analytics dashboard contains only basic statistics
- Engagement tracking mainly uses points rather than detailed streaks or monthly summaries
- JSON files are used instead of a full production database

These limitations do not prevent the main ClinicCare-Lite workflow from working.

---

## 17. Ethical and Clinical Boundaries

One of the most important requirements of ClinicCare-Lite is making sure that the system does not become a diagnostic tool.

For this reason, the system does not:

- Diagnose illnesses
- Interpret patient symptoms
- Calculate disease risk
- Recommend treatments
- Prescribe medication
- Publicly compare patients

The automated features are limited to administrative tasks such as file validation, notifications, task tracking, and completeness checking.

---

## 18. Possible Future Improvements

If the system were developed further, some improvements could include:

- Adding real email notifications
- Adding appointment reminders
- Adding task due-date reminders
- Improving message searching and threading
- Improving read and unread message management
- Adding announcement expiry and archiving
- Adding more detailed clinician analytics
- Calculating average review turnaround time
- Showing appointment no-show statistics
- Adding monthly charts
- Improving patient engagement history
- Moving from JSON files to a proper database
- Adding more automated security and integration tests

---

## 19. Conclusion

Overall, ClinicCare-Lite was able to achieve the main goal of creating a simple clinic administration and communication system.

Clinicians can assign tasks, review patient submissions, create appointments and announcements, communicate with patients, and view basic analytics.

Patients can view assigned tasks, upload files, receive feedback, communicate with clinicians, view appointments and announcements, and track their own engagement points.

Testing also helped us identify and correct problems with file size validation and automatic notifications.

Although there are still some features that could be added in the future, the current version provides a working task-to-review workflow while maintaining patient privacy and staying within the required non-diagnostic scope.