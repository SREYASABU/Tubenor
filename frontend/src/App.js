import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Chat from './components/Chat';
import OAuthCallback from './components/OAuthCallback';
import './styles/App.css';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Chat />} />
          <Route path="/oauth/callback" element={<OAuthCallback />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

