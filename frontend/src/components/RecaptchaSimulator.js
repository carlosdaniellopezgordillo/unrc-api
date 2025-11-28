import React, { useState } from 'react';
import { FaRobot } from 'react-icons/fa';
import './RecaptchaSimulator.css';

export default function RecaptchaSimulator({ onVerify }) {
  const [isChecked, setIsChecked] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);

  const handleCheck = async () => {
    setIsVerifying(true);
    // Simulamos una verificación que tarda 1.5 segundos
    setTimeout(() => {
      setIsChecked(true);
      setIsVerifying(false);
      onVerify(true);
    }, 1500);
  };

  const handleReset = () => {
    setIsChecked(false);
    onVerify(false);
  };

  return (
    <div className="recaptcha-container">
      <div className={`recaptcha-box ${isChecked ? 'verified' : ''}`}>
        <div className="recaptcha-checkbox">
          <input
            type="checkbox"
            id="recaptcha-check"
            checked={isChecked}
            onChange={handleCheck}
            disabled={isVerifying}
          />
          <label htmlFor="recaptcha-check">
            {isVerifying ? 'Verificando...' : 'No soy un robot'}
          </label>
        </div>
        {isVerifying && <div className="recaptcha-spinner"></div>}
      </div>
      <div className="recaptcha-logo">
        <FaRobot className="robot-icon" />
        <small>
          <a href="#" onClick={(e) => { e.preventDefault(); }}>
            Privacidad
          </a>
          {' - '}
          <a href="#" onClick={(e) => { e.preventDefault(); }}>
            Términos
          </a>
        </small>
      </div>
      {isChecked && (
        <button 
          type="button" 
          className="recaptcha-reset-btn"
          onClick={handleReset}
        >
          Limpiar verificación
        </button>
      )}
    </div>
  );
}
