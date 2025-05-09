import React from 'react';

type LeaderboardProps = {
  title: string;
  data: Array<[string, number]>;
};

function Leaderboard({ title, data }: LeaderboardProps) {
  return (
    <div style={{ marginBottom: '20px' }}>
      <h3>{title}</h3>
      <ul>
        {data.map(([name, count], index) => (
          <li key={index}>
            <a
              href={`https://robertsspaceindustries.com/citizens/${encodeURIComponent(name)}`}
              target="_blank"
              rel="noopener noreferrer"
              style={{ textDecoration: 'underline', color: '#0074d9' }}
            >
              {name}
            </a>: {count}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Leaderboard;
