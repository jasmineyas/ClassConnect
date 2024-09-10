import {useState} from 'react';

function NextStep(){
  return(
    <div>
      <p>Until September 15th, you will receive daily reports if you have new 
        classmate matches! After September 15th, you will receive a new match
        email whenever it happens. This is to help reduce noises in your inbox. 

        OH, remember to make friends with folks in other department as well!  
      </p>
    </div>
  )
}

function MainContent() {
  const [showNextStep, setShowNextStep] = useState(false)
  const handleSubmit = () => setShowNextStep(true)

  return (
    <div className="main-content">
      {!showNextStep ? 
        <div>
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
          <button onClick={handleSubmit}>Submit</button>  
        </div>
        : <NextStep /> }
    </div>
  );
}

export default MainContent;