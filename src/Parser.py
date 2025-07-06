import ply.yacc as yacc
from Lexer import tokens, lexer
import os

# Variable global para la ruta de salida del HTML
ruta_completa = "output.html"

def iniciar_html(nombre="output.html"):
    global ruta_completa
    ruta_completa = nombre
    with open(ruta_completa, 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Equipos</title>
  <style>
    .equipo { border: 1px solid gray; padding: 20px; margin-bottom: 30px; }
    .integrante, .proyecto { margin-left: 20px; }
    table { border-collapse: collapse; margin: 10px 0; }
    table, th, td { border: 1px solid #aaa; padding: 4px; }
  </style>
</head>
<body>
''')

def cerrar_html():
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write('</body></html>')

# ----------- REGLA PRINCIPAL -----------
def p_expresion_SIGMA(p):
    'expresion_SIGMA : ILLAVE json_atributos_nt DLLAVE'
    p[0] = p[2]
    cerrar_html()
    print("[DEBUG] Entrando a expresion_SIGMA")

def p_json_atributos_nt(p):
    '''json_atributos_nt : equipos_nt COMA VERSIONNT COMA FIRMA_DIGITALNT
                        | equipos_nt COMA FIRMA_DIGITALNT COMA VERSIONNT
                        | VERSIONNT COMA equipos_nt COMA FIRMA_DIGITALNT
                        | VERSIONNT COMA FIRMA_DIGITALNT COMA equipos_nt 
                        | FIRMA_DIGITALNT COMA equipos_nt COMA VERSIONNT
                        | FIRMA_DIGITALNT COMA VERSIONNT COMA equipos_nt
                        | equipos_nt COMA VERSIONNT
                        | equipos_nt COMA FIRMA_DIGITALNT
                        | VERSIONNT COMA equipos_nt
                        | FIRMA_DIGITALNT COMA equipos_nt
                        | equipos_nt'''
    result = {}
    for item in p[1:]:
        if isinstance(item, dict):
            result.update(item)
    p[0] = result
    print("[DEBUG] Entrando a json_atributos_nt")

def p_equipos_nt(p):
    'equipos_nt : EQUIPOS DOSPUNTOS ICORCHETE ILLAVE equipo_atributos_nt DLLAVE DCORCHETE'
    p[0] = {"equipos": [p[5]]}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write('<div class="equipo">\n')
    print("[DEBUG] Entrando a equipos_nt")

def p_equipo_atributos_nt(p):
    '''equipo_atributos_nt : NOMBRE_EQUIPONT COMA IDENTIDAD_EQUIPONT COMA direccion_nt COMA LINKNT COMA CARRERANT COMA ASIGNATURANT COMA UNIVERSIDAD_REGIONALNT COMA ALIANZA_EQUIPONT COMA integrantes_nt COMA proyectos_nt
                          | NOMBRE_EQUIPONT COMA IDENTIDAD_EQUIPONT COMA LINKNT COMA CARRERANT COMA ASIGNATURANT COMA UNIVERSIDAD_REGIONALNT COMA ALIANZA_EQUIPONT COMA integrantes_nt COMA proyectos_nt
                          | NOMBRE_EQUIPONT COMA IDENTIDAD_EQUIPONT COMA direccion_nt COMA CARRERANT COMA ASIGNATURANT COMA UNIVERSIDAD_REGIONALNT COMA ALIANZA_EQUIPONT COMA integrantes_nt COMA proyectos_nt
                          | NOMBRE_EQUIPONT COMA IDENTIDAD_EQUIPONT COMA CARRERANT COMA ASIGNATURANT COMA UNIVERSIDAD_REGIONALNT COMA ALIANZA_EQUIPONT COMA integrantes_nt COMA proyectos_nt'''
    equipo = {}
    for item in p[1:]:
        if isinstance(item, dict):
            equipo.update(item)
    p[0] = equipo
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write('</div>\n')
    print("[DEBUG] Entrando a equipo_atributos_nt")

def p_NOMBRE_EQUIPONT(p):
    '''NOMBRE_EQUIPONT : NOMBRE_EQUIPO DOSPUNTOS STRING
                       | NOMBRE_EQUIPO DOSPUNTOS NOMBREPROPIO'''
    p[0] = {"nombre_equipo": p[3]}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write(f"<h1>{p[3]}</h1>\n")
    print("[DEBUG] Entrando a NOMBRE_EQUIPONT")

def p_IDENTIDAD_EQUIPONT(p):
    'IDENTIDAD_EQUIPONT : IDENTIDAD_EQUIPO DOSPUNTOS URL'
    p[0] = {"identidad_equipo": p[3]}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write(f'<p><b>Identidad equipo:</b> <a href="{p[3]}" target="_blank">{p[3]}</a></p>\n')
    print("[DEBUG] Entrando a Identidad_EQUIPO")

def p_direccion_nt(p):
    '''direccion_nt : DIRECCION DOSPUNTOS ILLAVE calle_nt COMA ciudad_nt COMA pais_nt DLLAVE
                    | DIRECCION DOSPUNTOS ILLAVE pais_nt COMA calle_nt COMA ciudad_nt DLLAVE
                    | DIRECCION DOSPUNTOS ILLAVE calle_nt COMA pais_nt COMA ciudad_nt DLLAVE'''
    dir_dict = {}
    dir_dict.update(p[4])
    dir_dict.update(p[6])
    dir_dict.update(p[8])
    p[0] = {"direccion": dir_dict}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        dirstr = ", ".join(f"{k}: {v}" for k, v in dir_dict.items())
        f.write(f"<p><b>Dirección:</b> {dirstr}</p>\n")
    print("[DEBUG] Entrando a direccion_nt")

def p_calle_nt(p):
    'calle_nt : CALLE DOSPUNTOS STRING'
    p[0] = {"calle": p[3]}
    print("[DEBUG] Entrando a calle_nt")

def p_ciudad_nt(p):
    'ciudad_nt : CIUDAD DOSPUNTOS STRING'
    p[0] = {"ciudad": p[3]}
    print("[DEBUG] Entrando a ciudad_nt")

def p_pais_nt(p):
    'pais_nt : PAIS DOSPUNTOS STRING'
    p[0] = {"país": p[3]}
    print("[DEBUG] Entrando a pais_nt")

def p_LINKNT(p):
    'LINKNT : LINK DOSPUNTOS URL'
    p[0] = {"link": p[3]}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write(f'<p><b>Link:</b> <a href="{p[3]}" target="_blank">{p[3]}</a></p>\n')
    print("[DEBUG] Entrando a LINK")

def p_CARRERANT(p):
    'CARRERANT : CARRERA DOSPUNTOS STRING'
    p[0] = {"carrera": p[3]}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write(f'<p><b>Carrera:</b> {p[3]}</p>\n')
    print("[DEBUG] Entrando a CARRERA")

def p_ASIGNATURANT(p):
    'ASIGNATURANT : ASIGNATURA DOSPUNTOS STRING'
    p[0] = {"asignatura": p[3]}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write(f'<p><b>Asignatura:</b> {p[3]}</p>\n')
    print("[DEBUG] Entrando a ASIGNATURA")

def p_UNIVERSIDAD_REGIONALNT(p):
    'UNIVERSIDAD_REGIONALNT : UNIVERSIDAD_REGIONAL DOSPUNTOS STRING'
    p[0] = {"universidad_regional": p[3]}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write(f'<p><b>Universidad regional:</b> {p[3]}</p>\n')
    print("[DEBUG] Entrando a UNIVERSIDAD_REGIONAL")

def p_ALIANZA_EQUIPONT(p):
    'ALIANZA_EQUIPONT : ALIANZA_EQUIPO DOSPUNTOS STRING'
    p[0] = {"alianza_equipo": p[3]}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write(f'<p><b>Alianza equipo:</b> {p[3]}</p>\n')
    print("[DEBUG] Entrando a ALIANZA")

def p_integrantes_nt(p):
    'integrantes_nt : INTEGRANTES DOSPUNTOS ICORCHETE integrante_list_nt DCORCHETE'
    p[0] = {"integrantes": p[4]}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write("<h2>Integrantes</h2><ul>\n")
        for integrante in p[4]:
            f.write(f"<li><b>{integrante.get('nombre','')}</b><ul>")
            for k, v in integrante.items():
                if k == "nombre":
                    continue
                if k == "foto":
                    f.write(f'<li>Foto: <a href="{v}" target="_blank">{v}</a></li>')
                elif k == "email":
                    f.write(f'<li>Email: <a href="mailto:{v}">{v}</a></li>')
                else:
                    f.write(f"<li>{k.title()}: {v}</li>")
            f.write("</ul></li>\n")
        f.write("</ul>\n")
    print("[DEBUG] Entrando a integrantes_nt")

def p_integrante_list_nt(p):
    '''integrante_list_nt : ILLAVE integrante_nt DLLAVE COMA integrante_list_nt
                         | ILLAVE integrante_nt DLLAVE'''
    if len(p) == 6:
        p[0] = [p[2]] + p[5]
    else:
        p[0] = [p[2]]
    print("[DEBUG] Entrando a integrante_list_nt")

def p_integrante_nt(p):
    'integrante_nt : integrante_atributos_nt '
    p[0] = p[1]
    print("[DEBUG] Entrando a integrante_nt")

def p_integrante_atributos_nt(p):
    '''integrante_atributos_nt : nombre_integrante_nt COMA EDAD DOSPUNTOS INTEGER COMA cargo_nt COMA FOTO DOSPUNTOS URL COMA CORREO_EMAIL DOSPUNTOS EMAIL COMA HABILIDADES DOSPUNTOS STRING COMA SALARIO DOSPUNTOS FLOAT COMA ACTIVO DOSPUNTOS BOOLEAN
                              | nombre_integrante_nt COMA cargo_nt COMA FOTO DOSPUNTOS URL COMA CORREO_EMAIL DOSPUNTOS EMAIL COMA HABILIDADES DOSPUNTOS STRING COMA SALARIO DOSPUNTOS FLOAT COMA ACTIVO DOSPUNTOS BOOLEAN'''
    integrante = {}
    for item in p[1:]:
        if isinstance(item, dict):
            integrante.update(item)
    # Sobreescritura por índices (si existen)
    for i, name in [(3, "edad"), (13, "foto"), (15, "email"), (17, "habilidades"), (19, "salario"), (21, "activo")]:
        if len(p) > i:
            integrante[name] = p[i]
    p[0] = integrante
    print("[DEBUG] Entrando a integrante_atributos_nt")

def p_nombre_integrante_nt(p):
    'nombre_integrante_nt : NOMBRE DOSPUNTOS NOMBREPROPIO'
    p[0] = {"nombre": p[3]}
    print("[DEBUG] Entrando a nombre_integrante_nt:", p[3])

def p_cargo_nt(p):
    '''cargo_nt : CARGO DOSPUNTOS PRODUCT_ANALYST
               | CARGO DOSPUNTOS PROJECT_MANAGER
               | CARGO DOSPUNTOS UXDESIGNER
               | CARGO DOSPUNTOS MARKETING
               | CARGO DOSPUNTOS DEVELOPER
               | CARGO DOSPUNTOS MARKETING_DEVOPS
               | CARGO DOSPUNTOS DB_ADMIN'''
    p[0] = {"cargo": p[3]}
    print("[DEBUG] Entrando a cargo_nt")

def p_proyectos_nt(p):
    'proyectos_nt : PROYECTOS DOSPUNTOS ICORCHETE proyecto_list_nt DCORCHETE'
    p[0] = {"proyectos": p[4]}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write("<h2>Proyectos</h2>\n")
        for proyecto in p[4]:
            f.write(f"<div class='proyecto'><h3>{proyecto.get('nombre','')}</h3><ul>")
            for k, v in proyecto.items():
                if k in ("nombre", "tareas"):
                    continue
                if k == "video":
                    f.write(f'<li>Video: <a href="{v}" target="_blank">{v}</a></li>')
                else:
                    f.write(f"<li>{k.title()}: {v}</li>")
            f.write("</ul>")
            # Tareas como tabla
            tareas = proyecto.get("tareas", [])
            if tareas and isinstance(tareas, list) and len(tareas) > 0 and isinstance(tareas[0], dict):
                f.write("<table>")
                headers = tareas[0].keys()
                f.write("<tr>" + "".join(f"<th>{h.title()}</th>" for h in headers) + "</tr>")
                for tarea in tareas:
                    f.write("<tr>" + "".join(f"<td>{tarea.get(h,'')}</td>" for h in headers) + "</tr>")
                f.write("</table>")
            f.write("</div>\n")
    print("[DEBUG] Entrando a proyectos_nt")

def p_proyecto_list_nt(p):
    '''proyecto_list_nt : proyecto_nt COMA proyecto_list_nt
                       | proyecto_nt
                       | '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []
    print("[DEBUG] Entrando a proyecto_list_nt")

def p_proyecto_nt(p):
    'proyecto_nt : ILLAVE proyecto_atributos_nt DLLAVE'
    p[0] = p[2]
    print("[DEBUG] Entrando a proyecto_nt")

def p_proyecto_atributos_nt(p):
    'proyecto_atributos_nt : NOMBRE DOSPUNTOS STRING COMA estado_kv COMA RESUMEN DOSPUNTOS STRING COMA tareas_nt COMA FECHA_INICIO DOSPUNTOS DATE COMA FECHA_FIN DOSPUNTOS DATE COMA VIDEO DOSPUNTOS URL COMA CONCLUSION DOSPUNTOS STRING'
    p[0] = {
        "nombre": p[3],
        "estado": p[5]["estado"],
        "resumen": p[8],
        "tareas": p[10],
        "fecha_inicio": p[13],
        "fecha_fin": p[16],
        "video": p[19],
        "conclusion": p[22]
    }
    print("[DEBUG] Entrando a proyecto_atributos_nt")

def p_tareas_nt(p):
    'tareas_nt : TAREAS DOSPUNTOS ICORCHETE tarea_list_nt DCORCHETE'
    p[0] = p[4]
    print("[DEBUG] Entrando a tareas_nt")

def p_tarea_list_nt(p):
    '''tarea_list_nt : tarea_nt COMA tarea_list_nt
                    | tarea_nt
                    | '''
    if len(p) == 4:
        p[0] = [p[1]] + p[3]
    elif len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = []
    print("[DEBUG] Entrando a tarea_list_nt")

def p_tarea_nt(p):
    'tarea_nt : ILLAVE tarea_atributos_nt DLLAVE'
    p[0] = p[2]
    print("[DEBUG] Entrando a tarea_nt")

def p_tarea_atributos_nt(p):
    '''tarea_atributos_nt : tarea_atributo_list_nt'''
    tarea = {}
    for item in p[1]:
        if isinstance(item, dict):
            tarea.update(item)
        else:
            raise Exception(f"Elemento inválido en atributos de tarea: {item}")
    obligatorios = {"nombre", "estado", "resumen"}
    if not obligatorios.issubset(tarea.keys()):
        raise Exception("Faltan campos obligatorios en Tarea (nombre, estado, resumen)")
    p[0] = tarea
    print("[DEBUG] Entrando a tarea_atributos_nt")

def p_tarea_atributo_list_nt(p):
    '''tarea_atributo_list_nt : tarea_atributo COMA tarea_atributo_list_nt
                              | tarea_atributo'''
    if len(p) == 4:
        return_list = [p[1]] + p[3]
    else:
        return_list = [p[1]]
    p[0] = return_list

def p_tarea_atributo(p):
    '''tarea_atributo : NOMBRE DOSPUNTOS STRING
                      | estado_kv
                      | RESUMEN DOSPUNTOS STRING
                      | FECHA_INICIO DOSPUNTOS DATE
                      | FECHA_INICIO DOSPUNTOS NULL
                      | FECHA_FIN DOSPUNTOS DATE
                      | FECHA_FIN DOSPUNTOS NULL'''
    key = str(p[1]).strip('"').lower()
    if len(p) == 4 and key == "nombre":
        p[0] = {"nombre": p[3]}
    elif len(p) == 4 and key == "resumen":
        p[0] = {"resumen": p[3]}
    elif len(p) == 4 and key == "fecha_inicio":
        p[0] = {"fecha_inicio": p[3]}
    elif len(p) == 4 and key == "fecha_fin":
        p[0] = {"fecha_fin": p[3]}
    elif isinstance(p[1], dict):  # estado_kv
        p[0] = p[1]
    else:
        raise Exception(f"Elemento inválido en tarea_atributo: {p[1]}")

def p_estado_kv(p):
    'estado_kv : ESTADO DOSPUNTOS estado_val'
    p[0] = {"estado": p[3]}

def p_estado_val(p):
    '''estado_val : TO_DO
                  | INPROGRESS
                  | CANCELED
                  | DONE
                  | ON_HOLD'''
    p[0] = p[1]

def p_FIRMA_DIGITALNT(p):
    'FIRMA_DIGITALNT : FIRMA_DIGITAL DOSPUNTOS STRING'
    p[0] = {"firma_digital": p[3]}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write(f'<p><b>Firma digital:</b> {p[3]}</p>\n')
    print("[DEBUG] Entrando a Firma Digital")

def p_VERSIONNT(p):
    'VERSIONNT : VERSION DOSPUNTOS VERSIONE'
    p[0] = {"version": p[3]}
    with open(ruta_completa, 'a', encoding='utf-8') as f:
        f.write(f'<p><b>Versión:</b> {p[3]}</p>\n')
    print("[DEBUG] Entrando a VERSION")

def p_error(p):
    if p:
        try:
            pos = p.lexpos
        except Exception:
            pos = '?'
        msg = f"[DEBUG] Error de sintaxis en '{p.value}'"
        if hasattr(p.lexer, 'lexdata'):
            data = p.lexer.lexdata
            line = data.count('\n', 0, pos) + 1
            col = pos - data.rfind('\n', 0, pos)
            msg += f" en posición {pos} (línea {line}, columna {col})"
            lines = data.split('\n')
            if 0 < line <= len(lines):
                msg += f"\n{lines[line-1]}"
                msg += "\n" + " " * (col-1) + "^"
        print(msg)
    else:
        print("[DEBUG] Error de sintaxis al final de la entrada.")

parser = yacc.yacc()

# --- Ejemplo de uso ---
if __name__ == "__main__":
    # Cambia "entrada.json" por tu archivo de entrada
    archivo_json = "entrada.json"
    iniciar_html("salida.html")
    with open(archivo_json, "r", encoding="utf-8") as f:
        texto = f.read()
        parser.parse(texto, lexer=lexer)