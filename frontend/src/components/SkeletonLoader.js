import React from 'react';
import '../styles/SkeletonLoader.css';

function SkeletonLoader({ count = 3 }) {
  return (
    <div className="skeleton-container">
      {Array(count).fill(0).map((_, i) => (
        <div key={i} className="skeleton-card">
          <div className="skeleton-avatar"></div>
          <div className="skeleton-content">
            <div className="skeleton-title"></div>
            <div className="skeleton-text"></div>
            <div className="skeleton-text short"></div>
          </div>
          <div className="skeleton-button"></div>
        </div>
      ))}
    </div>
  );
}

export default SkeletonLoader;
