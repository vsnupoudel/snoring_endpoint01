// import logo from './logo.svg';
import './App.css';
// import DynamicComponent from './dynamicComponent.js'
import 'bootstrap/dist/css/bootstrap.min.css';
import Login from './Login.js'
import Signup from './Signup.js'
import { useState } from 'react';

function App() {
  const [showLogin, setShowLogin] = useState(false);
  // const [showSignup, setShowSignup] = useState(true);

  const toggleLogin = () => {
    setShowLogin(!showLogin);
  };

  return (
    <div className="App">
      <header className="App-header">
      <div>
      {showLogin ? (
        <Login  showLogin={showLogin} toggleLogin={toggleLogin}/>
      ) : (
        <Signup showLogin={showLogin} toggleLogin={toggleLogin}/>
      )}
    </div>
      </header>
    </div>
  );
}

export default App;
