// Signup.js
import React, { useState } from 'react';
import './Signup.css';

const Signup = ({ onSubmit }) => {
  const [firstName, setFirstName] = useState('');
  const [lastName, setLastName] = useState('');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (password !== repeatPassword) {
      console.log('Passwords do not match.');
      return;
    }

    try {
      // Assuming there's an API function to handle signup
      const userData = {
        firstName,
        lastName,
        username,
        email,
        password,
      };

      // Call the onSubmit function with user data
      onSubmit(userData);
    } catch (error) {
      console.error('Error during signup:', error);
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
      </label>
      <button type="submit">Sign Up</button>
    </form>
  );
};

export default Signup;
