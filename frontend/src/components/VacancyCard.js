import React from 'react';
import { FaMapMarkerAlt, FaUsers, FaClock, FaDollarSign, FaCheckCircle, FaBriefcase } from 'react-icons/fa';
import Badge from './Badge';

function VacancyCard({ vac, score }) {
  const { id, titulo, descripcion = '', habilidades_requeridas = [], ubicacion, modalidad, salario, tipo, fecha_publicacion } = vac || {};
  
  // Obtener información de empresa desde múltiples posibles ubicaciones
  const company = vac?.empresa || vac?.empresa_obj || vac?.empresa_data || {};
  const companyName = company?.nombre || company?.name || vac?.empresa_name || `Empresa`;

  const initials = (companyName || 'E').split(' ').map(s => s[0]).slice(0,2).join('').toUpperCase();

  // Determinar badges automáticamente
  const getDaysSinceCreated = () => {
    if (!fecha_publicacion) return null;
    const createdDate = new Date(fecha_publicacion);
    const now = new Date();
    const days = Math.floor((now - createdDate) / (1000 * 60 * 60 * 24));
    return days;
  };

  const days = getDaysSinceCreated();
  const isNew = days !== null && days <= 3;

  // Mapear tipo a color y duración estimada
  const tipoConfig = {
    'empleo': { label: 'Empleo', color: '#2ecc71', icon: '💼', bgColor: 'rgba(46, 204, 113, 0.1)' },
    'practica': { label: 'Prácticas', color: '#3498db', icon: '📚', bgColor: 'rgba(52, 152, 219, 0.1)' },
    'servicio_social': { label: 'Servicio Social', color: '#9b59b6', icon: '🤝', bgColor: 'rgba(155, 89, 182, 0.1)' }
  };

  const tipoInfo = tipoConfig[tipo] || { label: tipo, color: '#34495e', icon: '📋', bgColor: 'rgba(52, 73, 94, 0.1)' };

  const getModalidadIcon = (mod) => {
    const mods = {
      'presencial': '🏢',
      'remoto': '💻',
      'hibrido': '🔄'
    };
    return mods[mod] || '📍';
  };

  return (
    <div className="vacancy-card-enhanced">
      {/* Badges en la esquina superior derecha */}
      <div className="vacancy-badges-container">
        {isNew && <Badge type="vacancy" level="new" label="Recién publicada" />}
      </div>

      {/* Tipo de oportunidad - Badge de color */}
      <div className="vacancy-type-badge" style={{ backgroundColor: tipoInfo.bgColor, borderLeft: `4px solid ${tipoInfo.color}` }}>
        <span className="type-icon">{tipoInfo.icon}</span>
        <span className="type-label">{tipoInfo.label}</span>
      </div>

      {/* Encabezado con empresa */}
      <div className="vacancy-header">
        <div className="company-avatar-enhanced" style={{ backgroundColor: tipoInfo.color }}>
          {initials}
        </div>
        <div className="company-info">
          <div className="company-name-enhanced">{companyName}</div>
          <div className="vacancy-title">{titulo}</div>
        </div>
      </div>

      {/* Descripción */}
      <div className="vacancy-description">
        <p>{(descripcion || '').slice(0, 180)}{descripcion && descripcion.length > 180 ? '...' : ''}</p>
      </div>

      {/* Skills requeridas */}
      {habilidades_requeridas && habilidades_requeridas.length > 0 && (
        <div className="vacancy-skills">
          <div className="skills-label">Habilidades:</div>
          <div className="skills-container">
            {habilidades_requeridas.slice(0, 4).map(h => (
              <span className="skill-chip" key={h}>{h}</span>
            ))}
            {habilidades_requeridas.length > 4 && (
              <span className="skill-chip more">+{habilidades_requeridas.length - 4}</span>
            )}
          </div>
        </div>
      )}

      {/* Información detallada */}
      <div className="vacancy-details">
        <div className="detail-item">
          <FaMapMarkerAlt className="detail-icon" />
          <span className="detail-text">{ubicacion || 'Ubicación'}</span>
        </div>
        <div className="detail-item">
          <span className="detail-icon">{getModalidadIcon(modalidad)}</span>
          <span className="detail-text">{modalidad ? modalidad.charAt(0).toUpperCase() + modalidad.slice(1) : 'Modalidad'}</span>
        </div>
        {salario && (
          <div className="detail-item">
            <FaDollarSign className="detail-icon" style={{ color: '#27ae60' }} />
            <span className="detail-text" style={{ fontWeight: '600', color: '#27ae60' }}>
              ${typeof salario === 'number' ? salario.toLocaleString('es-ES') : salario}
            </span>
          </div>
        )}
      </div>

      {/* Barra de compatibilidad y botón */}
      <div className="vacancy-footer">
        <div className="compatibility-section">
          <div className="compatibility-bar">
            <div 
              className="compatibility-fill" 
              style={{ 
                width: `${Math.min(100, Math.round(score || 0))}%`,
                backgroundColor: score >= 70 ? '#27ae60' : score >= 40 ? '#f39c12' : '#e74c3c'
              }} 
            />
          </div>
          <div className="compatibility-text">
            <FaCheckCircle style={{ color: score >= 70 ? '#27ae60' : '#95a5a6', fontSize: '0.85rem' }} />
            <span>{score}% compatible</span>
          </div>
        </div>
        <a href={`http://localhost:8000/oportunidades/${id}`} target="_blank" rel="noreferrer">
          <button className="vacancy-btn">
            <FaBriefcase style={{ marginRight: '0.5rem' }} />
            Ver oferta
          </button>
        </a>
      </div>
    </div>
  );
}

export default VacancyCard;
