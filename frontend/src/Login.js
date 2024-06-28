// Login.js
import React, { useState } from 'react';
import './Login.css'; // Import the CSS file

const Login = ( props ) => {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');
  const [mydata, setMydata] = useState({"mydata":"nodata"})

  const { showLogin, toggleLogin} = props;
   
  function onSignupClick() {
    toggleLogin();
  }

  const handleSubmit = (e) => {
    e.preventDefault();
  };

  return (
    <div>
      <div>Please login</div>
      <form onSubmit={handleSubmit}>
        <label>
          Username or Email:
          <input
            type="text"
            value={identifier}
            onChange={(e) => setIdentifier(e.target.value)}
          />
        </label>
        <label>
          Password:
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </label>
        <button type="submit">Log In</button>
      </form>

      <div className='signup-button-in-login'>  
      <p>
        Don't have an account? 
        <br></br>
      </p>
      <button onClick={onSignupClick}>Sign Up</button>
      </div>

    </div>
  );
};

export default Login;
