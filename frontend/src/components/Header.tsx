
import React, { useState, useEffect } from 'react';
import { savePlayerName, saveScPath, loadPlayerName, loadScPath } from '../api/config';



function Header() {
  const [playerName, setPlayerName] = useState('');
  const [scPath, setScPath] = useState('');
  const [feedback, setFeedback] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    setPlayerName(loadPlayerName());
    setScPath(loadScPath());
  }, []);

  const handlePlayerNameChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setPlayerName(e.target.value);
    setError('');
  };

  const handleScPathChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setScPath(e.target.value);
    setError('');
  };

  const applyPlayerName = () => {
    if (!playerName.trim()) {
      setError('Spielername darf nicht leer sein!');
      return;
    }
    savePlayerName(playerName);
    setFeedback('Spielername gespeichert!');
    setTimeout(() => setFeedback(''), 2000);
  };

  const applyScPath = () => {
    if (!scPath.trim()) {
      setError('SC Path darf nicht leer sein!');
      return;
    }
    saveScPath(scPath);
    setFeedback('SC Path gespeichert!');
    setTimeout(() => setFeedback(''), 2000);
  };

  // Electron-spezifischer File-Dialog (optional, hier Dummy)
  const handleBrowse = () => {
    alert('Dateiauswahl ist in Electron möglich, hier als Platzhalter.');
  };

  return (
    <header style={{ padding: '10px', backgroundColor: '#f5f5f5', borderBottom: '1px solid #ddd' }}>
      <h1>SC Griefing Counter</h1>
      <div>
        <label>Player Name: </label>
        <input
          type="text"
          placeholder="Enter player name"
          value={playerName}
          onChange={handlePlayerNameChange}
        />
        <button onClick={applyPlayerName}>Apply</button>
      </div>
      <div>
        <label>SC Path: </label>
        <input
          type="text"
          placeholder="Enter SC path"
          value={scPath}
          onChange={handleScPathChange}
        />
        <button onClick={handleBrowse}>Browse</button>
        <button onClick={applyScPath}>Apply Path</button>
      </div>
      {error && <div style={{ color: 'red', marginTop: 5 }}>{error}</div>}
      {feedback && <div style={{ color: 'green', marginTop: 5 }}>{feedback}</div>}
    </header>
  );
}

export default Header;
