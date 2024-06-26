// Login.js
import React, { useState } from 'react';
import './Login.css'; // Import the CSS file

const Login = ({ onSubmit, onSignupClick, msg }) => {
  const [identifier, setIdentifier] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(identifier, password);
  };

  return (
    <div>
      <div>{msg}</div>
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
      <p>
        Don't have an account? <button onClick={onSignupClick}>Sign Up</button>
      </p>
    </div>
  );
};

export default Login;
