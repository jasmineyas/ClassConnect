import React from "react";
import { useState } from "react";
import { useForm } from "react-hook-form";
import logo from "../logo.png";
import GitHub from "../github.png";

function AppTitle() {
  return <img src={logo} alt="logo" />;
}

function StatusBar() {
  return (
    <div>
      <p className="status-bar">
        {" "}
        Classmates: xxxx | Course inventory: xxxx | Connected: xxxxx{" "}
      </p>
    </div>
  );
}

function NextStep() {
  return (
    <div>
      <p>
        Until September 15th, you will receive daily reports if you have new
        classmate matches! After September 15th, you will receive a new match
        email whenever it happens. This is to help reduce noises in your inbox.
        OH, remember to make friends with folks in other department as well!
      </p>
    </div>
  );
}

function Footer() {
  return (
    <div>
      <p>
        © 2024 ClassConnect.{" "}
        <a href="mailto:jasmine_pyz@icloud.com?subject=ClassConnect: I have an idea!&body=Hi Jasmine, here's an idea I have about ClassConnect.">
          Got idea to improve this? Hit me up!This is just an MVP.{" "}
        </a>
        <a href="https://github.com/jasmineyas/ClassConnect/tree/main">
          <img
            className="icons"
            src={GitHub}
            alt="Github"
            width="20"
            height="20"
          ></img>
        </a>
        <a href="https://www.linkedin.com/in/jasmine-pinyu-zou/">
          <img
            className="icons"
            src={GitHub}
            alt="Github"
            width="20"
            height="20"
          ></img>
        </a>
      </p>
    </div>
  );
}

interface StudentData {
  firstName: string;
  lastName: string;
  email: string;
  whatsapp: string;
  hashedID?: string;
  file: File;
}

function MainContent() {
  const [showNextStep, setShowNextStep] = useState(false);
  const { register, handleSubmit } = useForm<StudentData>();

  const onSubmit = (data: StudentData) => {
    const formData = new FormData();
    formData.append("firstName", data.firstName);
    formData.append("lastName", data.lastName);
    formData.append("email", data.email);
    formData.append("whatsapp", data.whatsapp);
    formData.append("file", data.file[0]);

    for (let [key, value] of formData.entries()) {
      console.log(`${key}: ${value}`);
    }

    fetch("/upload", {
      method: "POST",
      body: formData,
    }).then((response) => {
      // Handle response, get hashedID, etc.
    });
    setShowNextStep(true);
  };

  return (
    <div>
      <AppTitle />
      <div className="status-bar">
        <StatusBar />
      </div>
      <div className="main-content">
        {!showNextStep ? (
          <div>
            <form onSubmit={handleSubmit(onSubmit)}>
              <div className="file-uploader">
                <p>
                  (1) Upload your workday course export file here. Not sure how?
                </p>
                <input
                  type="file"
                  accept="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                  {...register("file")}
                />
              </div>
              <p>
                (2) Please share your contact info with your classmates. (Must
                provide email, otherwise, why are you here?)
              </p>
              <div>
                <label>First name: </label>
                <input {...register("firstName")} />
              </div>
              <div>
                <label>Last name: </label>
                <input {...register("lastName")} />
              </div>
              <div>
                <label>Email: </label>
                <input {...register("email")} />
              </div>
              <div>
                <label>WhatsApp: </label>
                <input {...register("whatsapp")} />
              </div>
              <div className="submit-privacy">
                <p>Privacy</p>
                <button type="submit">Submit</button>
              </div>
            </form>
            <div className="footer">
              <Footer />
            </div>
          </div>
        ) : (
          <NextStep />
        )}
      </div>
    </div>
  );
}

export default MainContent;