import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaPlus, FaEdit, FaTrash } from 'react-icons/fa';

const GestionOfertas = ({ token }) => {
  const [ofertas, setOfertas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const fetchOfertas = async () => {
      try {
        const res = await fetch(`${process.env.REACT_APP_API_URL}/oportunidades/me`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          const data = await res.json();
          setOfertas(data);
        } else {
          setError('No se pudieron cargar tus ofertas.');
        }
      } catch (err) {
        setError('Error de conexión al cargar las ofertas.');
      } finally {
        setLoading(false);
      }
    };

    if (token) {
      fetchOfertas();
    }
  }, [token]);

  const handleDelete = async (id) => {
    if (window.confirm('¿Estás seguro de que quieres eliminar esta oferta?')) {
      try {
        const res = await fetch(`${process.env.REACT_APP_API_URL}/oportunidades/${id}`, {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) {
          setOfertas(ofertas.filter(o => o.id !== id));
        } else {
          alert('No se pudo eliminar la oferta.');
        }
      } catch (err) {
        alert('Error de conexión al eliminar la oferta.');
      }
    }
  };

  if (loading) return <p>Cargando ofertas...</p>;
  if (error) return <p className="message message-error">{error}</p>;

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h3>Mis Ofertas de Trabajo</h3>
        <Link to="/dashboard-empresa/ofertas/nueva" className="btn btn-primary">
          <FaPlus /> Crear Nueva Oferta
        </Link>
      </div>
      <hr />
      {ofertas.length === 0 ? (
        <p>Aún no has publicado ninguna oferta. ¡Crea la primera!</p>
      ) : (
        <ul className="item-list">
          {ofertas.map(oferta => (
            <li key={oferta.id} className="list-item">
              <div>
                <strong>{oferta.titulo}</strong>
                <span className={`status-badge ${oferta.activa ? 'status-active' : 'status-inactive'}`}>
                  {oferta.activa ? 'Activa' : 'Inactiva'}
                </span>
              </div>
              <div className="item-actions">
                <button onClick={() => navigate(`/dashboard-empresa/ofertas/editar/${oferta.id}`)} className="btn-icon">
                  <FaEdit />
                </button>
                <button onClick={() => handleDelete(oferta.id)} className="btn-icon btn-danger">
                  <FaTrash />
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default GestionOfertas;
