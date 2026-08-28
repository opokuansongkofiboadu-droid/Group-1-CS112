# ClinicCare-Lite Design Diagrams

## 1. Use-Case Diagram

```mermaid
flowchart LR
    P[Patient]
    C[Clinician]

    P --> A[Register / Login]
    P --> B[View Assigned Tasks]
    P --> D[Upload Submission]
    P --> E[View Review Feedback]
    P --> F[Send / Receive Messages]
    P --> G[View Appointments]
    P --> H[View Announcements]
    P --> I[View Engagement Points]

    C --> A
    C --> J[Create and Assign Tasks]
    C --> K[View Patient Submissions]
    C --> L[Review Submissions]
    C --> M[Download Files]
    C --> F
    C --> N[Create Appointments]
    C --> O[Create Announcements]
    C --> Q[View Analytics]


### 2. System Architecture

Add underneath:

```markdown
## 2. System Architecture

```mermaid
flowchart TD
    U[Patient / Clinician]
    B[Web Browser]
    F[Flask Application - app.py]
    T[HTML / Jinja Templates]
    J[JSON Data Files]
    UP[Uploads Folder]
    BC[bcrypt]
    ENV[Environment Variables]

    U --> B
    B --> F
    F --> T
    T --> B
    F --> J
    F --> UP
    F --> BC
    ENV --> F

    
### 3. Simple Class/Data Model Diagram

Then add:

```markdown
## 3. Class / Data Model Diagram

```mermaid
classDiagram

    class User {
        user_id
        full_name
        email
        password_hash
        role
        engagement_points
    }

    class HealthTask {
        task_id
        patient_id
        clinician_id
        title
        description
        due_date
        status
    }

    class Submission {
        submission_id
        task_id
        patient_id
        filename
        submitted_at
        status
        review_outcome
        review_notes
    }

    class Message {
        message_id
        sender_id
        recipient_id
        content
        timestamp
        read
    }

    class Appointment {
        appointment_id
        patient_id
        clinician_id
        date
        time
        purpose
        status
    }

    class Announcement {
        announcement_id
        clinician_id
        title
        content
        priority
        published_at
    }

    User "1" --> "*" HealthTask : patient receives
    User "1" --> "*" HealthTask : clinician assigns
    HealthTask "1" --> "0..1" Submission : has
    User "1" --> "*" Message : sends/receives
    User "1" --> "*" Appointment : patient/clinician
    User "1" --> "*" Announcement : clinician creates