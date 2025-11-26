import React, { useState, useRef, useEffect } from 'react';

function TagInput({ tags, setTags, placeholder = 'Agregar y presiona Enter...', suggestions = [] }) {
  // Asegurar que tags siempre sea un array
  const validTags = Array.isArray(tags) ? tags : (tags ? [tags] : []);
  
  const [input, setInput] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filtered, setFiltered] = useState([]);
  const [allSuggestions, setAllSuggestions] = useState(suggestions || []);
  const inputRef = useRef(null);

  // Si no recibimos sugerencias por prop, intentamos obtenerlas del backend
  useEffect(() => {
    if (allSuggestions.length === 0) {
      const apiBase = process.env.REACT_APP_API_URL || 'http://localhost:8000';
      fetch(`${apiBase}/habilidades/`).then(r => r.json()).then(data => {
        // data es una lista de objetos {id, nombre}
        const names = Array.isArray(data) ? data.map(x => x.nombre || x.name || x) : [];
        setAllSuggestions(names);
      }).catch(() => {
        // silencioso: si falla, dejamos vacío
      });
    }
  }, [allSuggestions.length]);

  // Fallback si no hay sugerencias del backend ni por prop
  useEffect(() => {
    const defaultSuggestions = [
      'Python','JavaScript','React','Node.js','Django','SQL','PostgreSQL','AWS','Docker','Kubernetes','TensorFlow','pandas','Comunicación','Trabajo en equipo','Liderazgo'
    ];
    if ((allSuggestions || []).length === 0 && (suggestions || []).length === 0) {
      setAllSuggestions(defaultSuggestions);
    }
  }, [allSuggestions, suggestions]);

  useEffect(() => {
    if (!input) {
      setFiltered([]);
      setShowSuggestions(false);
      return;
    }
    const q = input.toLowerCase();
    const source = allSuggestions.length ? allSuggestions : suggestions;
    const f = source.filter(s => s.toLowerCase().includes(q) && !validTags.includes(s)).slice(0, 8);
    setFiltered(f);
    setShowSuggestions(f.length > 0);
  }, [input, allSuggestions, suggestions, validTags]);

  const addTag = (t) => {
    const value = t.trim();
    if (!value) return;
    if (validTags.includes(value)) return setInput('');
    setTags(prev => {
      const current = Array.isArray(prev) ? prev : [];
      return [...current, value];
    });
    setInput('');
    setShowSuggestions(false);
    inputRef.current && inputRef.current.focus();
  };

  const removeTag = (t) => {
    setTags(prev => {
      const current = Array.isArray(prev) ? prev : [];
      return current.filter(x => x !== t);
    });
  };

  const onKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      if (input) addTag(input);
    } else if (e.key === 'Backspace' && !input && validTags.length) {
      // Remove last tag
      setTags(prev => {
        const current = Array.isArray(prev) ? prev : [];
        return current.slice(0, -1);
      });
    } else if (e.key === 'ArrowDown' && filtered.length) {
      // focus first suggestion (simple UX)
      const el = document.querySelector('.tag-suggestion');
      el && el.focus();
    }
  };

  return (
    <div className="tag-input">
      <div className="tags">
        {validTags.map(t => (
          <span className="chip" key={t}>
            {t}
            <button className="chip-remove" onClick={() => removeTag(t)} aria-label={`Eliminar ${t}`}>×</button>
          </span>
        ))}
        <input
          ref={inputRef}
          className="tag-input-field"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder={placeholder}
        />
      </div>

      {showSuggestions && (
        <div className="tag-suggestions" role="listbox">
          {filtered.map(s => (
            <button type="button" key={s} className="tag-suggestion" onClick={() => addTag(s)}>{s}</button>
          ))}
        </div>
      )}
    </div>
  );
}

export default TagInput;
