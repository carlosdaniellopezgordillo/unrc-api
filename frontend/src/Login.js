import React, { useState } from 'react';
import { FaSignInAlt, FaCheckCircle, FaExclamationTriangle } from 'react-icons/fa';
import { Link, useNavigate } from 'react-router-dom';
import RecaptchaSimulator from './components/RecaptchaSimulator';

export default function Login({ onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [isRobotVerified, setIsRobotVerified] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!isRobotVerified) {
      setMessage('Por favor, verifica que no eres un robot.');
      return;
    }
    
    setLoading(true);
    setMessage('');
    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });
      if (res.ok) {
        const data = await res.json();
        setMessage('¡Login exitoso! Redirigiendo...');
        if (onLogin && data.access_token && data.user) {
          onLogin(data.access_token, data.user); // Pasamos el objeto de usuario completo
          
          // Redirigir según el tipo de usuario
          if (data.user.tipo === 'estudiante') {
            navigate('/dashboard-estudiante');
          } else if (data.user.tipo === 'empresa') {
            navigate('/dashboard-empresa');
          } else {
            navigate('/'); // Fallback a la página de inicio
          }
        }
      } else {
        const err = await res.json();
        setMessage('Error: ' + (err.detail || 'Credenciales inválidas.'));
      }
    } catch (error) {
      setMessage('Error de conexión con la API.');
    }
    setLoading(false);
  };

  return (
    <div className="form-container">
      <h2>Iniciar Sesión</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Email:</label>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Contraseña:</label>
          <input type="password" minLength={6} value={password} onChange={e => setPassword(e.target.value)} required />
        </div>
        <RecaptchaSimulator onVerify={setIsRobotVerified} />
        <button type="submit" className="btn btn-primary" disabled={loading || !isRobotVerified}>
          <FaSignInAlt style={{verticalAlign:'middle', marginRight: '0.5rem'}}/>
          {loading ? 'Entrando...' : 'Entrar'}
        </button>
      </form>
      {message && (
        <div className={`message ${message.startsWith('¡Login') ? 'message-success' : 'message-error'}`}>
          {message.startsWith('¡Login') ? <FaCheckCircle/> : <FaExclamationTriangle/>}
          {message}
        </div>
      )}
      <div className="section-divider"></div>
      <p>¿No tienes una cuenta? <Link to="/register">Regístrate aquí</Link></p>
      <Link to="/" className="btn btn-secondary">
        Volver al inicio
      </Link>
    </div>
  );
}
