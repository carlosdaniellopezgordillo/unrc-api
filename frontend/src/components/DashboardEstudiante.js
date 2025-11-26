import React, { useState, useEffect } from 'react';
import { FaUser, FaFileAlt, FaBriefcase } from 'react-icons/fa';
import PerfilEstudiante from './PerfilEstudiante';
import VacancyCard from './VacancyCard';
import SkeletonLoader from './SkeletonLoader';

function OportunidadesFeed({ estudianteId }) {
  const [oportunidades, setOportunidades] = useState([]);
  const [loading, setLoading] = useState(false);
  const [token, setToken] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    setToken(storedToken);
  }, []);

  useEffect(() => {
    if (!token) {
      setError('Token no encontrado. Por favor inicia sesión nuevamente.');
      return;
    }
    
    if (!estudianteId) {
      setError('Perfil de estudiante no configurado. Completa tu perfil primero.');
      return;
    }
    
    setLoading(true);
    setError(null);
    const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    
    fetch(`${apiUrl}/oportunidades/recomendadas/${estudianteId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => {
        if (!res.ok) {
          throw new Error(`Error ${res.status}: No se pudieron cargar las oportunidades`);
        }
        return res.json();
      })
      .then(data => {
        const oportunidadesData = Array.isArray(data) ? data : [];
        setOportunidades(oportunidadesData);
        setError(null);
      })
      .catch(err => {
        console.error('Error al cargar oportunidades:', err);
        setError(`Error: ${err.message}`);
        setOportunidades([]);
      })
      .finally(() => setLoading(false));
  }, [token, estudianteId]);

  return (
    <div className="oportunidades-feed">
      <div className="oportunidades-header">
        <h3>Oportunidades Recomendadas</h3>
        <p>Basadas en tu perfil y habilidades</p>
      </div>
      {loading && <SkeletonLoader count={6} />}
      {!loading && error && (
        <p className="no-data" style={{ color: '#e74c3c', fontWeight: '500' }}>⚠️ {error}</p>
      )}
      {!loading && !error && oportunidades.length === 0 && (
        <p className="no-data">No hay oportunidades recomendadas disponibles.</p>
      )}
      {!loading && oportunidades.length > 0 && (
        <div className="oportunidades-grid">
          {oportunidades.map(rec => (
            <VacancyCard 
              key={rec.oportunidad.id} 
              vac={rec.oportunidad} 
              score={rec.score}
            />
          ))}
        </div>
      )}
    </div>
  );
}

function DashboardEstudiante() {
  const [estudianteId, setEstudianteId] = useState(null);
  const [token, setToken] = useState(null);
  const [loadingProfile, setLoadingProfile] = useState(true);
  const [profileError, setProfileError] = useState(null);
  const [tab, setTab] = useState('perfil');

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    setToken(storedToken);
  }, []);

  // Obtener el ID del estudiante usando el endpoint /me/profile
  useEffect(() => {
    if (!token) {
      setProfileError('Token no encontrado');
      setLoadingProfile(false);
      return;
    }

    const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    fetch(`${apiUrl}/estudiantes/me/profile`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => {
        if (!res.ok) {
          throw new Error(`Error ${res.status}: No se pudo obtener el perfil del estudiante`);
        }
        return res.json();
      })
      .then(data => {
        setEstudianteId(data.id);
        setProfileError(null);
      })
      .catch(err => {
        console.error('Error al obtener perfil:', err);
        setProfileError(`Error: ${err.message}`);
        setEstudianteId(null);
      })
      .finally(() => setLoadingProfile(false));
  }, [token]);

  if (loadingProfile) {
    return (
      <div className="dashboard-estudiante">
        <div className="dashboard-header">
          <h2>Panel de Estudiante</h2>
          <p className="dashboard-subtitle">Cargando...</p>
        </div>
      </div>
    );
  }

  if (profileError) {
    return (
      <div className="dashboard-estudiante">
        <div className="dashboard-header">
          <h2>Panel de Estudiante</h2>
          <p className="dashboard-subtitle">Error al cargar</p>
        </div>
        <p style={{ color: '#e74c3c', fontWeight: '500' }}>⚠️ {profileError}</p>
      </div>
    );
  }

  return (
    <div className="dashboard-estudiante">
      <div className="dashboard-header">
        <h2>Panel de Estudiante</h2>
        <p className="dashboard-subtitle">Gestiona tu perfil y postulaciones</p>
      </div>

      <div className="dashboard-tabs">
        <button 
          className={`tab-button ${tab === 'perfil' ? 'active' : ''}`}
          onClick={() => setTab('perfil')}
        >
          <FaUser className="tab-icon" />
          Mi Perfil
        </button>
        <button 
          className={`tab-button ${tab === 'oportunidades' ? 'active' : ''}`}
          onClick={() => setTab('oportunidades')}
        >
          <FaBriefcase className="tab-icon" />
          Oportunidades
        </button>
      </div>

      <div className="dashboard-content">
        {tab === 'perfil' && <PerfilEstudiante estudianteId={estudianteId} />}
        {tab === 'oportunidades' && <OportunidadesFeed estudianteId={estudianteId} />}
      </div>
    </div>
  );
}

export default DashboardEstudiante;
