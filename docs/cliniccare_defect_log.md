# ClinicCare-Lite Defect Log
This document records some of the problems encountered when developing and testing ClinicCare-Lite,  and how these were resolved.

 The test process has a number of issues, as listed below:| Encountered Issue | What it does to the system | Correction by test runner | Status |

According to the scheme, the function of the television station is to transmit television programs to the public. Television programs will be widely disseminated to the audience. The function of the television station is to serve the general public by making the television programs available to their audience.

Validating on file sizes was not functioning properly.  Files larger than 5 MB were still able to be uploaded.12.  Changed the upload code so that it would read the file and determine the actual size prior to writing the file to disk.13. Fixed

Notification code was not properly indented | Clinicians failed to be automatically notified on submission | Moved into correct position within submit_task() function | Resolved |

| Not receiving patient review notification | Patient see the automatic message after clinician review | Changed the review function to make a new patient notification and save it | Resolved |

| `return` statement was indented wrong in task submission | in the submission function,  an error occurred | Corrected the indentation so the return statement was inside the submission function | Works, previous error resolved

| Virtual environment was not ignored by Git | `venv` files might have been tracked | appended `cliniccare_lite/venv/` to `.gitignore` | corrected |

## Summary
All the above faults were found on the testing phase of the system manual testing.  The corrected versions of the features were subsequently tested and passed.