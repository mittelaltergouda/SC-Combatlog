
import React from 'react';
import Leaderboards from './Leaderboards';
import RecentEvents from './RecentEvents';
import Stats from './Stats';

type MainContentProps = {
  leaderboard: any;
  recent: string;
  stats: string;
};

function MainContent({ leaderboard, recent, stats }: MainContentProps) {
  return (
    <main style={{ padding: '20px' }}>
      <Leaderboards title="Kill Leaderboard" data={leaderboard.kill_leaderboard || []} />
      <Leaderboards title="Death Leaderboard" data={leaderboard.death_leaderboard || []} />
      <RecentEvents events={recent} />
      <Stats stats={stats} />
    </main>
  );
}

export default MainContent;
