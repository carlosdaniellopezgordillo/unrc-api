import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom'; // Importar Link para la navegación

export default function Usuarios() {
  const [usuarios, setUsuarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    async function fetchUsuarios() {
      setLoading(true);
      setError('');
      try {
        const res = await fetch(`${process.env.REACT_APP_API_URL}/auth/usuarios/estudiantes`);
        if (res.ok) {
          const data = await res.json();
          setUsuarios(data);
        } else {
          setError('No se pudo obtener la lista de usuarios.');
        }
      } catch (err) {
        setError('Error de conexión con la API.');
      }
      setLoading(false);
    }
    fetchUsuarios();
  }, []);

  return (
    <div>
      <h2>Estudiantes Registrados</h2>
      
      {loading && <p>Cargando...</p>}
      {error && (
        <div style={{ color: '#9F2241', textAlign: 'center' }}>
          <p>{error}</p>
          <Link to="/" className="btn" style={{ textDecoration: 'none', display: 'inline-block', marginTop: '1rem', width: 'auto' }}>
            Volver al inicio
          </Link>
        </div>
      )}
      
      {!loading && !error && (
        <div>
          {usuarios.map((u, i) => (
            <div className="user-card" key={i}>
              <p><strong>Nombre:</strong> {u.nombre}</p>
              <p><strong>Email:</strong> {u.email}</p>
              <p><strong>Tipo:</strong> {u.tipo}</p>
            </div>
          ))}
          <Link to="/" className="btn" style={{ textDecoration: 'none', display: 'block', marginTop: '2rem' }}>
            Volver al inicio
          </Link>
        </div>
      )}
    </div>
  );
}
