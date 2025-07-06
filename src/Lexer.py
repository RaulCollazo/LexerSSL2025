import ply.lex as lex

reserved = {
    '"estado"': 'ESTADO',
    '"To do"': 'TO_DO',
    '"To Do"': 'TO_DO',
    '"In progress"': 'INPROGRESS',
    '"Canceled"': 'CANCELED',
    '"Done"': 'DONE',
    '"On hold"': "ON_HOLD",
    '"Product Analyst"': 'PRODUCT_ANALYST',
    '"Project Manager"': 'PROJECT_MANAGER',
    '"Developer"': 'DEVELOPER',
    '"Marketing"': 'MARKETING',
    '"UX designer"': 'UXDESIGNER',
    '"Marketing Devops"': 'MARKETING_DEVOPS',
    '"DB admin"': 'DB_ADMIN',
    '"version"': 'VERSION',
    '"firma_digital"': 'FIRMA_DIGITAL',
    '"equipos"': 'EQUIPOS',
    '"nombre_equipo"': 'NOMBRE_EQUIPO',
    '"identidad_equipo"': 'IDENTIDAD_EQUIPO',
    '"direccion"': 'DIRECCION',
    '"link"': 'LINK',
    '"carrera"': 'CARRERA',
    '"asignatura"': 'ASIGNATURA',
    '"universidad_regional"': 'UNIVERSIDAD_REGIONAL',
    '"alianza_equipo"': 'ALIANZA_EQUIPO',
    '"integrantes"': 'INTEGRANTES',
    '"proyectos"': 'PROYECTOS',
    '"calle"': 'CALLE',
    '"ciudad"': 'CIUDAD',
    '"pais"': 'PAIS',
    '"país"': 'PAIS',
    '"integrante"': 'INTEGRANTE',
    '"nombre"': 'NOMBRE',
    '"edad"': 'EDAD',
    '"cargo"': 'CARGO',
    '"foto"': 'FOTO',
    '"email"': 'CORREO_EMAIL',
    '"salario"': 'SALARIO',
    '"activo"': 'ACTIVO',
    '"habilidades"': 'HABILIDADES',
    '"proyecto"': 'PROYECTO',
    '"resumen"': 'RESUMEN',
    '"tareas"': 'TAREAS',
    '"fecha_inicio"': 'FECHA_INICIO',
    '"fecha_fin"': 'FECHA_FIN',
    '"video"': 'VIDEO',
    '"conclusión"': 'CONCLUSION',
    '"conclusion"': 'CONCLUSION',
    '"tarea"': 'TAREA',
    '"nombre_equipo"' : 'NOMBRE_EQUIPO'
}

tokens = (
    'URL', 'DATE', 'INTEGER', 'FLOAT', 'BOOLEAN',
    'ILLAVE', 'DLLAVE', 'ICORCHETE', 'DCORCHETE',
    'COMA', 'DOSPUNTOS', 'NOMBREPROPIO', 'STRING', 'NULL', 'VERSIONE',
    'EMAIL',
) + tuple(reserved.values())

t_ILLAVE = r'\{'
t_DLLAVE = r'\}'
t_ICORCHETE = r'\['
t_DCORCHETE = r'\]'
t_COMA = r','
t_DOSPUNTOS = r':'

# NOMBREPROPIO primero para prioridad sobre STRING
def t_NOMBREPROPIO(t):
    r'"[A-Z]+([a-z]+)\s [A-Z]+([a-z]+)"'
    if t.value in reserved:
        t.type = reserved.get(t.value)
    else:
        t.type = 'NOMBREPROPIO'
    return t

def t_EMAIL(t):
    r'"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,4}"'
    t.value = t.value.strip('"')
    return t

def t_URL(t):
    r'"(https?|ftp)://[^\s"]+"'
    t.value = t.value.strip('"')
    return t

def t_DATE(t):
    r'"(19[0-9]{2}|20[0-9]{2})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])"'
    t.value = t.value.strip('"')
    return t

def t_NULL(t):
    r'null'
    t.value = None
    return t

def t_VERSIONE(t):
    r'"\d+\.\d{1,2}"'
    t.value = t.value.strip('"')
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_BOOLEAN(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    if t.value in reserved:
        t.type = reserved.get(t.value)
        # NO le quites las comillas, así el parser ve CALLE
    else:
        t.value = t.value.strip('"')
    return t

t_ignore = ' \t\n\r'

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()