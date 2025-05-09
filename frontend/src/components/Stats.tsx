import React from 'react';

type StatsProps = {
  stats: string;
};

function Stats({ stats }: StatsProps) {
  return (
    <div style={{ marginBottom: '20px' }}>
      <h3>Statistics</h3>
      <pre style={{ backgroundColor: '#f9f9f9', padding: '10px', border: '1px solid #ddd' }}>{stats}</pre>
    </div>
  );
}

export default Stats;
