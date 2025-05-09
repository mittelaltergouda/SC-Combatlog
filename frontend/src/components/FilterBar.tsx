import React, { useState } from 'react';

const entityOptions = [
  { key: 'players', label: 'Spieler' },
  { key: 'unknown', label: 'Unbekannt' },
  { key: 'npc_pilot', label: 'NPC Pilot' },
  { key: 'npc_civilian', label: 'NPC Zivilist' },
  { key: 'npc_worker', label: 'NPC Arbeiter' },
  { key: 'npc_lawenforcement', label: 'NPC Gesetz' },
  { key: 'npc_gunner', label: 'NPC Gunner' },
  { key: 'npc_technical', label: 'NPC Techniker' },
  { key: 'npc_test', label: 'NPC Test' },
  { key: 'npc_pirate', label: 'NPC Pirat' },
  { key: 'npc_ground', label: 'NPC Boden' },
  { key: 'npc_animal', label: 'NPC Tier' },
  { key: 'npc_uncategorized', label: 'NPC Unkategorisiert' },
];

function FilterBar({ onFilterChange, onRefresh, isRefreshing, countdown, onClearFilters }: any) {
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [entities, setEntities] = useState<{[key:string]: boolean}>(
    Object.fromEntries(entityOptions.map(opt => [opt.key, true]))
  );

  const handleDateChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.name === 'start') setStartDate(e.target.value);
    else setEndDate(e.target.value);
  };

  const handleEntityChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setEntities({ ...entities, [e.target.name]: e.target.checked });
  };

  const handleApply = () => {
    onFilterChange({ startDate, endDate, ...entities });
  };

  return (
    <div style={{ padding: '10px', background: '#eef', borderBottom: '1px solid #ccc', display: 'flex', flexDirection: 'column', gap: 8 }}>
      <div>
        <label>Start: <input type="date" name="start" value={startDate} onChange={handleDateChange} /></label>
        <label style={{ marginLeft: 10 }}>Ende: <input type="date" name="end" value={endDate} onChange={handleDateChange} /></label>
        <button onClick={handleApply} style={{ marginLeft: 10 }}>Filter anwenden</button>
        <button onClick={onClearFilters} style={{ marginLeft: 5 }}>Filter zurücksetzen</button>
        <button onClick={onRefresh} style={{ marginLeft: 20 }} disabled={isRefreshing}>
          {isRefreshing ? `Aktualisiere... (${countdown}s)` : 'Refresh'}
        </button>
      </div>
      <div>
        {entityOptions.map(opt => (
          <label key={opt.key} style={{ marginRight: 8 }}>
            <input type="checkbox" name={opt.key} checked={entities[opt.key]} onChange={handleEntityChange} />
            {opt.label}
          </label>
        ))}
      </div>
    </div>
  );
}

export default FilterBar;
