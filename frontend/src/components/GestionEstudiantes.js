import React, { useState, useEffect } from 'react';
import { FaUser, FaSearch, FaFilter, FaSortAmountDown } from 'react-icons/fa';
import StudentCard from './StudentCard';
import './GestionEstudiantes.css';

const GestionEstudiantes = ({ token }) => {
  const [estudiantes, setEstudiantes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('gpa');
  const [filterHabilidad, setFilterHabilidad] = useState('');
  const [availableSkills, setAvailableSkills] = useState([]);
  const [error, setError] = useState('');

  const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  useEffect(() => {
    const fetchEstudiantes = async () => {
      console.log('🔍 Iniciando fetchEstudiantes');
      console.log('📡 API URL:', apiUrl);
      try {
        const fetchUrl = `${apiUrl}/auth/usuarios/estudiantes`;
        console.log('🌐 Llamando a:', fetchUrl);
        const res = await fetch(fetchUrl);
        console.log('✅ Response recibido:', res);
        console.log('📊 Response status:', res.status);
        console.log('📊 Response ok:', res.ok);
        
        if (res.ok) {
          const data = await res.json();
          console.log('✅ Datos parseados exitosamente');
          console.log('📊 Estudiantes obtenidos:', data);
          console.log('📊 Cantidad de estudiantes:', data.length);
          setEstudiantes(data);
          
          // Extraer todas las habilidades únicas
          const skills = new Set();
          data.forEach(est => {
            if (est.habilidades_tecnicas && Array.isArray(est.habilidades_tecnicas)) {
              est.habilidades_tecnicas.forEach(h => skills.add(h));
            }
          });
          const skillsArray = Array.from(skills).sort();
          console.log('📊 Habilidades encontradas:', skillsArray.length);
          setAvailableSkills(skillsArray);
        } else {
          console.error('❌ Error status:', res.status);
          const errorText = await res.text();
          console.error('❌ Error response:', errorText);
          setError('No se pudieron cargar los estudiantes.');
        }
      } catch (err) {
        setError('Error de conexión al cargar estudiantes.');
        console.error('❌ Error completo:', err);
        console.error('❌ Stack:', err.stack);
      } finally {
        setLoading(false);
      }
    };

    console.log('🎬 useEffect disparado, apiUrl:', apiUrl);
    fetchEstudiantes();
  }, [apiUrl]);

  // Filtrar y ordenar estudiantes
  const filteredEstudiantes = estudiantes
    .filter(est => {
      const nombre = est.usuario?.nombre?.toLowerCase() || est.nombre?.toLowerCase() || '';
      const carrera = est.carrera?.toLowerCase() || '';
      const search = searchTerm.toLowerCase();
      
      const matchSearch = nombre.includes(search) || carrera.includes(search);
      const matchSkill = !filterHabilidad || 
        (est.habilidades_tecnicas && est.habilidades_tecnicas.includes(filterHabilidad));
      
      return matchSearch && matchSkill;
    })
    .sort((a, b) => {
      switch(sortBy) {
        case 'gpa':
          return (b.gpa || 0) - (a.gpa || 0);
        case 'semestre':
          return (b.semestre || 0) - (a.semestre || 0);
        case 'nombre':
          const nameA = a.usuario?.nombre || a.nombre || '';
          const nameB = b.usuario?.nombre || b.nombre || '';
          return nameA.localeCompare(nameB);
        default:
          return 0;
      }
    });

  if (loading) return (
    <div className="gestion-estudiantes-loading">
      <p>Cargando estudiantes...</p>
    </div>
  );

  return (
    <div className="gestion-estudiantes-container">
      {/* Header */}
      <div className="gestion-header">
        <div className="gestion-header-title">
          <FaUser className="gestion-header-icon" />
          <div>
            <h2>Talento Disponible</h2>
            <p>Explora a los mejores estudiantes de UNRC</p>
          </div>
        </div>
        <div className="gestion-stats">
          <div className="stat-card">
            <span className="stat-number">{filteredEstudiantes.length}</span>
            <span className="stat-label">Estudiantes</span>
          </div>
          <div className="stat-card">
            <span className="stat-number">{availableSkills.length}</span>
            <span className="stat-label">Habilidades</span>
          </div>
        </div>
      </div>

      {/* Filtros y búsqueda */}
      <div className="gestion-filters">
        <div className="search-box">
          <FaSearch className="search-icon" />
          <input
            type="text"
            placeholder="Buscar por nombre o carrera..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="search-input"
          />
        </div>

        <div className="filters-row">
          <div className="filter-group">
            <label className="filter-label">
              <FaFilter style={{ marginRight: '0.4rem' }} />
              Filtrar por Habilidad
            </label>
            <select 
              value={filterHabilidad} 
              onChange={(e) => setFilterHabilidad(e.target.value)}
              className="filter-select"
            >
              <option value="">Todas las habilidades</option>
              {availableSkills.map(skill => (
                <option key={skill} value={skill}>{skill}</option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label className="filter-label">
              <FaSortAmountDown style={{ marginRight: '0.4rem' }} />
              Ordenar por
            </label>
            <select 
              value={sortBy} 
              onChange={(e) => setSortBy(e.target.value)}
              className="filter-select"
            >
              <option value="gpa">GPA (Mayor a Menor)</option>
              <option value="semestre">Semestre (Mayor a Menor)</option>
              <option value="nombre">Nombre (A-Z)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Error message */}
      {error && (
        <div className="gestion-error">
          {error}
        </div>
      )}

      {/* Grid de estudiantes */}
      {filteredEstudiantes.length === 0 && estudiantes.length === 0 ? (
        <div className="gestion-no-results">
          <FaUser className="no-results-icon" />
          <p>No se encontraron estudiantes en la base de datos.</p>
          <p style={{ fontSize: '0.9rem', color: '#999' }}>Debug: Estudiantes cargados = {estudiantes.length}, Filtrados = {filteredEstudiantes.length}</p>
        </div>
      ) : filteredEstudiantes.length === 0 ? (
        <div className="gestion-no-results">
          <FaUser className="no-results-icon" />
          <p>No se encontraron estudiantes con los criterios seleccionados.</p>
          <p style={{ fontSize: '0.9rem', color: '#999' }}>Debug: Total disponibles = {estudiantes.length}</p>
        </div>
      ) : (
        <div className="estudiantes-grid">
          {filteredEstudiantes.map(estudiante => (
            <StudentCard 
              key={estudiante.id} 
              student={estudiante}
              compatibilityScore={estudiante.gpa ? (estudiante.gpa / 4.0) * 100 : 0}
            />
          ))}
        </div>
      )}
    </div>
  );
};

export default GestionEstudiantes;
