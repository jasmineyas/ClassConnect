import {useState} from 'react';

function MainContent() {

  return (
    <div className="main-content">
      <div className="file-uploader">
        <p>(1) Upload your workday course export csv file here. Not sure how? </p>
        <input type="file" />
      </div>
      <div className= "contact-form">
        <p>(2) Please share your contact info with your classmates. (Must provide email, otherwise, why are you here?) </p>
        <div>
          <label for="fname">First name: </label>
          <input type="text" id="fname" ></input>
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
      <button>Submit</button>
    </div>
  );
}

export default MainContent;