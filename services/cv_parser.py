import os
from typing import Dict, List

# Importar librerías para leer PDFs y Word
try:
    from pypdf import PdfReader
except Exception:
    try:
        from PyPDF2 import PdfReader
    except Exception:
        PdfReader = None

from docx import Document
import re

# Importar spaCy para análisis de lenguaje natural (NLP)
# Detecta entidades como universidades, organizaciones, etc
try:
    import spacy
    nlp = None
    try:
        nlp = spacy.load('es_core_news_sm')  # Modelo en español
    except Exception:
        try:
            nlp = spacy.load('en_core_web_sm')  # Fallback: inglés
        except Exception:
            nlp = None
except Exception:
    spacy = None
    nlp = None

KEY_SECTIONS = [
    'habilidad', 'skills', 'habilidades',
    'proyecto', 'proyectos',
    'experiencia', 'experiencias',
    'formación', 'educación', 'estudios', 'carrera'
]


def extract_text_from_pdf(path: str) -> str:
    """Extrae texto de PDF. Si falla, devuelve string vacío."""
    text = []
    try:
        reader = PdfReader(path)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                # Normalizar espacios entre caracteres (problema común en PDFs escaneados)
                # "C A R L O S" → "CARLOS"
                page_text = re.sub(r'\s+', ' ', page_text)
                # Detectar y arreglar caracteres separados por espacios
                # Si hay muchos espacios entre caracteres, probablemente sea un PDF mal formateado
                if page_text.count(' ') > len(page_text) * 0.3:
                    # Remover espacios entre caracteres individuales
                    page_text = re.sub(r'(\w)\s+(?=\w)', r'\1', page_text)
                text.append(page_text)
    except Exception:
        return ''
    return '\n'.join(text)


def extract_text_from_docx(path: str) -> str:
    """Extrae texto de Word (.docx). Si falla, devuelve string vacío."""
    try:
        doc = Document(path)
        paragraphs = [p.text for p in doc.paragraphs if p.text]
        return '\n'.join(paragraphs)
    except Exception:
        return ''


def extract_text(path: str) -> str:
    """Detecta tipo de archivo y extrae texto (PDF o DOCX)."""
    ext = os.path.splitext(path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(path)
    elif ext in ('.doc', '.docx'):
        return extract_text_from_docx(path)
    else:
        return ''


def simple_parse_sections(text: str) -> Dict[str, List[str]]:
    """
    Parser mejorado de CVs v2.0. 
    Extrae: carrera, habilidades, proyectos, experiencias.
    """
    # Preparar texto: líneas individuales
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    lower_lines = [l.lower() for l in lines]

    # Inicializar resultados
    result = {
        'carrera': None,
        'habilidades': [],
        'proyectos': [],
        'experiencias': []
    }

    text_norm = re.sub(r"\s+", " ", text)
    text_lower = text_norm.lower()

    # Palabras clave para detectar habilidades
    skill_keywords = [
        'python', 'java', 'javascript', 'c++', 'c#', 'ruby', 'php', 'golang', 'rust', 'kotlin',
        'sql', 'postgres', 'postgresql', 'mysql', 'mongodb', 'nosql', 'oracle', 'sqlite',
        'docker', 'kubernetes', 'jenkins', 'gitlab', 'github', 'git',
        'machine learning', 'deep learning', 'data science', 'ai', 'artificial intelligence',
        'pandas', 'numpy', 'scipy', 'scikit-learn', 'sklearn',
        'react', 'angular', 'vue', 'node', 'nodejs', 'express',
        'aws', 'azure', 'gcp', 'cloud', 'devops',
        'html', 'css', 'bootstrap', 'tailwind',
        'tensorflow', 'pytorch', 'keras', 'transformers', 'huggingface',
        'nlp', 'natural language', 'computer vision', 'cv',
        'rest', 'api', 'graphql', 'websocket',
        'agile', 'scrum', 'kanban', 'jira',
        'linux', 'windows', 'macos', 'unix',
        'excel', 'powerpoint', 'tableau', 'power bi', 'looker',
        'selenium', 'pytest', 'unittest', 'testing',
        'fastapi', 'django', 'flask', 'spring',
        'redis', 'elasticsearch', 'rabbitmq',
        'spacy', 'nltk', 'gensim',
        'git', 'svn', 'bitbucket'
    ]

    # CARRERA: Buscar patrones "EDUCACIÓN:" o "CARRERA:"
    # Validar que no sea demasiado larga (máx 200 caracteres)
    carrera_patterns = [
        r"(carrera|estudios|formaci[oó]n|educaci[oó]n|licenciatura)[:\s\-]*([A-Za-z0-9\sáéíóú\,\.\-]+?)(?=\n|experiencia|laboral|trabajo|proyecto|habilidad|skill)",
    ]
    
    for pattern in carrera_patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            extracted = match.group(2) if match.lastindex >= 2 else match.group(0)
            extracted = extracted.strip()
            # Limitar a UNA sola línea
            lines_extracted = extracted.split('\n')
            first_line = lines_extracted[0].split(',')[0].strip()
            
            # Buscar solo palabras de carrera, no párrafos completos
            if 5 < len(first_line) < 150:
                # Validar que NO sea un párrafo (no tenga verbos de acción)
                if not any(verb in first_line.lower() for verb in ['desarrollé', 'trabajé', 'realizé', 'implementé', 'creé', 'participé', 'dirigí']):
                    result['carrera'] = first_line
                    break
    
    # Si no encontramos, buscar palabra clave de educación seguida de carrera
    if not result['carrera']:
        for i, l in enumerate(lower_lines):
            if any(k in l for k in ('carrera', 'estudios', 'formación', 'educación', 'licenciatura')):
                # La carrera está en la siguiente línea
                if i + 1 < len(lines):
                    candidate = lines[i+1].strip()
                    # Debe ser corta y no tener verbos de acción
                    if 5 < len(candidate) < 150 and not candidate.endswith('.'):
                        if not any(verb in candidate.lower() for verb in ['desarrollé', 'trabajé', 'realizé']):
                            result['carrera'] = candidate
                            break
                # O en la misma línea después del ":"
                if ':' in l:
                    candidate = l.split(':', 1)[1].strip().split('\n')[0].strip()
                    if 5 < len(candidate) < 150:
                        if not any(verb in candidate.lower() for verb in ['desarrollé', 'trabajé', 'realizé']):
                            result['carrera'] = candidate
                            break
    
    # Fallback: buscar palabras de grados pero NO párrafos
    if not result['carrera']:
        for l in lines:
            if any(degree in l.lower() for degree in ['ingenier', 'licenci', 'lic.', 'técnic', 'grado', 'pregrado']):
                candidate = l.strip()
                # Si es una línea que termina abruptamente o es muy corta, es probablemente carrera
                if 5 < len(candidate) < 150 and not candidate.endswith('.'):
                    result['carrera'] = candidate
                    break

    # HABILIDADES: Buscar por palabras clave (python, java, etc)
    found_skills = set()
    for kw in skill_keywords:
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.add(kw.title())
    
    if found_skills:
        result['habilidades'].extend(sorted(found_skills))

    # HABILIDADES: Buscar sección "HABILIDADES:" y extraer líneas siguientes
    for i, l in enumerate(lower_lines):
        if any(k in l for k in ('habilidad', 'skills', 'competencia', 'técnica')):
            chunk = lines[i+1:i+6]
            for c in chunk:
                if c and not any(keyword in c.lower() for keyword in 
                               ('experiencia', 'proyecto', 'formación', 'educación')):
                    if ',' in c:
                        result['habilidades'].extend([x.strip() for x in c.split(',') if x.strip()])
                    else:
                        result['habilidades'].append(c.strip())

    # PROYECTOS: Buscar sección "PROYECTOS:" y extraer líneas siguientes
    # Mejorado: detectar mejor dónde termina la sección
    for i, l in enumerate(lower_lines):
        if any(k in l for k in ('proyecto', 'portfolio', 'proyecto', 'desarrollo', 'solución')):
            # Pero evitar falsos positivos
            if 'proyecto' in l.lower() or 'portfolio' in l.lower() or 'desarrollo de' in l.lower():
                chunk = lines[i+1:i+15]  # Aumentar límite
                for c in chunk:
                    # Detener si encontramos otra sección
                    if any(section in c.lower() for section in 
                           ['habilidad', 'skill', 'educación', 'carrera', 'formación', 'contacto', 'experiencia']):
                        break
                    
                    if c and len(c) > 5:
                        # Filtrar líneas que sean solo números
                        if any(char.isalpha() for char in c):
                            result['proyectos'].append(c.strip())

    # EXPERIENCIA: Buscar sección "EXPERIENCIA:" y extraer líneas siguientes
    # Mejorado: detectar mejor dónde termina la sección
    for i, l in enumerate(lower_lines):
        if any(k in l for k in ('experiencia', 'laboral', 'profesional', 'trabajo', 'empleo')):
            # Extraer líneas hasta la siguiente sección
            chunk = lines[i+1:i+15]  # Aumentar de 10 a 15
            in_experience = True
            for c in chunk:
                # Detectar si llegamos a otra sección
                if any(section in c.lower() for section in 
                       ['proyecto', 'habilidad', 'skill', 'educación', 'carrera', 'formación', 'contacto']):
                    in_experience = False
                    break
                
                # Agregar solo si tiene contenido significativo
                if c and len(c) > 5 and in_experience:
                    # Filtrar líneas que sean solo números o símbolos
                    if any(char.isalpha() for char in c):
                        result['experiencias'].append(c.strip())

    # Fallback: líneas que empiezan con "skills:", "proyecto:", etc
    for l in lines:
        low = l.lower()
        if any(low.startswith(prefix) for prefix in ('skills:', 'habilidades:', 'habilidad:')):
            tail = l.split(':', 1)[1]
            result['habilidades'].extend([x.strip() for x in tail.split(',') if x.strip()])
        if any(low.startswith(prefix) for prefix in ('proyecto:', 'proyectos:')):
            tail = l.split(':', 1)[1]
            if tail.strip():
                result['proyectos'].append(tail.strip())
        if any(low.startswith(prefix) for prefix in ('experiencia:', 'experiencias:', 'empleo:')):
            tail = l.split(':', 1)[1]
            if tail.strip():
                result['experiencias'].append(tail.strip())

    # Limpiar: eliminar duplicados y validar longitud mínima
    # Carrera: máximo 1 línea, entre 5-150 caracteres
    if result['carrera']:
        result['carrera'] = result['carrera'].strip()
        if len(result['carrera']) > 150:
            result['carrera'] = result['carrera'][:150]
    
    # Habilidades: pequeños items, sin duplicados
    result['habilidades'] = list(dict.fromkeys([
        h.strip() for h in result['habilidades'] 
        if h and len(h.strip()) > 0 and len(h.strip()) < 100
    ]))
    
    # Proyectos: items más largos permitidos
    result['proyectos'] = list(dict.fromkeys([
        p.strip() for p in result['proyectos'] 
        if p and len(p.strip()) > 5 and len(p.strip()) < 500 and p.count('\n') < 3
    ]))
    
    # Experiencias: items medianos
    result['experiencias'] = list(dict.fromkeys([
        e.strip() for e in result['experiencias'] 
        if e and len(e.strip()) > 5 and len(e.strip()) < 500 and e.count('\n') < 3
    ]))

    # Usar spaCy NLP para enriquecer si está disponible
    if nlp is not None:
        try:
            doc = nlp(text)
            # Detectar universidades si carrera no está definida
            if not result['carrera']:
                for ent in doc.ents:
                    if ent.label_ in ('ORG',) and any(edu_word in ent.text.lower() 
                                                      for edu_word in ('universidad', 'escuela', 'instituto', 'college')):
                        result['carrera'] = ent.text
                        break
            # Usar noun chunks para encontrar habilidades adicionales
            for chunk in doc.noun_chunks:
                ch = chunk.text.lower()
                for kw in skill_keywords:
                    if kw in ch and kw not in [h.lower() for h in result['habilidades']]:
                        result['habilidades'].append(chunk.text.title())
        except Exception:
            pass

    return result


def parse_cv(path: str) -> Dict[str, List[str]]:
    """Extrae texto de CV y parsea para obtener datos estructurados."""
    try:
        text = extract_text(path)
        if not text:
            return {'carrera': None, 'habilidades': [], 'proyectos': [], 'experiencias': []}
        return simple_parse_sections(text)
    except Exception as e:
        print(f"Error parsing CV: {e}")
        return {'carrera': None, 'habilidades': [], 'proyectos': [], 'experiencias': []}

