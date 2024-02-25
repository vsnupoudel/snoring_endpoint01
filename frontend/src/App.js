// import logo from './logo.svg';
import './App.css';
// import DynamicComponent from './dynamicComponent.js'
import 'bootstrap/dist/css/bootstrap.min.css';
import Login from './Login.js'
import Signup from './Signup.js'
import { useState } from 'react';

function App() {
  const [showLogin, setShowLogin] = useState(false);
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
