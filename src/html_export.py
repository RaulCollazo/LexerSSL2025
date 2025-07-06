import os
import json

def exportar_a_html5(data, nombre_archivo=None):
    def html_escape(text):
        return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    # --- CORRECCIÓN: Intenta convertir a dict si viene como string ---
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception:
            data = {"nombre_equipo": str(data)}

    # Si no se especifica el nombre, toma el del JSON y cambia .json por .html
    if not nombre_archivo:
        if isinstance(data, dict) and data.get("_origen_json"):
            nombre_archivo = os.path.splitext(data["_origen_json"])[0] + ".html"
        else:
            nombre_archivo = "output.html"

    html = [
        '<!DOCTYPE html>',
        '<html lang="es">',
        '<head>',
        '  <meta charset="UTF-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f'  <title>{html_escape(data.get("nombre_equipo", "Equipos")) if isinstance(data, dict) else "Equipos"}</title>',
        '  <style>',
        '    .equipo { border: 1px solid gray; padding: 20px; margin-bottom: 30px; }',
        '    .integrante, .proyecto { margin-left: 20px; }',
        '    table { border-collapse: collapse; margin: 10px 0; }',
        '    table, th, td { border: 1px solid #aaa; padding: 4px; }',
        '  </style>',
        '</head>',
        '<body>'
    ]

    # Normalización de entrada
    equipos = []
    if isinstance(data, dict):
        if "equipos" in data:
            equipos = data["equipos"]
        else:
            equipos = [data]
    elif isinstance(data, list):
        equipos = data
    else:
        equipos = [{"nombre_equipo": str(data)}]

    for equipo in equipos:
        if not isinstance(equipo, dict):
            equipo = {"nombre_equipo": str(equipo)}
        html.append('<div class="equipo">')
        html.append(f"<h1>{html_escape(equipo.get('nombre_equipo', 'Equipo'))}</h1>")

        # Otros campos del equipo
        for key, value in equipo.items():
            if key in ("nombre_equipo", "integrantes", "proyectos"):
                continue
            if key == "link":
                html.append(f'<p>Link: <a href="{html_escape(value)}" target="_blank">{html_escape(value)}</a></p>')
            elif key == "direccion" and isinstance(value, dict):
                # Mostrar dirección en un solo <p>
                dir_str = ", ".join(f"{k.title()}: {v}" for k, v in value.items())
                html.append(f"<p>Dirección: {html_escape(dir_str)}</p>")
            else:
                html.append(f"<p>{html_escape(key.title())}: {html_escape(value)}</p>")

        # Integrantes
        integrantes = equipo.get("integrantes", [])
        if isinstance(integrantes, dict):
            integrantes = [integrantes]
        if integrantes and isinstance(integrantes, list):
            html.append("<h2>Integrantes</h2><ul>")
            for integrante in integrantes:
                if not isinstance(integrante, dict):
                    continue
                nombre = integrante.get("nombre", "Sin nombre")
                html.append(f"<li><b>{html_escape(nombre)}</b><ul>")
                for k, v in integrante.items():
                    if k == "nombre":
                        continue
                    if k == "foto":
                        html.append(f'<li>Foto: <a href="{html_escape(v)}" target="_blank">{html_escape(v)}</a></li>')
                    elif k == "email":
                        html.append(f'<li>Email: <a href="mailto:{html_escape(v)}">{html_escape(v)}</a></li>')
                    else:
                        html.append(f"<li>{html_escape(k.title())}: {html_escape(v)}</li>")
                html.append("</ul></li>")
            html.append("</ul>")

        # Proyectos
        proyectos = equipo.get("proyectos", [])
        if isinstance(proyectos, dict):
            proyectos = [proyectos]
        if proyectos and isinstance(proyectos, list):
            html.append("<h2>Proyectos</h2>")
            for proyecto in proyectos:
                if not isinstance(proyecto, dict):
                    continue
                nombre = proyecto.get("nombre", "Proyecto")
                html.append(f"<h3>{html_escape(nombre)}</h3><ul>")
                for k, v in proyecto.items():
                    if k in ("nombre", "tareas"):
                        continue
                    if k == "video":
                        html.append(f'<li>Video: <a href="{html_escape(v)}" target="_blank">{html_escape(v)}</a></li>')
                    else:
                        html.append(f"<li>{html_escape(k.title())}: {html_escape(v)}</li>")
                html.append("</ul>")

                # Tareas como tabla
                tareas = proyecto.get("tareas", [])
                if isinstance(tareas, dict):
                    tareas = [tareas]
                if tareas and isinstance(tareas, list) and len(tareas) > 0 and isinstance(tareas[0], dict):
                    html.append("<table>")
                    headers = tareas[0].keys()
                    html.append("<tr>" + "".join(f"<th>{html_escape(h.title())}</th>" for h in headers) + "</tr>")
                    for tarea in tareas:
                        html.append("<tr>" + "".join(f"<td>{html_escape(tarea.get(h,''))}</td>" for h in headers) + "</tr>")
                    html.append("</table>")
        html.append('</div>')

    html.append('</body></html>')

    with open(nombre_archivo, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"Archivo HTML generado: {nombre_archivo}")