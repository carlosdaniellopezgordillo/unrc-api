import React, { useState, useEffect } from 'react';
import './App.css';
import { Routes, Route, Link, Navigate, useLocation } from 'react-router-dom';
import { FaUserPlus, FaSignInAlt, FaUserCircle, FaSignOutAlt } from 'react-icons/fa';

import Register from './Register';
import Login from './Login';
import Usuarios from './Usuarios';
import PerfilUsuario from './PerfilUsuario';
import DashboardEstudiante from './components/DashboardEstudiante';
import DashboardEmpresa from './components/DashboardEmpresa';
import Home from './components/Home';
import WelcomeModal from './components/WelcomeModal';

// Un componente para proteger rutas
const ProtectedRoute = ({ user, children, role }) => {
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  if (role && user.tipo !== role) {
    return <Navigate to="/" replace />;
  }
  return children;
};


// Home component imported from components/Home.js


function App() {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  const handleLogin = (newToken, userData) => {
    localStorage.setItem('token', newToken);
    localStorage.setItem('user', JSON.stringify(userData));
    setToken(newToken);
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
  };

  // Welcome modal state lifted to App so navigation-driven changes can close it reliably
  const [showWelcome, setShowWelcome] = useState(() => {
    // respect a "no volver a mostrar" flag if present; otherwise show by default
    return localStorage.getItem('noMostrarWelcome') === '1' ? false : true;
  });

  const location = useLocation();

  // Close the welcome modal when the route changes away from home
  useEffect(() => {
    if (location.pathname !== '/') {
      setShowWelcome(false);
    }
  }, [location]);

  return (
    <div className="App">
        <header className="App-header">
          <div className="header-left" style={{ display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
            <img src={process.env.PUBLIC_URL + '/logo urc.png'} alt="Logo UNRC" style={{height:'58px', borderRadius:'8px', boxShadow:'0 2px 8px rgba(0,0,0,0.06)'}} />
            <div>
              <h1 style={{marginBottom:'0.1rem'}}>API Vinculación UNRC</h1>
              <p style={{fontWeight:500, fontSize:'0.9rem', margin:'0'}}>Sistema Inteligente de Gestión del Talento</p>
            </div>
          </div>

          <nav className="header-nav" style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            {!user ? (
              <>
                <Link to="/login" className="btn small"><FaSignInAlt />&nbsp;Ingresar</Link>
                <Link to="/register" className="btn small outline"><FaUserPlus />&nbsp;Registro</Link>
              </>
            ) : (
              <>
                <Link to="/perfil" className="btn small outline"><FaUserCircle />&nbsp;Perfil</Link>
                <button onClick={handleLogout} className="btn small" style={{display:'flex',alignItems:'center',gap:'0.4rem'}}><FaSignOutAlt /> Salir</button>
              </>
            )}
          </nav>
        </header>

        <hr className="section-divider" />
  {/* Welcome modal mounted globally so route changes can reliably close it */}
  <WelcomeModal visible={showWelcome} onClose={() => setShowWelcome(false)} />

  <main>
          <Routes>
            <Route path="/" element={<Home user={user} onLogout={handleLogout} />} />
            <Route path="/register" element={<Register />} />
            <Route path="/login" element={<Login onLogin={handleLogin} />} />
            <Route path="/usuarios" element={<Usuarios />} />

            {/* Rutas Protegidas */}
            <Route 
              path="/perfil" 
              element={
                <ProtectedRoute user={user}>
                  <PerfilUsuario token={token} userId={user?.id} onLogout={handleLogout} />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/dashboard-estudiante" 
              element={
                <ProtectedRoute user={user} role="estudiante">
                  <DashboardEstudiante />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/dashboard-empresa/*" 
              element={
                <ProtectedRoute user={user} role="empresa">
                  <DashboardEmpresa token={token} />
                </ProtectedRoute>
              } 
            />

          </Routes>
        </main>

        <hr className="section-divider" />
        <footer style={{ marginTop: '2rem', padding: '1.5rem 0', textAlign: 'center', color: '#666', borderTop: '1px solid #e0e0e0', fontSize: '0.9rem' }}>
          <p>Desarrollado para la <strong>Universidad Nacional Rosario Castellanos (UNRC)</strong> © 2025</p>
          <p style={{ marginTop: '0.5rem' }}>Proyecto prototípico por estudiantes de 8º semestre de Ciencias de Datos para Negocios, plantel Magdalena Contreras (MAC).</p>
          <p style={{ marginTop: '0.5rem' }}>Contacto: <a href="mailto:soporte@unrc.edu.mx" style={{ color: '#9F2241' }}>soporte@unrc.edu.mx</a></p>
        </footer>
      </div>
  );
}

export default App;
