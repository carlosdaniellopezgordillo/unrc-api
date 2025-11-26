from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


def calcular_compatibilidad(estudiante, oportunidad) -> float:
    """

     Usa TF-IDF para similitud semántica de habilidades.
    """
    puntuacion = 0.0
    
    # Extrae datos del estudiante
    semestre_est = getattr(estudiante, 'semestre', 0) or 0
    gpa_est = getattr(estudiante, 'gpa', 0.0) or 0.0
    habilidades_est = getattr(estudiante, 'habilidades_tecnicas', []) or []
    disponibilidad_est = getattr(estudiante, 'disponibilidad', True)
    experiencia_count = len(getattr(estudiante, 'experiencias', []) or [])
    proyectos_count = len(getattr(estudiante, 'proyectos_lista', []) or [])
    
    # Extrae requisitos de la oportunidad
    semestre_min = getattr(oportunidad, 'semestre_minimo', 0)
    gpa_min = getattr(oportunidad, 'gpa_minimo', None)
    habilidades_req = getattr(oportunidad, 'habilidades_requeridas', []) or []
    experiencia_requerida = getattr(oportunidad, 'anos_experiencia_minimo', 0) or 0
    
    # ============ CRITERIO 1: Semestre (20%) ============
    # Penalizar si no cumple, dar bonus si excede
    if semestre_est >= semestre_min:
        puntuacion += 20.0
        # Bonus: cada semestre extra = 0.5 puntos (máx 5 puntos)
        bonus_semestre = min((semestre_est - semestre_min) * 0.5, 5.0)
        puntuacion += bonus_semestre
    else:
        # Penalización por no cumplir semestre mínimo
        deficit = (semestre_min - semestre_est) / max(semestre_min, 1)
        penalizacion = deficit * 20.0
        puntuacion -= min(penalizacion, 20.0)
    
    # ============ CRITERIO 2: GPA (15%) ============
    if gpa_min is None or gpa_est >= gpa_min:
        puntuacion += 15.0
        # Bonus: GPA más alto = más puntos
        if gpa_min and gpa_est > gpa_min:
            bonus_gpa = min((gpa_est - gpa_min) * 5, 5.0)
            puntuacion += bonus_gpa
    else:
        # Penalización por GPA insuficiente
        deficit_gpa = (gpa_min - gpa_est) / max(gpa_min, 1)
        penalizacion_gpa = deficit_gpa * 15.0
        puntuacion -= min(penalizacion_gpa, 15.0)
    
    # ============ CRITERIO 3: Habilidades con TF-IDF (40% - MÁS IMPORTANTE) ============
    # Usa similitud coseno en lugar de matching exacto
    puntuacion_habilidades = calcular_similitud_habilidades_tfidf(habilidades_est, habilidades_req)
    puntuacion += puntuacion_habilidades * 0.40  # 40 puntos máximo
    
    # ============ CRITERIO 4: Experiencia (15%) ============
    # Calcula basado en cantidad de experiencias
    experiencia_score = min(experiencia_count / max(experiencia_requerida, 1), 1.0)
    puntuacion += experiencia_score * 15.0
    
    # ============ CRITERIO 5: Proyectos (10%) ============
    # Bonus por proyectos realizados
    proyecto_score = min(proyectos_count / 2, 1.0)  # 2+ proyectos = máximo bonus
    puntuacion += proyecto_score * 10.0
    
    # ============ CRITERIO 6: Disponibilidad (5%) ============
    if disponibilidad_est:
        puntuacion += 5.0
    
    # Retorna puntuación entre 0-100
    return max(0, min(puntuacion, 100.0))


def calcular_similitud_habilidades_tfidf(habilidades_est, habilidades_req) -> float:
    """
    Calcula similitud entre habilidades usando TF-IDF y cosine similarity.
    
    VENTAJAS:
    - Detecta habilidades similares (python ≈ python3)
    - Entiende relaciones semánticas
    - Más flexible que matching exacto
    
    PARÁMETROS:
    - habilidades_est: lista de habilidades del estudiante
    - habilidades_req: lista de habilidades requeridas
    
    RETORNA:
    - Puntuación entre 0-100
    """
    
    # Validar que haya habilidades
    if not habilidades_req:
        return 100.0  # Si no hay requisitos, máxima puntuación
    
    if not habilidades_est:
        return 0.0  # Si estudiante no tiene habilidades, puntuación mínima
    
    # Convertir a strings y limpiar
    habilidades_est = [str(h).lower().strip() for h in habilidades_est if h]
    habilidades_req = [str(h).lower().strip() for h in habilidades_req if h]
    
    # MÉTODO 1: Matching exacto (rápido)
    # Contar habilidades que coinciden exactamente
    habilidades_est_set = set(habilidades_est)
    coincidencias_exactas = len(habilidades_est_set.intersection(set(habilidades_req)))
    
    # Si hay coincidencias exactas, usarlas
    if coincidencias_exactas > 0:
        return (coincidencias_exactas / len(habilidades_req)) * 100.0
    
    # MÉTODO 2: TF-IDF (más sofisticado)
    try:
        # Crear documento para cada conjunto de habilidades
        # El documento es: "python java docker" (todas las habilidades juntas)
        doc_estudiante = " ".join(habilidades_est)
        doc_requerido = " ".join(habilidades_req)
        
        # Vectorizar usando TF-IDF
        vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 2))
        try:
            # Intentar con ambos documentos
            tfidf_matrix = vectorizer.fit_transform([doc_estudiante, doc_requerido])
            # Calcular similitud coseno
            similitud = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return similitud * 100.0
        except:
            # Si falla TF-IDF, usar similitud de substrings
            return calcular_similitud_substrings(habilidades_est, habilidades_req)
    except:
        # Si todo falla, retornar 0
        return 0.0


def calcular_similitud_substrings(habilidades_est, habilidades_req) -> float:
    """
    Fallback: Calcula similitud buscando substrings comunes.
    Útil cuando TF-IDF no está disponible.
    
    EJEMPLOS:
    - "python" y "python3" → similitud alta
    - "javascript" y "js" → similitud media
    - "docker" y "kubernetes" → similitud baja
    """
    similitudes = []
    
    for req in habilidades_req:
        max_similitud = 0.0
        
        for est in habilidades_est:
            # Similitud por substring
            if req in est or est in req:
                max_similitud = 1.0
                break
            
            # Similitud por caracteres comunes (Jaccard)
            set_req = set(req)
            set_est = set(est)
            if set_req and set_est:
                interseccion = len(set_req & set_est)
                union = len(set_req | set_est)
                similitud_jaccard = interseccion / union if union > 0 else 0.0
                max_similitud = max(max_similitud, similitud_jaccard)
        
        similitudes.append(max_similitud)
    
    # Promedio de similitudes
    resultado = (sum(similitudes) / len(similitudes)) * 100.0 if similitudes else 0.0
    return resultado