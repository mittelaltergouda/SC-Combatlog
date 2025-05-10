
import React, { useEffect, useState, useRef } from 'react';
import { fetchStats, fetchLeaderboards } from './api/stats';
import Header from './components/Header';
import Modal from 'react-modal';
import { loadPlayerName, loadScPath, savePlayerName, saveScPath } from './api/config';
import Footer from './components/Footer';
import MainContent from './components/MainContent';
import FilterBar from './components/FilterBar';


Modal.setAppElement('#root');

function App() {
  const [stats, setStats] = useState('');
  const [recent, setRecent] = useState('');
  const [leaderboard, setLeaderboard] = useState<any>({ kill_leaderboard: [], death_leaderboard: [] });
  const [filters, setFilters] = useState<any>({});
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [countdown, setCountdown] = useState(0);
  const refreshInterval = useRef<number | ReturnType<typeof setInterval> | null>(null);
  // Komfort: Dialog für Erststart
  const [showSetup, setShowSetup] = useState(false);
  const [setupPlayer, setSetupPlayer] = useState('');
  const [setupPath, setSetupPath] = useState('');
  const [setupError, setSetupError] = useState('');

  const fetchAll = (filterParams = filters) => {
    setIsRefreshing(true);
    fetchStats(filterParams).then(data => {
      setStats(data.stats);
      setRecent(data.recent);
    });
    fetchLeaderboards(filterParams).then(data => setLeaderboard(data)).finally(() => setIsRefreshing(false));
  };

  useEffect(() => {
    // Komfort: Setup-Dialog bei Erststart
    const pn = loadPlayerName();
    const sp = loadScPath();
    if (!pn || !sp) {
      setShowSetup(true);
      setSetupPlayer(pn || '');
      setSetupPath(sp || '');
      return;
    }
    fetchAll();
    setCountdown(60);
    if (refreshInterval.current) clearInterval(refreshInterval.current);
    refreshInterval.current = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) {
          fetchAll();
          return 60;
        }
        return prev - 1;
      });
    }, 1000);
    return () => {
      if (refreshInterval.current) clearInterval(refreshInterval.current);
    };
    // eslint-disable-next-line
  }, [JSON.stringify(filters)]);

  // Komfort: Setup speichern
  const handleSetupSave = () => {
    if (!setupPlayer.trim() || !setupPath.trim()) {
      setSetupError('Bitte Spielername und SC-Pfad angeben!');
      return;
    }
    savePlayerName(setupPlayer.trim());
    saveScPath(setupPath.trim());
    setShowSetup(false);
    setSetupError('');
    setTimeout(() => fetchAll(), 100);
  };

  // Komfort: Electron File-Browser für SC-Pfad
  const handleBrowse = async () => {
    if ((window as any).electron && (window as any).electron.showOpenDialog) {
      const result = await (window as any).electron.showOpenDialog({ properties: ['openDirectory'] });
      if (result && result.filePaths && result.filePaths[0]) {
        setSetupPath(result.filePaths[0]);
      }
    } else {
      alert('Dateiauswahl ist nur in Electron möglich.');
    }
  };

  const handleFilterChange = (newFilters: any) => {
    setFilters(newFilters);
    setCountdown(60);
    fetchAll(newFilters);
  };

  const handleRefresh = () => {
    setCountdown(60);
    fetchAll();
  };

  const handleClearFilters = () => {
    setFilters({});
    setCountdown(60);
    fetchAll({});
  };

  return (
    <>
      <Modal
        isOpen={showSetup}
        contentLabel="Ersteinrichtung"
        style={{ content: { maxWidth: 400, margin: 'auto', inset: 80 } }}
        shouldCloseOnOverlayClick={false}
        shouldCloseOnEsc={false}
        ariaHideApp={false}
      >
        <h2>Ersteinrichtung</h2>
        <div style={{ marginBottom: 10 }}>
          <label>Spielername:<br />
            <input type="text" value={setupPlayer} onChange={e => setSetupPlayer(e.target.value)} style={{ width: '100%' }} />
          </label>
        </div>
        <div style={{ marginBottom: 10 }}>
          <label>SC-Pfad:<br />
            <input type="text" value={setupPath} onChange={e => setSetupPath(e.target.value)} style={{ width: '80%' }} />
            <button onClick={handleBrowse} style={{ marginLeft: 5 }}>Browse</button>
          </label>
        </div>
        {setupError && <div style={{ color: 'red', marginBottom: 10 }}>{setupError}</div>}
        <button onClick={handleSetupSave} style={{ width: '100%' }}>Speichern und starten</button>
      </Modal>
      {!showSetup && (
        <div>
          <Header />
          <FilterBar
            onFilterChange={handleFilterChange}
            onRefresh={handleRefresh}
            isRefreshing={isRefreshing}
            countdown={countdown}
            onClearFilters={handleClearFilters}
          />
          <MainContent leaderboard={leaderboard} recent={recent} stats={stats} />
          <Footer />
        </div>
      )}
    </>
  );
}

export default App;
