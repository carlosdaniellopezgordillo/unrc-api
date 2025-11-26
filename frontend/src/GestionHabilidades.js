import React, { useState, useEffect } from 'react';

export default function GestionHabilidades({ token, userSkills, onProfileUpdate }) {
  const [allSkills, setAllSkills] = useState([]);
  const [availableSkills, setAvailableSkills] = useState([]);
  const [selectedSkill, setSelectedSkill] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  // 1. Cargar todas las habilidades existentes en el sistema
  useEffect(() => {
    async function fetchAllSkills() {
      try {
        const res = await fetch(`${process.env.REACT_APP_API_URL}/habilidades/`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setAllSkills(data);
        }
      } catch (err) {
        setError('No se pudieron cargar las habilidades.');
      }
    }
    fetchAllSkills();
  }, [token]);

  // 2. Filtrar las habilidades que el usuario ya tiene para mostrar solo las que puede añadir
  useEffect(() => {
    if (allSkills.length > 0) {
      const userSkillIds = new Set(userSkills.map(s => s.id));
      const skillsToAdd = allSkills.filter(s => !userSkillIds.has(s.id));
      setAvailableSkills(skillsToAdd);
      if (skillsToAdd.length > 0) {
        setSelectedSkill(skillsToAdd[0].id);
      }
    }
  }, [allSkills, userSkills]);

  // 3. Llamar a la API para AÑADIR una habilidad
  const handleAddSkill = async () => {
    if (!selectedSkill) return;
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/habilidades/me/${selectedSkill}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const updatedUser = await res.json();
        onProfileUpdate(updatedUser); // Notificar al componente padre que el perfil se actualizó
      } else {
        const err = await res.json();
        setError(err.detail || 'Error al añadir habilidad.');
      }
    } catch (err) {
      setError('Error de conexión al añadir habilidad.');
    }
    setLoading(false);
  };

  // 4. Llamar a la API para ELIMINAR una habilidad
  const handleRemoveSkill = async (skillId) => {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${process.env.REACT_APP_API_URL}/habilidades/me/${skillId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (res.ok) {
        const updatedUser = await res.json();
        onProfileUpdate(updatedUser); // Notificar al componente padre que el perfil se actualizó
      } else {
        const err = await res.json();
        setError(err.detail || 'Error al eliminar habilidad.');
      }
    } catch (err) {
      setError('Error de conexión al eliminar habilidad.');
    }
    setLoading(false);
  };

  return (
    <div className="gestion-seccion">
      <h4>Gestionar Mis Habilidades</h4>
      
      {/* Sección para añadir nuevas habilidades */}
      <div className="add-item-form">
        <select value={selectedSkill} onChange={e => setSelectedSkill(e.target.value)}>
          {availableSkills.length > 0 ? (
            availableSkills.map(skill => (
              <option key={skill.id} value={skill.id}>{skill.nombre}</option>
            ))
          ) : (
            <option>No hay más habilidades para añadir</option>
          )}
        </select>
        <button onClick={handleAddSkill} disabled={loading || availableSkills.length === 0}>
          {loading ? 'Añadiendo...' : 'Añadir Habilidad'}
        </button>
      </div>

      {error && <p className="error-message">{error}</p>}

      {/* Lista de habilidades actuales del usuario */}
      <ul className="item-list">
        {userSkills.map(skill => (
          <li key={skill.id}>
            {skill.nombre}
            <button onClick={() => handleRemoveSkill(skill.id)} disabled={loading} className="delete-button">
              Eliminar
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
