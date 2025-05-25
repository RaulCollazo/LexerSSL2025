import ply.lex as lex
import os

# Palabras Reservadas
reserved = {
    '"estado"': 'ESTADOO',
    '"To do"': 'TO_DO',
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
    '"integrante"':'INTEGRANTE',
    '"nombre"': 'NOMBRE',
    '"edad"': 'EDAD',
    '"cargo"': 'CARGO',
    '"foto"':'FOTO',
    '"email"':'CORREO_EMAIL',
    '"salario"': 'SALARIO',
    '"activo"': 'ACTIVO',
    '"habilidades"':'HABILIDADES',
    '"proyecto"':'PROYECTO',
    '"resumen"':'RESUMEN',
    '"tareas"':'TAREAS',
    '"fecha_inicio"': 'FECHA_INICIO',
    '"fecha_fin"': 'FECHA_FIN',
    '"video"':'VIDEO',
    '"conclusión"':'CONCLUSION',
    '"tarea"':'TAREA',

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

def t_NOMBREPROPIO(t):
    r'"[A-Z][a-z]+ [A-Z][a-z]+"'
    return t

def t_STRING(t):
    r'"([^\\\n]|(\\.))*?"'
    # Si es palabra reservada, cambia tipo y valor
    if t.value in reserved:
        t.type = reserved[t.value]
        t.value = t.type  # O si prefieres, t.value = t.value.strip('"')
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()



print(f"¿Desea analizar Léxicamente un string o un archivo?")

def mostrar_menu():
    print("Menú de opciones")
    print("1. Realizar el análisis léxico de forma manual")
    print("2. Analizar un archivo.json específico")
    print("3. Salir")

ruta_archivo = ''

def analizar_entrada_manual():
    data = input("Ingrese el texto a analizar: ")
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        print(f"Se ha encontrado el token: '{tok.value}' del tipo: {tok.type}")

def analizar_archivo():
    global ruta_archivo  # Acceder y modificar la variable global ruta_archivo
    ruta_archivo = input("Ingrese la ruta del archivo .json: ")
    try:
        with open(ruta_archivo, "r") as file:
            data = file.read()
            lexer.input(data)
            while True:
                tok = lexer.token()
                if not tok:
                    break
                print(f"Se ha encontrado el token: '{tok.value}' del tipo: {tok.type}")
    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo en la ruta: {ruta_archivo}")

def menu():
    while True:
        mostrar_menu()
        try:
            opcion = int(input("Elige una opción (1-3): "))
            if opcion == 1:
                analizar_entrada_manual()
            elif opcion == 2:
                analizar_archivo()
                # Después de llamar a analizar_archivo(), ruta_archivo debería estar definida
                if ruta_archivo:
                    carpeta = os.path.dirname(os.path.abspath(__file__))
                    nombre_archivo = os.path.basename(ruta_archivo)
                    nombre_archivo = nombre_archivo + '.html'
                    # Crear la carpeta si no existe
                    os.makedirs(carpeta, exist_ok=True)
                    # Definir la ruta completa del archivo
                    global ruta_completa
                    ruta_completa = os.path.join(carpeta, nombre_archivo)
                    # Crear y escribir en el archivo HTML
                    with open(ruta_completa, 'w') as archivo:
                        archivo.write('')
                else:
                    print("No se ha proporcionado una ruta válida.")
            elif opcion == 3:
                print("Saliendo del programa...")
                break
            else:
                print("Opción no válida. Por favor, elige una opción del 1 al 3.")
        except ValueError:
            print("Entrada no válida. Por favor, introduce un número.")

if __name__ == "__main__":
    menu()