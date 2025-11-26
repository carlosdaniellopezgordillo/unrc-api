import React from 'react';
import { Routes, Route, NavLink, Outlet } from 'react-router-dom';
import { FaUser, FaBriefcase, FaGraduationCap } from 'react-icons/fa';
import PerfilEmpresa from './PerfilEmpresa';
import GestionOfertas from './GestionOfertas';
import FormularioOferta from './FormularioOferta';
import GestionEstudiantes from './GestionEstudiantes';

const DashboardEmpresa = ({ token }) => {
  return (
    <div className="dashboard-container">
      <aside className="dashboard-sidebar">
        <nav>
          <NavLink to="perfil" className="sidebar-link">
            <FaUser /> Mi Perfil
          </NavLink>
          <NavLink to="ofertas" className="sidebar-link">
            <FaBriefcase /> Gestionar Ofertas
          </NavLink>
          <NavLink to="estudiantes" className="sidebar-link">
            <FaGraduationCap /> Explorar Talento
          </NavLink>
          {/* Agrega más enlaces aquí a medida que crezca */}
        </nav>
      </aside>
      <main className="dashboard-content">
        <Routes>
          <Route index element={<PerfilEmpresa token={token} />} />
          <Route path="perfil" element={<PerfilEmpresa token={token} />} />
          <Route path="ofertas" element={<GestionOfertas token={token} />} />
          <Route path="ofertas/nueva" element={<FormularioOferta token={token} />} />
          <Route path="ofertas/editar/:ofertaId" element={<FormularioOferta token={token} />} />
          <Route path="estudiantes" element={<GestionEstudiantes token={token} />} />
        </Routes>
        <Outlet />
      </main>
    </div>
  );
};

export default DashboardEmpresa;
