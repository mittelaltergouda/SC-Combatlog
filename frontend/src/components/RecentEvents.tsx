import React, { useRef, useEffect } from 'react';


type RecentEventsProps = {
  events: string;
};

const RecentEvents: React.FC<RecentEventsProps> = ({ events }) => {
  // Spieler-Namen im Text als Hyperlink auf RSI-Profil
  const linkifyNames = (text: string) => {
    return text.replace(/([A-Za-z0-9_\-]{3,})/g, (match) => {
      if (["killed", "by", "at", "with", "on", "in", "the", "and", "from", "to", "for", "a", "an", "of", "is", "was", "as", "vs", "using", "unknown", "npc", "player", "event", "id", "date", "time"].includes(match.toLowerCase())) return match;
      return `<a href="https://robertsspaceindustries.com/citizens/${encodeURIComponent(match)}" target="_blank" rel="noopener noreferrer" style="text-decoration:underline;color:#0074d9">${match}</a>`;
    });
  };
  const preRef = useRef<HTMLPreElement>(null);
  // Scrollposition merken und wiederherstellen
  useEffect(() => {
    const pre = preRef.current;
    if (!pre) return;
    const prevScroll = pre.dataset.scrollTop ? parseInt(pre.dataset.scrollTop) : 0;
    pre.scrollTop = prevScroll;
    return () => {
      if (pre) pre.dataset.scrollTop = String(pre.scrollTop);
    };
    // eslint-disable-next-line
  }, [events]);
  return (
    <div style={{ marginBottom: '20px' }}>
      <h3>Recent Kill Events</h3>
      <pre
        ref={preRef}
        style={{ backgroundColor: '#f9f9f9', padding: '10px', border: '1px solid #ddd', maxHeight: 300, overflow: 'auto' }}
        dangerouslySetInnerHTML={{ __html: linkifyNames(events) }}
      />
    </div>
  );
};

export default RecentEvents;
