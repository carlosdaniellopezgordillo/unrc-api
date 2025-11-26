import React from 'react';
import { FaUser, FaGraduationCap, FaCode, FaTrophy, FaStar } from 'react-icons/fa';

function StudentCard({ student, compatibilityScore = 0 }) {
  const { 
    usuario, 
    matricula, 
    semestre, 
    carrera, 
    gpa,
    habilidades_tecnicas = [],
    habilidades_blandas = [],
    proyectos = []
  } = student || {};

  const studentName = usuario?.nombre || 'Estudiante';
  const initials = studentName.split(' ').map(s => s[0]).slice(0, 2).join('').toUpperCase();

  // Determinar color basado en GPA
  const getGPAColor = (gpa) => {
    if (gpa >= 3.8) return { color: '#10b981', label: 'Excelente' };
    if (gpa >= 3.5) return { color: '#3b82f6', label: 'Muy bien' };
    if (gpa >= 3.0) return { color: '#f59e0b', label: 'Bien' };
    return { color: '#ef4444', label: 'Regular' };
  };

  const gpaInfo = getGPAColor(gpa);

  return (
    <div className="student-card-enhanced">
      {/* Barra superior de color basado en GPA */}
      <div className="student-card-top-bar" style={{ backgroundColor: gpaInfo.color }}></div>

      {/* Header con avatar y nombre */}
      <div className="student-header">
        <div className="student-avatar" style={{ backgroundColor: gpaInfo.color }}>
          {initials}
        </div>
        <div className="student-info">
          <div className="student-name">{studentName}</div>
          <div className="student-matricula">ID: {matricula || 'N/A'}</div>
        </div>
        <div className="student-gpa">
          <div className="gpa-badge" style={{ backgroundColor: `${gpaInfo.color}22`, borderColor: gpaInfo.color }}>
            <FaStar style={{ color: gpaInfo.color, marginRight: '0.3rem' }} />
            {gpa?.toFixed(2) || 'N/A'}
          </div>
        </div>
      </div>

      {/* Información académica */}
      <div className="student-academic">
        <div className="academic-item">
          <FaGraduationCap className="academic-icon" />
          <div className="academic-content">
            <span className="academic-label">Semestre</span>
            <p>{semestre || 'N/A'}</p>
          </div>
        </div>
        <div className="academic-item">
          <FaTrophy className="academic-icon" />
          <div className="academic-content">
            <span className="academic-label">Carrera</span>
            <p>{carrera || 'No especificada'}</p>
          </div>
        </div>
      </div>

      {/* Habilidades Técnicas */}
      {habilidades_tecnicas && habilidades_tecnicas.length > 0 && (
        <div className="student-skills-section">
          <div className="skills-header">
            <FaCode style={{ marginRight: '0.4rem', color: '#3b82f6' }} />
            Habilidades Técnicas
          </div>
          <div className="skills-container">
            {habilidades_tecnicas.slice(0, 5).map((skill, idx) => (
              <span className="skill-chip-student" key={idx}>{skill}</span>
            ))}
            {habilidades_tecnicas.length > 5 && (
              <span className="skill-chip-student more">+{habilidades_tecnicas.length - 5}</span>
            )}
          </div>
        </div>
      )}

      {/* Habilidades Blandas */}
      {habilidades_blandas && habilidades_blandas.length > 0 && (
        <div className="student-skills-section">
          <div className="skills-header">
            💬 Habilidades Blandas
          </div>
          <div className="skills-container">
            {habilidades_blandas.slice(0, 4).map((skill, idx) => (
              <span className="skill-chip-soft" key={idx}>{skill}</span>
            ))}
            {habilidades_blandas.length > 4 && (
              <span className="skill-chip-soft more">+{habilidades_blandas.length - 4}</span>
            )}
          </div>
        </div>
      )}

      {/* Proyectos */}
      {proyectos && proyectos.length > 0 && (
        <div className="student-projects-section">
          <div className="projects-header">
            📁 Proyectos ({proyectos.length})
          </div>
          <div className="projects-list">
            {proyectos.slice(0, 3).map((project, idx) => (
              <div className="project-item" key={idx}>
                <span className="project-dot">→</span>
                <span className="project-name">{project}</span>
              </div>
            ))}
            {proyectos.length > 3 && (
              <div className="project-item">
                <span className="project-dot">+</span>
                <span className="project-more">{proyectos.length - 3} más</span>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Barra de compatibilidad y botón */}
      <div className="student-footer">
        <div className="compatibility-section">
          <div className="compatibility-bar">
            <div 
              className="compatibility-fill" 
              style={{ 
                width: `${Math.min(100, Math.round(compatibilityScore || 0))}%`,
                backgroundColor: compatibilityScore >= 70 ? '#10b981' : compatibilityScore >= 40 ? '#f59e0b' : '#ef4444'
              }} 
            />
          </div>
          <div className="compatibility-text">
            <span>{Math.round(compatibilityScore || 0)}% compatible</span>
          </div>
        </div>
        <button className="student-contact-btn">
          <FaUser style={{ marginRight: '0.4rem' }} />
          Ver Perfil
        </button>
      </div>
    </div>
  );
}

export default StudentCard;
