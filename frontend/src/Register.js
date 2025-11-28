import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import RecaptchaSimulator from './components/RecaptchaSimulator';
import './App.css'; // Asegúrate de que los estilos generales estén importados

export default function Register() {
  const [nombre, setNombre] = useState('');
  const [apellido, setApellido] = useState('');
  const [email, setEmail] = useState('');
  const [tipo, setTipo] = useState('estudiante');
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
      // El backend espera 'tipo', no 'rol'
      const usuario = { nombre, apellido, email, tipo, password };
      const res = await fetch(`${process.env.REACT_APP_API_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(usuario)
      });

      if (res.ok) {
        setMessage('¡Registro exitoso! Redirigiendo al login...');
        setTimeout(() => {
          navigate('/login');
        }, 2000);
      } else {
        const err = await res.json();
        setMessage('Error en el registro: ' + (err.detail || 'Por favor, verifica tus datos.'));
      }
    } catch (error) {
      setMessage('Error de conexión. No se pudo contactar con la API.');
    }
    setLoading(false);
  };

  return (
    <div className="form-container">
      <h2>Crear una cuenta</h2>
      <p>Únete a nuestra comunidad de talento y oportunidades.</p>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Nombre:</label>
          <input type="text" value={nombre} onChange={e => setNombre(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Apellido:</label>
          <input type="text" value={apellido} onChange={e => setApellido(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Email:</label>
          <input type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Quiero registrarme como:</label>
          <select value={tipo} onChange={e => setTipo(e.target.value)} required>
            <option value="estudiante">Estudiante</option>
            <option value="empresa">Empresa</option>
          </select>
        </div>
        <div className="form-group">
          <label>Contraseña:</label>
          <input type="password" minLength={6} value={password} onChange={e => setPassword(e.target.value)} required />
        </div>
        <RecaptchaSimulator onVerify={setIsRobotVerified} />
        <button type="submit" className="btn btn-primary" disabled={loading || !isRobotVerified}>
          {loading ? 'Registrando...' : 'Crear Cuenta'}
        </button>
      </form>
      {message && <div className={`message ${message.startsWith('¡Registro') ? 'message-success' : 'message-error'}`}>{message}</div>}
      <div className="section-divider"></div>
      <p>¿Ya tienes una cuenta? <Link to="/login">Inicia sesión aquí</Link></p>
      <Link to="/" className="btn btn-secondary">
        Volver al inicio
      </Link>
    </div>
  );
}
