import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaUser, FaSearch, FaCheckCircle } from 'react-icons/fa';
import VacancyCard from './VacancyCard';
import SkeletonLoader from './SkeletonLoader';

function Home({ user }) {
  const navigate = useNavigate();
  const [vacantes, setVacantes] = useState([]);
  const [loading, setLoading] = useState(false);

  // Note: Welcome modal state was lifted to App.js. Buttons here now just navigate.
  

  useEffect(() => {
    setLoading(true);
    fetch((process.env.REACT_APP_API_URL || 'http://localhost:8000') + '/oportunidades')
      .then(r => r.json())
      .then(data => setVacantes(Array.isArray(data) ? data.slice(0,6) : []))
      .catch(() => setVacantes([]))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="home-hero">
  {/* WelcomeModal is rendered in App.js (global) */}
      <div className="hero-wrapper">
        <div className="hero-card">
          <div className="hero-left">
            <h1 className="hero-title">Encuentra oportunidades en UNRC</h1>
            <p className="hero-sub">Busca ofertas por habilidades, ubicación o tipo. Completa tu perfil para mejorar las recomendaciones.</p>

            <div className="hero-search">
              <div className="hero-actions">
                <button className="btn" onClick={() => navigate('/oportunidades')}>Ver todas las ofertas</button>
                {!user ? (
                  <>
                    <button className="btn" onClick={() => navigate('/login')}>Ingresar</button>
                    <button className="btn outline" onClick={() => navigate('/register')}>Regístrate</button>
                  </>
                ) : (
                  user.tipo === 'empresa' ? <Link to="/dashboard-empresa" className="btn outline">Publicar oferta</Link> : <Link to="/dashboard-estudiante" className="btn outline">Completar perfil</Link>
                )}
              </div>
              <div className="hero-stats">
                <div className="stat">
                  <strong>+{vacantes.length}</strong>
                  <span>vacantes activas</span>
                </div>
                <div className="stat">
                  <strong>+1200</strong>
                  <span>estudiantes</span>
                </div>
              </div>
            </div>
            {/* Illustration removed: image now shown in the welcome modal to avoid duplication */}

            <aside className="hero-featured">
              <div className="featured-vacancies">
                <h3>Vacantes destacadas</h3>
                {loading && <SkeletonLoader count={1} />}
                {!loading && vacantes.length === 0 && <p>No hay vacantes disponibles.</p>}
                {!loading && vacantes.length > 0 && (
                  <div className="featured-carousel">
                    {vacantes.map(v => (
                      <div key={v.id} className="featured-item" style={{ animation: 'fadeIn 0.3s ease-in' }}>
                        <VacancyCard vac={v} score={0} />
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </aside>
          </div>
        </div>

        <section className="how-it-works">
          <h3>¿Cómo funciona?</h3>
          <div className="how-grid">
            <div className="user-card">
              <div className="card-icon">
                <FaUser />
              </div>
              <h4>1. Crea tu perfil</h4>
              <p>Completa tus datos y sube tu CV para mejorar tu matching.</p>
            </div>
            <div className="user-card">
              <div className="card-icon">
                <FaSearch />
              </div>
              <h4>2. Busca vacantes</h4>
              <p>Filtra por habilidades y aplica en un par de clics.</p>
            </div>
            <div className="user-card">
              <div className="card-icon">
                <FaCheckCircle />
              </div>
              <h4>3. Postula y recibe feedback</h4>
              <p>Las empresas revisan tu perfil y te contactan si encajas.</p>
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

export default Home;
