import React from 'react';

const icons = {
  gold: '🥇',
  silver: '🥈',
  bronze: '🥉',
  starter: '✨',
  // Vacancy badges
  new: '🆕',
  urgent: '⚡',
  top: '⭐'
};

function Badge({ level = 'starter', label = '', type = 'profile' }) {
  const emoji = icons[level] || icons.starter;
  
  if (type === 'vacancy') {
    return (
      <div className={`vacancy-badge vacancy-badge-${level}`} title={label}>
        <span className="badge-emoji">{emoji}</span>
        <span className="badge-text">{label}</span>
      </div>
    );
  }
  
  return (
    <div className={`badge badge-${level}`} title={label} aria-hidden={false}>
      <div className="badge-emoji">{emoji}</div>
      {label && <div className="badge-label">{label}</div>}
    </div>
  );
}

export default Badge;
