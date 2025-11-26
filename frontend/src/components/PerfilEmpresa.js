import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaBuilding, FaPhone, FaMapMarkerAlt, FaGlobe, FaSave, FaEdit, FaBriefcase, FaTimes, FaCheck, FaUsers, FaEnvelope } from 'react-icons/fa';
import FormularioOferta from './FormularioOferta';
import './PerfilEmpresa.css';

const PerfilEmpresa = ({ token }) => {
    const navigate = useNavigate();
    const [empresa, setEmpresa] = useState(null);
    const [ofertas, setOfertas] = useState([]);
    const [loading, setLoading] = useState(true);
    const [isEditing, setIsEditing] = useState(false);
    const [message, setMessage] = useState('');
    const [showNewOfertaForm, setShowNewOfertaForm] = useState(false);
    const [formData, setFormData] = useState({
        nombre: '',
        descripcion: '',
        email_contacto: '',
        telefono: '',
        ubicacion: '',
        website: '',
        numero_empleados: ''
    });

    const apiUrl = process.env.REACT_APP_API_URL;

    // Cargar datos de la empresa y ofertas
    useEffect(() => {
        const fetchEmpresa = async () => {
            try {
                const res = await fetch(`${apiUrl}/empresas/me`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    setEmpresa(data);
                    setFormData({
                        nombre: data.nombre || '',
                        descripcion: data.descripcion || '',
                        email_contacto: data.email_contacto || '',
                        telefono: data.telefono || '',
                        ubicacion: data.ubicacion || '',
                        website: data.website || '',
                        numero_empleados: data.numero_empleados || ''
                    });
                }
            } catch (error) {
                setMessage('Error al cargar los datos de la empresa');
            } finally {
                setLoading(false);
            }
        };
        
        // Cargar ofertas de la empresa
        const fetchOfertas = async () => {
            try {
                const res = await fetch(`${apiUrl}/oportunidades/me`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    setOfertas(data);
                }
            } catch (error) {
                console.error('Error al cargar ofertas:', error);
            }
        };
        
        if (token) {
            fetchEmpresa();
            fetchOfertas();
        }
    }, [token, apiUrl]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    const handleSave = async () => {
        try {
            const res = await fetch(`${apiUrl}/empresas/me`, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(formData)
            });

            if (res.ok) {
                const data = await res.json();
                setEmpresa(data);
                setIsEditing(false);
                setMessage('✓ Perfil actualizado correctamente');
                setTimeout(() => setMessage(''), 3000);
            } else {
                setMessage('Error al actualizar el perfil');
            }
        } catch (error) {
            setMessage('Error de conexión');
        }
    };

    if (loading) return (
        <div className="empresa-loading">
            <p>Cargando perfil de empresa...</p>
        </div>
    );

    return (
        <div className="empresa-profile-container">
            {/* Mensaje de estado */}
            {message && (
                <div className={`empresa-message ${message.startsWith('✓') ? 'empresa-message-success' : 'empresa-message-error'}`}>
                    {message.startsWith('✓') ? <FaCheck /> : <FaTimes />}
                    {message}
                </div>
            )}

            {/* Header con información básica */}
            <div className="empresa-header-section">
                <div className="empresa-header-top">
                    <div className="empresa-info-header">
                        <div className="empresa-avatar">
                            <FaBuilding />
                        </div>
                        <div className="empresa-basic-info">
                            <h1>{empresa?.nombre || 'Tu Empresa'}</h1>
                            <p className="empresa-tagline">{empresa?.descripcion || 'Completa tu perfil para que los estudiantes te conozcan'}</p>
                        </div>
                    </div>
                    <button 
                        className={`empresa-edit-btn ${isEditing ? 'empresa-edit-btn-cancel' : 'empresa-edit-btn-primary'}`}
                        onClick={() => isEditing ? setIsEditing(false) : setIsEditing(true)}
                    >
                        {isEditing ? (
                            <>
                                <FaTimes /> Cancelar
                            </>
                        ) : (
                            <>
                                <FaEdit /> Editar Perfil
                            </>
                        )}
                    </button>
                </div>

                {/* Vista de edición o visualización */}
                {isEditing ? (
                    <div className="empresa-edit-section">
                        <div className="empresa-form-grid">
                            <div className="empresa-form-group">
                                <label>Nombre de la Empresa</label>
                                <input
                                    type="text"
                                    name="nombre"
                                    value={formData.nombre}
                                    onChange={handleInputChange}
                                    placeholder="Nombre de tu empresa"
                                />
                            </div>

                            <div className="empresa-form-group">
                                <label><FaUsers /> Número de Empleados</label>
                                <input
                                    type="text"
                                    name="numero_empleados"
                                    value={formData.numero_empleados}
                                    onChange={handleInputChange}
                                    placeholder="Ej: 50-100"
                                />
                            </div>

                            <div className="empresa-form-group empresa-form-full">
                                <label>Descripción de la Empresa</label>
                                <textarea
                                    name="descripcion"
                                    value={formData.descripcion}
                                    onChange={handleInputChange}
                                    placeholder="Cuéntanos sobre tu empresa, su misión, visión y valores..."
                                    rows="4"
                                />
                            </div>

                            <div className="empresa-form-group">
                                <label><FaPhone /> Teléfono</label>
                                <input
                                    type="tel"
                                    name="telefono"
                                    value={formData.telefono}
                                    onChange={handleInputChange}
                                    placeholder="+34 123 456 789"
                                />
                            </div>

                            <div className="empresa-form-group">
                                <label><FaMapMarkerAlt /> Ubicación</label>
                                <input
                                    type="text"
                                    name="ubicacion"
                                    value={formData.ubicacion}
                                    onChange={handleInputChange}
                                    placeholder="Ciudad, País"
                                />
                            </div>

                            <div className="empresa-form-group">
                                <label><FaGlobe /> Website</label>
                                <input
                                    type="url"
                                    name="website"
                                    value={formData.website}
                                    onChange={handleInputChange}
                                    placeholder="https://tuempresa.com"
                                />
                            </div>

                            <div className="empresa-form-group">
                                <label><FaEnvelope /> Email de Contacto</label>
                                <input
                                    type="email"
                                    name="email_contacto"
                                    value={formData.email_contacto}
                                    onChange={handleInputChange}
                                    placeholder="contacto@empresa.com"
                                />
                            </div>
                        </div>

                        <button className="empresa-save-btn" onClick={handleSave}>
                            <FaSave /> Guardar Cambios
                        </button>
                    </div>
                ) : (
                    <div className="empresa-info-display">
                        <div className="empresa-info-grid">
                            <div className="empresa-info-card">
                                <div className="empresa-info-icon"><FaBuilding /></div>
                                <div className="empresa-info-content">
                                    <span className="empresa-info-label">Empresa</span>
                                    <p>{empresa?.nombre || 'No especificado'}</p>
                                </div>
                            </div>

                            <div className="empresa-info-card">
                                <div className="empresa-info-icon"><FaUsers /></div>
                                <div className="empresa-info-content">
                                    <span className="empresa-info-label">Empleados</span>
                                    <p>{empresa?.numero_empleados || 'No especificado'}</p>
                                </div>
                            </div>

                            <div className="empresa-info-card">
                                <div className="empresa-info-icon"><FaMapMarkerAlt /></div>
                                <div className="empresa-info-content">
                                    <span className="empresa-info-label">Ubicación</span>
                                    <p>{empresa?.ubicacion || 'No especificada'}</p>
                                </div>
                            </div>

                            <div className="empresa-info-card">
                                <div className="empresa-info-icon"><FaPhone /></div>
                                <div className="empresa-info-content">
                                    <span className="empresa-info-label">Teléfono</span>
                                    <p>{empresa?.telefono || 'No especificado'}</p>
                                </div>
                            </div>

                            <div className="empresa-info-card">
                                <div className="empresa-info-icon"><FaEnvelope /></div>
                                <div className="empresa-info-content">
                                    <span className="empresa-info-label">Email</span>
                                    <p>{empresa?.email_contacto || 'No especificado'}</p>
                                </div>
                            </div>

                            <div className="empresa-info-card">
                                <div className="empresa-info-icon"><FaGlobe /></div>
                                <div className="empresa-info-content">
                                    <span className="empresa-info-label">Website</span>
                                    <p>
                                        {empresa?.website ? (
                                            <a href={empresa.website} target="_blank" rel="noopener noreferrer">
                                                {empresa.website}
                                            </a>
                                        ) : 'No especificado'}
                                    </p>
                                </div>
                            </div>
                        </div>

                        {empresa?.descripcion && (
                            <div className="empresa-description-display">
                                <h3>Acerca de nosotros</h3>
                                <p>{empresa.descripcion}</p>
                            </div>
                        )}
                    </div>
                )}
            </div>

            {/* Sección de Ofertas */}
            <div className="empresa-ofertas-section">
                <div className="empresa-ofertas-header">
                    <div>
                        <h2><FaBriefcase /> Mis Ofertas de Trabajo</h2>
                        <p className="empresa-ofertas-count">
                            {ofertas.length} oferta{ofertas.length !== 1 ? 's' : ''} publicada{ofertas.length !== 1 ? 's' : ''}
                        </p>
                    </div>
                    <div className="empresa-ofertas-actions">
                        <button 
                            className="empresa-new-oferta-btn"
                            onClick={() => setShowNewOfertaForm(!showNewOfertaForm)}
                        >
                            + Nueva Oferta
                        </button>
                        <button 
                            className="empresa-browse-students-btn"
                            onClick={() => navigate('/dashboard-empresa/estudiantes')}
                        >
                            <FaUsers /> Ver Estudiantes
                        </button>
                    </div>
                </div>

                {/* Lista de Ofertas */}
                {ofertas.length === 0 ? (
                    <div className="empresa-no-ofertas">
                        <FaBriefcase className="empresa-no-ofertas-icon" />
                        <p>Aún no has publicado ninguna oferta de trabajo.</p>
                        <p className="empresa-no-ofertas-sub">¡Crea tu primera oferta y encuentra los mejores estudiantes!</p>
                    </div>
                ) : (
                    <div className="empresa-ofertas-grid">
                        {ofertas.map(oferta => (
                            <div key={oferta.id} className="empresa-oferta-card">
                                <div className="empresa-oferta-header">
                                    <h4>{oferta.titulo}</h4>
                                    <span className={`empresa-oferta-status ${oferta.activa ? 'empresa-oferta-active' : 'empresa-oferta-inactive'}`}>
                                        {oferta.activa ? '● Activa' : '● Inactiva'}
                                    </span>
                                </div>

                                <div className="empresa-oferta-meta">
                                    <div className="empresa-oferta-meta-item">
                                        <span className="empresa-oferta-label">Tipo:</span>
                                        <span className="empresa-oferta-value">{oferta.tipo}</span>
                                    </div>
                                    <div className="empresa-oferta-meta-item">
                                        <span className="empresa-oferta-label">Modalidad:</span>
                                        <span className="empresa-oferta-value">{oferta.modalidad}</span>
                                    </div>
                                    <div className="empresa-oferta-meta-item">
                                        <span className="empresa-oferta-label">Ubicación:</span>
                                        <span className="empresa-oferta-value">{oferta.ubicacion}</span>
                                    </div>
                                </div>

                                {oferta.habilidades_requeridas && oferta.habilidades_requeridas.length > 0 && (
                                    <div className="empresa-oferta-skills">
                                        <span className="empresa-oferta-label">Habilidades requeridas:</span>
                                        <div className="empresa-skills-tags">
                                            {oferta.habilidades_requeridas.map(h => (
                                                <span key={h} className="empresa-skill-tag">{h}</span>
                                            ))}
                                        </div>
                                    </div>
                                )}

                                {oferta.salario && (
                                    <div className="empresa-oferta-salary">
                                        <span className="empresa-oferta-label">Salario:</span>
                                        <span className="empresa-oferta-value empresa-salary-amount">${oferta.salario.toLocaleString()}</span>
                                    </div>
                                )}
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {/* Formulario para Nueva Oferta */}
            {showNewOfertaForm && (
                <div className="empresa-new-oferta-section">
                    <div className="empresa-form-header">
                        <h2>Crear Nueva Oferta de Trabajo</h2>
                        <button 
                            className="empresa-close-form-btn"
                            onClick={() => setShowNewOfertaForm(false)}
                        >
                            <FaTimes />
                        </button>
                    </div>
                    <FormularioOferta token={token} />
                </div>
            )}
        </div>
    );
};

export default PerfilEmpresa;
