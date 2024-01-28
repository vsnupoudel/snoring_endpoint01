// import logo from './logo.svg';
import './App.css';
// import DynamicComponent from './dynamicComponent.js'
import Login from './login.js'
import Signup from './signup.js'
import { useState } from 'react';

function App() {
  const [showLogin, setShowLogin] = useState(true);
  const [showSignup, setShowSignup] = useState(false);

  function handleLogin() {
    console.log('handelLogin')
  }
  function handleSignupClick() {
    console.log('handleSignupClick')
  }
  function handleSignup() {
    console.log('handleSignup')
  }
  function handleLoginClick() {
    console.log('handleLoginClick')
  }

  return (
    <div className="App">
      <header className="App-header">
      <div>
      {showLogin ? (
        <Login onSubmit={handleLogin} onSignupClick={handleSignupClick} />
      ) : (
        <Signup onSubmit={handleSignup} onLoginClick={handleLoginClick} />
      )}
    </div>
      </header>
    </div>
  );
}

export default App;
