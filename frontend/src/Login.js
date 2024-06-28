// Login.js
import React, { useState } from 'react';
import './Login.css'; // Import the CSS file

const Login = ( props ) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [mydata, setMydata] = useState({"mydata":"nodata"})

  const { showLogin, toggleLogin} = props;
   
  function onSignupClick() {
    toggleLogin();
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

      // Create an object with user data
      const userData = {
        username,
        password,
      };
  
      console.log (JSON.stringify(userData) )

      
    try {
      // Make the API request
      const response = await fetch('http://localhost:8080/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
      });

      if (response.ok) {
        // Handle successful response (e.g., show a success message)
        const text = await response.json();
        console.log('API response:', text);   
      } else {
        // Handle errors (e.g., show an error message)
        console.error('Error registering user:', response.statusText);
      }
    } catch (error) {
      console.error('Error during API call:', error);
    }

  };

  return (
    <div>
      <div>Please login</div>
      <form onSubmit={handleSubmit}>
        <label>
          Username or Email:
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
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
