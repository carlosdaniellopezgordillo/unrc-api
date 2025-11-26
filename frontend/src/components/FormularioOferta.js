import React, { useState, useEffect } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import TagInput from './TagInput';

const FormularioOferta = ({ token }) => {
  const [oferta, setOferta] = useState({
    titulo: '',
    descripcion: '',
    tipo: 'empleo',
    habilidades_requeridas: [],
    semestre_minimo: 1,
    ubicacion: '',
    modalidad: 'presencial',
    salario: '',
    activa: true,
    gpa_minimo: '',
    duracion_meses: '',
    fecha_cierre: '',
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const navigate = useNavigate();
  const { ofertaId } = useParams();
  const isEditing = Boolean(ofertaId);

  useEffect(() => {
    if (isEditing) {
      const fetchOferta = async () => {
        setLoading(true);
        try {
          const res = await fetch(`${process.env.REACT_APP_API_URL}/oportunidades/${ofertaId}`, {
            headers: { 'Authorization': `Bearer ${token}` }
          });
          if (res.ok) {
            const data = await res.json();
            setOferta({
              titulo: data.titulo || '',
              descripcion: data.descripcion || '',
              tipo: data.tipo || 'empleo',
              habilidades_requeridas: Array.isArray(data.habilidades_requeridas) ? data.habilidades_requeridas : [],
              semestre_minimo: data.semestre_minimo || 1,
              ubicacion: data.ubicacion || '',
              modalidad: data.modalidad || 'presencial',
              salario: data.salario || '',
              activa: data.activa !== undefined ? data.activa : true,
              gpa_minimo: data.gpa_minimo || '',
              duracion_meses: data.duracion_meses || '',
              fecha_cierre: data.fecha_cierre || '',
            });
          } else {
            setMessage('No se pudo cargar la oferta para editar.');
          }
        } catch (err) {
          setMessage('Error de conexión.');
        } finally {
          setLoading(false);
        }
      };
      fetchOferta();
    }
  }, [isEditing, ofertaId, token]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setOferta(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    // Asegurar que habilidades_requeridas sea siempre un array
    let habilidades = oferta.habilidades_requeridas;
    if (typeof habilidades === 'string') {
      habilidades = habilidades.split(',').map(h => h.trim()).filter(h => h);
    } else if (!Array.isArray(habilidades)) {
      habilidades = [];
    }

    const payload = {
      titulo: oferta.titulo,
      descripcion: oferta.descripcion,
      tipo: oferta.tipo,
      habilidades_requeridas: habilidades,
      semestre_minimo: parseInt(oferta.semestre_minimo),
      ubicacion: oferta.ubicacion,
      modalidad: oferta.modalidad,
      activa: oferta.activa,
      salario: oferta.salario && oferta.salario.toString().trim() ? parseFloat(oferta.salario) : null,
      gpa_minimo: oferta.gpa_minimo && oferta.gpa_minimo.toString().trim() ? parseFloat(oferta.gpa_minimo) : null,
      duracion_meses: oferta.duracion_meses && oferta.duracion_meses.toString().trim() ? parseInt(oferta.duracion_meses) : null,
      fecha_cierre: oferta.fecha_cierre && oferta.fecha_cierre.toString().trim() ? oferta.fecha_cierre : null
    };

    const url = isEditing
      ? `${process.env.REACT_APP_API_URL}/oportunidades/${ofertaId}`
      : `${process.env.REACT_APP_API_URL}/oportunidades/`;
    
    const method = isEditing ? 'PATCH' : 'POST';

    try {
      const res = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        setMessage(`¡Oferta ${isEditing ? 'actualizada' : 'creada'} con éxito!`);
        setTimeout(() => navigate('/dashboard-empresa/ofertas'), 2000);
      } else {
        const err = await res.json();
        setMessage('Error: ' + (err.detail || 'No se pudo guardar la oferta.'));
      }
    } catch (err) {
      setMessage('Error de conexión.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>{isEditing ? 'Editar Oferta' : 'Crear Nueva Oferta'}</h3>
      <form onSubmit={handleSubmit} className="form-container" style={{maxWidth: '700px', margin: 'auto'}}>
        <div className="form-group">
          <label>Título</label>
          <input type="text" name="titulo" value={oferta.titulo} onChange={handleChange} required />
        </div>
        <div className="form-group">
          <label>Descripción</label>
          <textarea name="descripcion" value={oferta.descripcion} onChange={handleChange} required rows="4"></textarea>
        </div>
        <div className="form-group">
          <label>Habilidades Requeridas</label>
          {/* TagInput es un componente más amigable para ingresar skills */}
          <TagInput
            tags={oferta.habilidades_requeridas}
            setTags={(tags) => setOferta(prev => ({ ...prev, habilidades_requeridas: tags }))}
            placeholder="Agregar habilidad y presionar Enter"
          />
        </div>
        <div style={{display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem'}}>
          <div className="form-group">
            <label>Tipo</label>
            <select name="tipo" value={oferta.tipo} onChange={handleChange}>
              <option value="empleo">Empleo</option>
              <option value="practica">Práctica</option>
              <option value="servicio_social">Servicio Social</option>
            </select>
          </div>
          <div className="form-group">
            <label>Modalidad</label>
            <select name="modalidad" value={oferta.modalidad} onChange={handleChange}>
              <option value="presencial">Presencial</option>
              <option value="remoto">Remoto</option>
              <option value="hibrido">Híbrido</option>
            </select>
          </div>
          <div className="form-group">
            <label>Ubicación</label>
            <input type="text" name="ubicacion" value={oferta.ubicacion} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Salario (opcional)</label>
            <input type="number" name="salario" value={oferta.salario} onChange={handleChange} placeholder="Ej: 15000" />
          </div>
          <div className="form-group">
            <label>Semestre Mínimo</label>
            <input type="number" name="semestre_minimo" value={oferta.semestre_minimo} onChange={handleChange} min="1" max="10" />
          </div>
        </div>
        <div className="form-group">
          <label style={{display: 'flex', alignItems: 'center'}}>
            <input type="checkbox" name="activa" checked={oferta.activa} onChange={handleChange} style={{width: 'auto', marginRight: '10px'}} />
            Oferta Activa
          </label>
        </div>
        <button type="submit" className="btn btn-primary" disabled={loading}>
          {loading ? 'Guardando...' : (isEditing ? 'Actualizar Oferta' : 'Crear Oferta')}
        </button>
      </form>
      {message && <div className={`message ${message.includes('éxito') ? 'message-success' : 'message-error'}`}>{message}</div>}
    </div>
  );
};

export default FormularioOferta;
