# ClassConnect

# Plan

- [x] Define key user stories
- [x] Define MVP scope
- [x] Create mocks for the MVP - very simple one page app.
      ------> ended up not being so simple...
      ![mock](/docs/mock.png)
      ![mock with components](/docs/mvp-mock-with-components.png)
- [x] Define a simple databse schema
- [x] Look into the hashing algorithm for student IDs- selected 1
- [IP] Set up the react app
- [IP] Define the states and functionality
- [x] Breakdown tasks
- V1
  - [x] create file uploader component - no need to create - already have one
  - [x] create input form component
  - [x] create a hidden success screen
    - ~~[IP ] figure out where the file gets uploaded to google cloud~~ no longer needed as we are not storing files any more.
    - [x] need to implement a backend: Python with Flask - as it's lightweight and minimalistic. I dont' think I will see super high traffic with this app.
    - [IP] how to implement the logic of parsing the uploaded csv info
    - [ ] set up Heroku SQL with created tables
    - [ ] logic to send data to SQL
  - [ ] create qureies for matching + update
- V2
  - [ ] add the logic for getting the stats bar component
- V3
  - [ ] add privacy note pop up
- V4
  - [ ] Add styling to everything...
- [ ] Define test flows
- [ ] Carry out the test flows
- [ ] Invite beta testers
- [ ] Iterate based on feedback

# key user stories

- As a new BCS student, I want to be able to find folks in my cohorts, who are in the same course as well as the same lecture, lab and discussion sections as me so that I can connect with them and form study groups, or pair up as lab / porject partners.
- Students should be able to upload their course schedule and get notified of other students who are in their course, as well as who share the same lecture, lab and discussion sections.
- Students should be able to share their contact information if they wish to be contacted by other users.

# MVP scope

- There's a button to upload a schedule.
- The data base work and update student schedule correctly.
- There's a status bar to show how many people have uploaded their schedules, and list of courses and number of people in each course.
- There's a blurb that talk about the purpose of app and how it works (aka people get email at 5pm daily of updates).
- MVP Note! It is posisble the email update feature will be hard to implement...if it's hard...we could forgo this and just display information on the app... and we could display a message to the user to check back the next day if they don't see any matches.
  - Or send email to users when 'five' more folks have uploaded their schedules./ when the database has new matches for a given users / Users get an email with new matches

# Database Schema:

Student Table
| COLUMN | DATA TYPE | NOTES |
| ------ | --------- | ----- |
| first_name | VARCHAR | first name of the student |
| last_name | VARCHAR | first name of the student |
| hashed_student_id | VARCHAR | unique hashed student id for security and for identification usage |
| email | VARCHAR | required |
| phone_number | VARCHAR | optional |
| whatsapp | VARCHAR | optional |
| discord_handle | VARCHAR | optional |
| facebook name | VARCHAR | optional |
| instagram_handle | VARCHAR | optional |

CourseSection Table

| COLUMN                    | DATA TYPE | NOTES                                      |
| ------------------------- | --------- | ------------------------------------------ |
| course_code               | VARCHAR   | Course ID (e.g. 'CPSC_V 121')              |
| course_name               | VARCHAR   | Course Name (e.g. 'Models of Computation') |
| section_ID                | VARCHAR   | section ID ('101')                         |
| (course_code, section_ID) | VARCHAR   | Composite primary key                      |
| instruction_format        | VARCHAR   | Lab or tutorial or lecture                 |
| meeting_patterns          | VARCHAR   | Meeting times (e.g., "MWF 9:00-10:00")     |
| Delivery_Mode             | VARCHAR   | In-person, online, etc.                    |
| start_date                | DATE      | course start date                          |
| end_date                  | DATE      | course end date                            |

Enrollment Table
| COLUMN | DATA TYPE | NOTES |
| ------ | --------- | ----- |
| enrollment_id | VARCHAR | Composite key of student_id, course_id, section_id, course_start_date. One stuent can only enroll in a course once in the same term, but could enroll in the same course twice in different terms. |
| hashed_student_id | VARCHAR | unique hashed id of the student id for security |
| registeration_status | VARCHAR | registered or waitlisted |
| course_code | VARCHAR | Course code |
| section_code | VARCHAR | 'L1D' |
| enrollment_date | DATE | when this was added to the database |

Notes on the data processing flow:

- User fills out the form and uploads the file.
- The frontend sends a POST request to the backend, containing the form data (firstName, lastName, etc.) and the file.
- The backend processes the file to extract the student ID and course information, generates the hashedID, and return a success msg / error to the front end.
- Why? Seperation of concenrs... Security... file never stays on the frontend

# Notes for future

- Try ORM python libraries
