import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function WelcomeModal({ visible, onClose }) {
  const [imgError, setImgError] = useState(false);
  const navigate = useNavigate();
  if (!visible) return null;

  const goAndClose = (path) => {
    // Cerrar la modal primero y navegar después con un pequeño delay
    onClose && onClose();
    // small timeout ensures modal unmounts and avoids overlay race conditions
    setTimeout(() => navigate(path), 60);
  };

  return (
    <div className="welcome-modal-overlay" role="dialog" aria-modal="true">
      <div className="welcome-modal-card">
  {/* small corner logo removed to avoid duplicating the main illustration */}
  <button type="button" className="welcome-modal-close" onClick={() => { onClose(); }} aria-label="Cerrar">×</button>

        <div className="welcome-modal-content">
          <div className="welcome-illustration" aria-hidden>
            {!imgError ? (
              <img
                src={process.env.PUBLIC_URL + '/universidad-rosario-castellanos-pirc-pagina-oficial-del-aula-virtual-1.jpg'}
                alt="UNRC"
                onError={() => setImgError(true)}
              />
            ) : (
              <svg width="320" height="160" viewBox="0 0 320 160" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="0" y="0" width="320" height="160" rx="12" fill="#FFFFFF" opacity="0.03"/>
                <circle cx="44" cy="44" r="34" fill="#9F2241" opacity="0.08" />
                <rect x="100" y="18" width="200" height="28" rx="8" fill="#9F2241" opacity="0.08" />
                <rect x="100" y="58" width="200" height="16" rx="8" fill="#9F2241" opacity="0.06" />
                <rect x="100" y="84" width="120" height="12" rx="8" fill="#9F2241" opacity="0.05" />
              </svg>
            )}
          </div>
          <div className="welcome-text">
            <h2>¡Bienvenido a UNRC Conecta!</h2>
            <p>Encuentra oportunidades, completa tu perfil y conecta con empresas. A continuación un breve resumen de cómo funciona la plataforma:</p>

            <ol className="welcome-steps">
              <li><strong>Crea tu perfil:</strong> Completa tus datos y sube tu CV para mejorar tus recomendaciones.</li>
              <li><strong>Busca vacantes:</strong> Filtra por habilidades y aplica en un par de clics.</li>
              <li><strong>Postula y recibe feedback:</strong> Las empresas revisan tu perfil y te contactan si encajas.</li>
            </ol>

            <div className="welcome-actions" style={{ marginTop: '1rem', display:'flex', gap:'0.6rem' }}>
              <button type="button" className="btn" onClick={() => goAndClose('/login')}>Ingresar</button>
              <button type="button" className="btn outline" onClick={() => goAndClose('/register')}>Registrarme</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default WelcomeModal;
