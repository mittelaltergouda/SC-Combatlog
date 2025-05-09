

import React, { useState, useEffect } from 'react';
import { fetchLogStatus, fetchDbSize, fetchUpdateCheck, clearAppData } from '../api/system';

function Footer() {
  const [logsProcessed, setLogsProcessed] = useState(0);
  const [totalLogs, setTotalLogs] = useState(0);
  const [dbSize, setDbSize] = useState(0);


  const [updateInfo, setUpdateInfo] = useState<{current_version?: string, latest_version?: string, update_available?: boolean}>({});
  const [clearMsg, setClearMsg] = useState('');

  // Lädt Log-Status, DB-Größe und Update-Info regelmäßig
  useEffect(() => {
    const loadStatus = () => {
      fetchLogStatus().then(data => {
        setLogsProcessed(data.imported);
        setTotalLogs(data.total);
      });
      fetchDbSize().then(data => {
        setDbSize(data.db_size_kb);
      });
      fetchUpdateCheck().then(data => {
        setUpdateInfo(data);
      });
    };
    loadStatus();
    const interval = setInterval(loadStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const handleClearAppData = async () => {
    const res = await clearAppData();
    setClearMsg(res.message || 'AppData gelöscht');
    setTimeout(() => setClearMsg(''), 3000);
  };

  const progress = totalLogs > 0 ? ((logsProcessed / totalLogs) * 100).toFixed(2) : 0;

  return (
    <footer style={{ padding: '10px', backgroundColor: '#f5f5f5', borderTop: '1px solid #ddd', marginTop: '20px' }}>
      <div>
        <span>Logs Processed: {logsProcessed}/{totalLogs} ({progress}%)</span>
        <span style={{ marginLeft: '20px' }}>DB Size: {dbSize} KB</span>
        <span style={{ marginLeft: '20px' }}>
          Version: {updateInfo.current_version || '-'}
          {updateInfo.update_available ? (
            <span style={{ color: 'red', marginLeft: 5 }}>Update verfügbar: {updateInfo.latest_version}</span>
          ) : null}
        </span>
        <button style={{ marginLeft: 20 }} onClick={handleClearAppData}>AppData löschen</button>
        {clearMsg && <span style={{ marginLeft: 10, color: 'green' }}>{clearMsg}</span>}
      </div>
    </footer>
  );
}

export default Footer;
