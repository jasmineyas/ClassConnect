import { useState } from "react";
import logo from "../logo.png";
import GitHub from "../github.png";

function AppTitle() {
  return <img src={logo}></img>;
}

function StatusBar() {
  return (
    <div>
      <p class="status-bar">
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

function MainContent() {
  const [showNextStep, setShowNextStep] = useState(false);
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]); // Get the selected file
  };

  const handleSubmit = () => {
    // if (!file) {
    //   alert("Please upload your workday course export csv file.");
    //   return;
    // }
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
            <div className="file-uploader">
              <p>
                (1) Upload your workday course export csv file here. Not sure
                how?
              </p>
              <input type="file" accept=".csv" onChange={handleFileChange} />
            </div>
            <div className="contact-form">
              <p>
                (2) Please share your contact info with your classmates. (Must
                provide email, otherwise, why are you here?)
              </p>
              <div>
                <label for="fname">First name: </label>
                <input type="text" id="fname"></input>
              </div>
              <div>
                <label for="lname">Last name: </label>
                <input type="text" id="lname"></input>
              </div>

              <div>
                <label for="email">Email: </label>
                <input type="text" id="email"></input>
              </div>
              <div>
                <label for="phone">WhatsApp: </label>
                <input type="text" id="whatsapp"></input>
              </div>
            </div>
            <div className="submit-privacy">
              <p>Privacy</p>
              <button onClick={handleSubmit}>Submit</button>
            </div>
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
