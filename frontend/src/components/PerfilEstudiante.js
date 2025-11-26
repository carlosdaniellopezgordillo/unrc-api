import React, { useState, useEffect } from 'react';
import { FaFileAlt, FaBriefcase, FaCode, FaGraduationCap, FaSave, FaEdit, FaTimes, FaCheck, FaStar, FaDownload, FaShare } from 'react-icons/fa';
import TagInput from './TagInput';
import VacancyCard from './VacancyCard';
import Badge from './Badge';
import './PerfilEstudiante.css';

function PerfilEstudiante({ estudianteId }) {
  const [loading, setLoading] = useState(true);
  const [cvFile, setCvFile] = useState(null);
  const [cvPath, setCvPath] = useState(null);
  const [skills, setSkills] = useState([]);
  const [softSkills, setSoftSkills] = useState([]);
  const [projects, setProjects] = useState([]);
  const [experiences, setExperiences] = useState([]);
  const [carrera, setCarrera] = useState('');
  const [message, setMessage] = useState("");
  const [messageType, setMessageType] = useState(""); // 'success' o 'error'
  const [recomendadas, setRecomendadas] = useState([]);
  const [cvExtracted, setCvExtracted] = useState(null);
  const [token, setToken] = useState(null);
  const [isEditing, setIsEditing] = useState(false);
  const [studentData, setStudentData] = useState({
    nombre: '',
    email: '',
    matricula: '',
    semestre: '',
    gpa: '',
    carrera: ''
  });

  useEffect(() => {
    const storedToken = localStorage.getItem('token');
    setToken(storedToken);
  }, []);

  useEffect(() => {
    if (!token) return;
    
    const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    fetch(`${apiUrl}/estudiantes/me/profile`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(res => {
        if (!res.ok) throw new Error('No se pudo cargar el perfil');
        return res.json();
      })
      .then(data => {
        // Obtener el nombre del usuario desde localStorage si está disponible
        const storedUser = localStorage.getItem('user');
        const userName = storedUser ? JSON.parse(storedUser).nombre : '';
        
        setStudentData({
          nombre: userName || data.nombre || '',
          email: data.email || '',
          matricula: data.matricula || '',
          semestre: data.semestre || '',
          gpa: data.gpa || '',
          carrera: data.carrera || ''
        });
        setSkills(data.habilidades_tecnicas || []);
        setSoftSkills(data.habilidades_blandas || []);
        setProjects(data.proyectos || []);
        setExperiences(data.experiencias || []);
        setCarrera(data.carrera || '');
        setCvPath(data.cv_path || null);
      })
      .catch(err => {
        console.error(err);
        showMessage('Error al cargar el perfil', 'error');
      })
      .finally(() => setLoading(false));
  }, [token]);

  useEffect(() => {
    if (!estudianteId || !token) return;
    const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    fetch(`${apiUrl}/oportunidades/recomendadas/${estudianteId}`, {
      headers: { 'Authorization': `Bearer ${token}` }
    })
      .then(r => r.json())
      .then(data => setRecomendadas(data || []))
      .catch(() => setRecomendadas([]));
  }, [estudianteId, token]);

  const showMessage = (text, type = 'success') => {
    setMessage(text);
    setMessageType(type);
    setTimeout(() => setMessage(''), 4000);
  };

  const handleCvChange = (e) => setCvFile(e.target.files[0]);

  const handleCvUpload = async (e) => {
    e.preventDefault();
    if (!cvFile) return showMessage('Selecciona un archivo', 'error');
    if (!token) return showMessage('No estás autenticado', 'error');
    
    try {
      const formData = new FormData();
      formData.append('file', cvFile);
      
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/estudiantes/me/upload_cv`, { 
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData 
      });
      
      if (!res.ok) {
        const errorData = await res.json();
        showMessage(errorData.detail || `Error: ${res.status}`, 'error');
        return;
      }
      
      const data = await res.json();
      showMessage('CV subido correctamente', 'success');
      setCvPath(data.cv_path);
      setCvExtracted(data.parsed || null);
      setCvFile(null);
      
      if (data.parsed) {
        if (data.parsed.habilidades && data.parsed.habilidades.length > 0) {
          const nuevasHabilidades = [...new Set([
            ...skills.map(s => s.toLowerCase()),
            ...data.parsed.habilidades.map(h => h.toLowerCase())
          ])].map(h => {
            return skills.find(s => s.toLowerCase() === h) || data.parsed.habilidades.find(x => x.toLowerCase() === h) || h;
          });
          setSkills(nuevasHabilidades);
        }
        if (data.parsed.carrera) {
          setCarrera(data.parsed.carrera);
        }
        if (data.parsed.proyectos && data.parsed.proyectos.length > 0) {
          const nuevosProyectos = [...new Set([...projects, ...data.parsed.proyectos])];
          setProjects(nuevosProyectos);
        }
        if (data.parsed.experiencias && data.parsed.experiencias.length > 0) {
          const nuevasExperiencias = [...new Set([...experiences, ...data.parsed.experiencias])];
          setExperiences(nuevasExperiencias);
        }
      }
    } catch (error) {
      console.error('Error al subir CV:', error);
      showMessage(`Error de conexión: ${error.message}`, 'error');
    }
  };

  const handlePerfilUpdate = async (e) => {
    e.preventDefault();
    if (!token) return showMessage('No estás autenticado', 'error');
    
    try {
      const formData = new FormData();
      formData.append('carrera', studentData.carrera || '');
      formData.append('semestre', studentData.semestre || '');
      formData.append('habilidades_tecnicas', JSON.stringify(Array.isArray(skills) ? skills : []));
      formData.append('habilidades_blandas', JSON.stringify(Array.isArray(softSkills) ? softSkills : []));
      formData.append('proyectos', JSON.stringify(Array.isArray(projects) ? projects.filter(p => p && p.trim()) : []));
      
      // Serializar experiencias correctamente
      let experienciasSerializadas = [];
      if (Array.isArray(experiences)) {
        experienciasSerializadas = experiences.map(exp => {
          if (typeof exp === 'string') {
            return { puesto: exp.trim(), empresa: '', descripcion: exp.trim() };
          }
          return {
            puesto: (exp.puesto || '').toString().trim(),
            empresa: (exp.empresa || '').toString().trim(),
            descripcion: (exp.descripcion || '').toString().trim()
          };
        }).filter(exp => exp.puesto || exp.descripcion);
      }
      formData.append('experiencias', JSON.stringify(experienciasSerializadas));
      
      const apiUrl = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      const res = await fetch(`${apiUrl}/estudiantes/me/perfil`, { 
        method: 'PATCH',
        headers: { 'Authorization': `Bearer ${token}` },
        body: formData 
      });
      
      if (!res.ok) {
        const errorData = await res.json();
        showMessage(errorData.detail || `Error: ${res.status}`, 'error');
        console.error('Error al actualizar perfil:', errorData);
        return;
      }
      
      const data = await res.json();
      showMessage('Perfil actualizado correctamente', 'success');
      setIsEditing(false);
      console.log('Perfil actualizado:', data);
    } catch (error) {
      console.error('Error al guardar perfil:', error);
      showMessage(`Error de conexión: ${error.message}`, 'error');
    }
  };

  const calculateCompletion = () => {
    let total = 5;
    let score = 0;
    if (cvPath) score += 1;
    if (skills && skills.length > 0) score += 1;
    if (softSkills && softSkills.length > 0) score += 1;
    if (projects && projects.length > 0) score += 1;
    if (experiences && experiences.length > 0) score += 1;
    return Math.round((score / total) * 100);
  };

  const handleShareProfile = () => {
    const apiBase = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    const url = `${apiBase}/estudiantes/${estudianteId}/public`;
    navigator.clipboard?.writeText(url);
    showMessage('Enlace copiado al portapapeles', 'success');
    window.open(url, '_blank');
  };

  const getCompletionBadge = () => {
    const pct = calculateCompletion();
    if (pct >= 90) return { level: 'gold', label: 'Perfil Elite' };
    if (pct >= 70) return { level: 'silver', label: 'Perfil Avanzado' };
    if (pct >= 40) return { level: 'bronze', label: 'En Desarrollo' };
    return { level: 'starter', label: 'Comienza' };
  };

  const getGPAColor = (gpa) => {
    if (gpa >= 3.8) return '#10b981';
    if (gpa >= 3.5) return '#3b82f6';
    if (gpa >= 3.0) return '#f59e0b';
    return '#ef4444';
  };

  if (loading) return (
    <div className="estudiante-profile-container">
      <div className="estudiante-loading">Cargando perfil...</div>
    </div>
  );

  if (!estudianteId) return (
    <div className="estudiante-profile-container">
      <div className="estudiante-loading">No estás autenticado.</div>
    </div>
  );

  const badge = getCompletionBadge();
  const completion = calculateCompletion();

  return (
    <div className="estudiante-profile-container">
      {/* Mensaje flotante */}
      {message && (
        <div className={`estudiante-message ${messageType === 'success' ? 'estudiante-message-success' : 'estudiante-message-error'}`}>
          <span>{message}</span>
        </div>
      )}

      {/* Header Section */}
      <div className="estudiante-header-section">
        <div className="estudiante-header-top">
          <div className="estudiante-info-header">
            <div className="estudiante-avatar" style={{ backgroundColor: getGPAColor(studentData.gpa) }}>
              {studentData.nombre.split(' ').map(n => n[0]).join('').toUpperCase()}
            </div>
            <div className="estudiante-basic-info">
              <h1>{studentData.nombre || 'Mi Perfil'}</h1>
              <p className="estudiante-email">{studentData.email}</p>
              <p className="estudiante-carrera">{studentData.carrera}</p>
            </div>
          </div>
          <div className="estudiante-header-actions">
            <button className="estudiante-share-btn" onClick={handleShareProfile}>
              <FaShare /> Compartir
            </button>
            <button 
              className="estudiante-edit-btn"
              onClick={() => setIsEditing(!isEditing)}
            >
              {isEditing ? <><FaTimes /> Cancelar</> : <><FaEdit /> Editar</>}
            </button>
          </div>
        </div>

        {/* Academic Info Cards */}
        <div className="estudiante-header-body">
          {isEditing ? (
            <div className="estudiante-edit-info-form">
              <div className="form-group">
                <label>Carrera</label>
                <input 
                  type="text" 
                  value={studentData.carrera}
                  onChange={(e) => setStudentData({...studentData, carrera: e.target.value})}
                  placeholder="Ingresa tu carrera"
                />
              </div>
              <div className="form-group">
                <label>Semestre</label>
                <select 
                  value={studentData.semestre}
                  onChange={(e) => setStudentData({...studentData, semestre: e.target.value})}
                >
                  <option value="">Selecciona tu semestre</option>
                  {[1,2,3,4,5,6,7,8,9,10].map(s => (
                    <option key={s} value={s}>{s}</option>
                  ))}
                </select>
              </div>
            </div>
          ) : (
            <div className="estudiante-info-cards">
              <div className="estudiante-info-card">
                <div className="estudiante-info-icon"><FaGraduationCap /></div>
                <div className="estudiante-info-content">
                  <span className="estudiante-info-label">Matrícula</span>
                  <p>{studentData.matricula || 'N/A'}</p>
                </div>
              </div>

              <div className="estudiante-info-card">
                <div className="estudiante-info-icon"><FaStar /></div>
                <div className="estudiante-info-content">
                  <span className="estudiante-info-label">GPA</span>
                  <p style={{ color: getGPAColor(studentData.gpa) }}>
                    {studentData.gpa ? parseFloat(studentData.gpa).toFixed(2) : 'N/A'}
                  </p>
                </div>
              </div>

              <div className="estudiante-info-card">
                <div className="estudiante-info-icon"><FaBriefcase /></div>
                <div className="estudiante-info-content">
                  <span className="estudiante-info-label">Semestre</span>
                  <p>{studentData.semestre || 'N/A'}</p>
                </div>
              </div>

              <div className="estudiante-info-card">
                <div className="estudiante-info-icon"><FaCheck /></div>
                <div className="estudiante-info-content">
                  <span className="estudiante-info-label">Completitud</span>
                  <p>{completion}%</p>
                </div>
              </div>
            </div>
          )}

          {/* Completion Bar */}
          <div className="estudiante-completion-section">
            <div className="estudiante-completion-header">
              <h3>Progreso del Perfil</h3>
              <Badge level={badge.level} label={badge.label} />
            </div>
            <div className="estudiante-completion-bar-container">
              <div className="estudiante-completion-bar">
                <div 
                  className="estudiante-completion-fill" 
                  style={{ width: `${completion}%` }}
                />
              </div>
              <div className="estudiante-completion-text">{completion}% completado</div>
            </div>
            <div className="estudiante-completion-checklist">
              <div className={`checklist-item ${cvPath ? 'completed' : ''}`}>
                <FaCheck style={{ opacity: cvPath ? 1 : 0.3 }} /> CV Subido
              </div>
              <div className={`checklist-item ${skills.length > 0 ? 'completed' : ''}`}>
                <FaCheck style={{ opacity: skills.length > 0 ? 1 : 0.3 }} /> Habilidades Técnicas
              </div>
              <div className={`checklist-item ${softSkills.length > 0 ? 'completed' : ''}`}>
                <FaCheck style={{ opacity: softSkills.length > 0 ? 1 : 0.3 }} /> Habilidades Blandas
              </div>
              <div className={`checklist-item ${projects.length > 0 ? 'completed' : ''}`}>
                <FaCheck style={{ opacity: projects.length > 0 ? 1 : 0.3 }} /> Proyectos
              </div>
              <div className={`checklist-item ${experiences.length > 0 ? 'completed' : ''}`}>
                <FaCheck style={{ opacity: experiences.length > 0 ? 1 : 0.3 }} /> Experiencias
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* CV Section */}
      <div className="estudiante-section estudiante-cv-section">
        <div className="estudiante-section-header">
          <h2><FaFileAlt /> Currículum Vitae</h2>
          <p>Sube tu CV para que las empresas puedan conocer tu perfil</p>
        </div>

        {cvPath && (
          <div className="cv-uploaded">
            <div className="cv-info">
              <FaCheck style={{ color: '#10b981' }} />
              <div>
                <p>CV cargado correctamente</p>
                <small>Disponible para descargar</small>
              </div>
            </div>
            <a 
              href={`http://localhost:8000/estudiantes/${estudianteId}/cv/download`} 
              target="_blank" 
              rel="noreferrer"
              className="cv-download-btn"
            >
              <FaDownload /> Descargar
            </a>
          </div>
        )}

        <form onSubmit={handleCvUpload} className="cv-upload-form">
          <div className="cv-file-input">
            <input 
              type="file" 
              id="cv-file"
              accept=".pdf,.doc,.docx" 
              onChange={handleCvChange}
            />
            <label htmlFor="cv-file">
              {cvFile ? `Seleccionado: ${cvFile.name}` : 'Arrastra tu CV aquí o haz clic para seleccionar'}
            </label>
          </div>
          <button 
            type="submit"
            disabled={!cvFile}
            className="cv-upload-btn"
          >
            <FaFileAlt /> {cvFile ? 'Subir CV' : 'Selecciona un archivo'}
          </button>
        </form>
      </div>

      {/* CV Extracted Info */}
      {cvExtracted && (
        <div className="estudiante-section">
          <div className="estudiante-section-header">
            <h2><FaFileAlt /> Información Extraída del CV</h2>
            <p>Datos detectados automáticamente - puedes editarlos abajo</p>
          </div>
          
          <div className="extracted-cards-grid">
            {cvExtracted.carrera && (
              <div className="extracted-card">
                <FaGraduationCap className="extracted-icon" />
                <h4>Carrera</h4>
                <p>{cvExtracted.carrera}</p>
              </div>
            )}
            
            {cvExtracted.habilidades && cvExtracted.habilidades.length > 0 && (
              <div className="extracted-card">
                <FaCode className="extracted-icon" />
                <h4>Skills Detectados</h4>
                <div className="extracted-skills">
                  {cvExtracted.habilidades.slice(0, 3).map((h, idx) => (
                    <span key={idx}>{h}</span>
                  ))}
                  {cvExtracted.habilidades.length > 3 && (
                    <span className="more">+{cvExtracted.habilidades.length - 3}</span>
                  )}
                </div>
              </div>
            )}
            
            {cvExtracted.experiencias && cvExtracted.experiencias.length > 0 && (
              <div className="extracted-card">
                <FaBriefcase className="extracted-icon" />
                <h4>Experiencias</h4>
                <p>{cvExtracted.experiencias.length} encontrada{cvExtracted.experiencias.length !== 1 ? 's' : ''}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Skills Section */}
      <div className="estudiante-section">
        <div className="estudiante-section-header">
          <h2><FaCode /> Habilidades Técnicas</h2>
          <p>Agrega las tecnologías y lenguajes que dominas</p>
        </div>
        {isEditing ? (
          <TagInput
            tags={skills}
            setTags={setSkills}
            placeholder="Escribe una habilidad y presiona Enter"
          />
        ) : (
          <div className="skills-display">
            {skills.length > 0 ? (
              <div className="skills-tags">
                {skills.map((skill, idx) => (
                  <span key={idx} className="skill-tag">{skill}</span>
                ))}
              </div>
            ) : (
              <p className="no-data">No has agregado habilidades técnicas aún</p>
            )}
          </div>
        )}
      </div>

      {/* Soft Skills Section */}
      <div className="estudiante-section">
        <div className="estudiante-section-header">
          <h2>💬 Habilidades Blandas</h2>
          <p>Comunicación, liderazgo, trabajo en equipo, etc.</p>
        </div>
        {isEditing ? (
          <TagInput
            tags={softSkills}
            setTags={setSoftSkills}
            placeholder="Ej: Comunicación, Liderazgo, Resolución de problemas"
          />
        ) : (
          <div className="skills-display">
            {softSkills.length > 0 ? (
              <div className="skills-tags">
                {softSkills.map((skill, idx) => (
                  <span key={idx} className="soft-skill-tag">{skill}</span>
                ))}
              </div>
            ) : (
              <p className="no-data">No has agregado habilidades blandas aún</p>
            )}
          </div>
        )}
      </div>

      {/* Projects Section */}
      <div className="estudiante-section">
        <div className="estudiante-section-header">
          <h2>📁 Proyectos</h2>
          <p>Comparte los proyectos en los que has trabajado</p>
        </div>
        {isEditing ? (
          <textarea 
            value={projects.join('\n')} 
            onChange={e => setProjects(e.target.value.split('\n').filter(p => p.trim()))} 
            rows={4}
            className="estudiante-textarea"
            placeholder="Nombre del proyecto&#10;Otro proyecto&#10;Otro más..."
          />
        ) : (
          <div className="projects-display">
            {projects.length > 0 ? (
              <ul className="projects-list">
                {projects.map((project, idx) => (
                  project.trim() && (
                    <li key={idx}>
                      <span className="project-dot">→</span> {project}
                    </li>
                  )
                ))}
              </ul>
            ) : (
              <p className="no-data">No has agregado proyectos aún</p>
            )}
          </div>
        )}
      </div>

      {/* Experiences Section */}
      <div className="estudiante-section">
        <div className="estudiante-section-header">
          <h2><FaBriefcase /> Experiencias</h2>
          <p>Tus experiencias laborales previas</p>
        </div>
        {isEditing ? (
          <textarea 
            value={experiences.map(x => `${x.puesto || ''} @ ${x.empresa || ''}`).join('\n')} 
            onChange={e => setExperiences(e.target.value.split('\n').filter(x => x.trim()).map(line => {
              const parts = line.split('@');
              return { puesto: (parts[0] || '').trim(), empresa: (parts[1] || '').trim() };
            }))} 
            rows={4}
            className="estudiante-textarea"
            placeholder="Puesto @ Empresa&#10;Otro Puesto @ Otra Empresa"
          />
        ) : (
          <div className="experiences-display">
            {experiences.length > 0 ? (
              <ul className="experiences-list">
                {experiences.map((exp, idx) => (
                  (exp.puesto || exp.empresa) && (
                    <li key={idx}>
                      <div className="exp-icon"><FaBriefcase /></div>
                      <div className="exp-content">
                        <p className="exp-puesto">{exp.puesto || 'Sin especificar'}</p>
                        <p className="exp-empresa">{exp.empresa || 'Sin empresa'}</p>
                      </div>
                    </li>
                  )
                ))}
              </ul>
            ) : (
              <p className="no-data">No has agregado experiencias aún</p>
            )}
          </div>
        )}
      </div>

      {/* Recommended Vacancies */}
      {recomendadas && recomendadas.length > 0 && (
        <div className="estudiante-section">
          <div className="estudiante-section-header">
            <h2><FaBriefcase /> Vacantes Recomendadas</h2>
            <p>Basado en tu perfil y habilidades</p>
          </div>
          <div className="recomendadas-grid">
            {recomendadas.slice(0, 3).map(r => (
              <VacancyCard key={r.oportunidad.id} vac={r.oportunidad} score={r.score} />
            ))}
          </div>
        </div>
      )}

      {/* Save Button */}
      {isEditing && (
        <div className="estudiante-actions">
          <button 
            onClick={handlePerfilUpdate}
            className="estudiante-save-btn"
          >
            <FaSave /> Guardar Cambios
          </button>
          <button 
            onClick={() => setIsEditing(false)}
            className="estudiante-cancel-btn"
          >
            <FaTimes /> Cancelar
          </button>
        </div>
      )}
    </div>
  );
}

export default PerfilEstudiante;
