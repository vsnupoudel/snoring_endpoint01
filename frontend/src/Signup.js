// Signup.js
import React, { useState } from 'react';
import './Signup.css';

const Signup = ( props ) => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const {  showLogin, toggleLogin} = props;


    // Create an object with user data
    const userData = {
      firstName,
      lastName,
      username,
      email,
      password,
    };

    console.log (JSON.stringify(userData) )

    try {
      // Make the API request
      const response = await fetch('http://localhost:8080/register', {
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
        toggleLogin();  
      } else {
        // Handle errors (e.g., show an error message)
        console.error('Error registering user:', response.statusText);
      }
    } catch (error) {
      console.error('Error during API call:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        First Name (Optional):
        <input
          type="text"
          value={firstName}
          onChange={(e) => setFirstName(e.target.value)}
        />
      </label>
      <label>
        Last Name (Optional):
        <input
          type="text"
          value={lastName}
          onChange={(e) => setLastName(e.target.value)}
        />
      </label>
      <label>
        Username:
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
      </label>
      <label>
        Email:
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </label>
      <label>
        Password:
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </label>
      <label>
        Repeat Password:
        <input
          type="password"
          value={repeatPassword}
          onChange={(e) => setRepeatPassword(e.target.value)}
          required
        />
        {password !== repeatPassword && (
      <p style={{ color: 'red' }}>Passwords do not match</p>
    )}
      </label>
      <button type="submit">Sign Up</button>
    </form>
  );
};

export default Signup;
