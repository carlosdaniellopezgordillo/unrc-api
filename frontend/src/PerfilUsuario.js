import React, { useState } from 'react';
import GestionHabilidades from './GestionHabilidades'; // Importamos el nuevo componente

export default function PerfilUsuario({ user, token, onLogout, onProfileUpdate }) {
  const [editing, setEditing] = useState(null); // Para controlar qué se está editando

  if (!user) {
    return <div>Cargando perfil...</div>;
  }

  const handleProfileUpdate = (updatedUser) => {
    onProfileUpdate(updatedUser); // Pasamos la actualización al componente padre (App.js)
    setEditing(null); // Cerramos el modo de edición
  };

  return (
    <div className="perfil-container">
      <div className="perfil-header">
        <h2>Perfil de {user.nombre} {user.apellido}</h2>
        <p>{user.email}</p>
        <button onClick={onLogout} className="logout-button">Cerrar sesión</button>
      </div>

      {/* Sección de Habilidades */}
      <div className="perfil-seccion">
        <h3>Habilidades</h3>
        {editing === 'habilidades' ? (
          <GestionHabilidades 
            token={token}
            userSkills={user.estudiante?.habilidades || []}
            onProfileUpdate={handleProfileUpdate}
          />
        ) : (
          <>
            <ul className="skills-list">
              {(user.estudiante?.habilidades || []).map(h => <li key={h.id}>{h.nombre}</li>)}
            </ul>
            <button onClick={() => setEditing('habilidades')} className="edit-button">Gestionar Habilidades</button>
          </>
        )}
      </div>

      {/* Sección de Experiencia Laboral */}
      <div className="perfil-seccion">
        <h3>Experiencia Laboral</h3>
        {/* Aquí iría el componente GestionExperiencia cuando lo creemos */}
        <ul className="experience-list">
          {(user.estudiante?.experiencias || []).map(exp => (
            <li key={exp.id}>
              <strong>{exp.puesto}</strong> en {exp.empresa} ({exp.fecha_inicio} - {exp.fecha_fin || 'Actual'})
              <p>{exp.descripcion}</p>
            </li>
          ))}
        </ul>
        <button onClick={() => alert('Funcionalidad en desarrollo')} className="edit-button">Gestionar Experiencia</button>
      </div>

      {/* Sección de Proyectos */}
      <div className="perfil-seccion">
        <h3>Proyectos</h3>
        {/* Aquí iría el componente GestionProyectos cuando lo creemos */}
        <ul className="projects-list">
          {(user.estudiante?.proyectos || []).map(pro => (
            <li key={pro.id}>
              <strong>{pro.nombre}</strong>
              <p>{pro.descripcion}</p>
              {pro.url && <a href={pro.url} target="_blank" rel="noopener noreferrer">Ver Proyecto</a>}
            </li>
          ))}
        </ul>
        <button onClick={() => alert('Funcionalidad en desarrollo')} className="edit-button">Gestionar Proyectos</button>
      </div>
    </div>
  );
}
