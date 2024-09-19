# ClassConnect

# Plan

- [x] Define key user stories
- [x] Define MVP scope
- [x] Create mocks for the MVP - very simple one page app.
      ------> ended up not being so simple...
      ![mock](/docs/mock.png)
      ![mock with components](/docs/mvp-mock-with-components.png)
- [x] Define a simple databse schema
- [X] Look into the hashing algorithm for student IDs
- [X] Set up the react app
- [X] Define the states and functionality
- [X] Breakdown tasks
- V1
  - [IP - some bug] create file uploader component
  - [x] create input form component
  - [x] create a hidden success screen
    - [] figure out where the file gets uploaded to google cloud
    - [IP] need to implement a backend: Python with Flask - as it's lightweight and minimalistic. I dont' think I will see super high traffic with this app.
    - [ ] how to implement the logic of parsing the uploaded csv info
    - [ ] how to store the processed student and course info 
  - [X] create the hashing algorithm - no need to create...use existing ones lol MD5
  - [ ] create the matching logic
  - [ ] NOTE: Not only look up the course in this term, but connect you with students of next term as well. I think this is not rly a V5 but it's something very easy that MVP should be able to do. 
- V2
  - [ ] add the logic for getting the stats bar component
- V3
  - [ ] add privacy note pop up
- V4
  - [ ] Add styling to everything...
- [ ] Constraints:
      - [ ] File has to be xlsx
      - [ ] User has to have at least 1 way of contact info
      - [ ] The file has to match the current format (can make it less generic i guess)
- [ ] Define test flows - this should have been done first. Honestly. MY BAD.   
      - [ ] testflow1: missing information in the form
      - [ ] testflow2: excel format updated due to workday updates so processing logic breaks
      - [ ] testflow3: wrong excel file
      - [ ] testflow4: user update their file after iniital upload
      - [ ] testflow5: user update their contact info
      - [ ] testflow6: user upload a different student's schedule
      - [ ] testflow7: 
- [ ] Carry out the test flows
- [ ] Invite beta testers
- [ ] Iterate based on feedback
- [ ] Clean up readme file...

# key user stories

- As a new BCS student, I want to be able to find folks in my cohorts, who are in the same course as well as the same lecture, lab and discussion sections as me so that I can connect with them and form study groups, or pair up as lab / porject partners.
- Students should be able to upload their course schedule and get notified of other students who are in their course, as well as who share the same lecture, lab and discussion sections.
- Students should be able to share their contact information if they wish to be contacted by other users.

# MVP scope

- There's a button to upload a schedule.
- There's a status bar to show how many people have uploaded their schedules, and list of courses and number of people in each course.
- Hasing algorithm has to be implemented for privacy reasons.
- There's a blurb that talk about the purpose of app and how it works (aka people get email at 5pm daily of updates).
- [br]MVP Note! It is posisble the email update feature will be hard to implement...if it's hard...we could forgo this and just display information on the app... and we could display a message to the user to check back the next day if they don't see any matches. Or send email to users when 'five' more folks have uploaded their schedules.
  &nbsp;&nbsp;&nbsp;&nbsp;when the database has new matches for a given users:
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Users get an email with new matches

# Database Schema:

- User:
  - full_name: string
  - email: string
  - hashed_id: string
  - phone_number: number #optional
  - discord_handle: string #optional
  - contact_on_facebook: boolean #optional
  - instagram_handle: string #optional
- Course:
  - course_listing: string #UniqueCourseID
  - instruction_format: string #{lecture,lecture, discussion}
  - section_id: string #UniqueSectionID
  - number_of_students: number #for each section
  - contained_users: array of user_hased_ids and user_contacts
    - [[User_hashed_id, user_name, various_User_contact_info],
    - [User_hashed_id, user_name, various_User_contact_info],
    - ...]

#NOTES:
Flow for the data processing:

- User fills out the form and uploads the file.
- The frontend sends a POST request to the backend, containing the form data (firstName, lastName, etc.) and the file.
- The backend processes the file to extract the student ID, generates the hashedID, and returns the hashed data to the frontend or stores it.
  Why?
  Seperation of concenrs...
  Security... file never stays on the frontend
