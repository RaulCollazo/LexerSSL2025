import tkinter as tk
from tkinter import filedialog, messagebox
from Lexer import lexer
from Parser import parser
from html_export import exportar_a_html5
import os
import json

console_output = []
parser_result = None
last_filename = None  # Guardar el nombre del archivo fuente

def analizar_lexer(texto):
    lexer.input(texto)
    resultado = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        resultado.append(f"Token: {tok.value} - Tipo: {tok.type}")
    return "\n".join(resultado)

def analizar_parser(texto):
    global console_output, parser_result
    console_output = []
    parser_result = None
    try:
        import builtins
        import json
        import os

        original_print = print

        def print_to_console(*args, **kwargs):
            message = " ".join(str(a) for a in args)
            console_output.append(message)

        builtins.print = print_to_console

        # Ejecutar parser
        parser_result = parser.parse(texto, lexer=lexer)

        builtins.print = original_print

        # Preparar mensaje de consola
        if console_output:
            resultado_parser = "Parseo exitoso.\n\n" + "\n".join(console_output)
        else:
            resultado_parser = "Parseo exitoso."

        # Mostrar contenido parseado
        resultado_parser += "\n\n[Resultado del Parser]\n"
        resultado_parser += json.dumps(parser_result, indent=2, ensure_ascii=False)

        # Función para limpiar comillas dobles de strings
        def limpiar_parser_result(data):
            if isinstance(data, dict):
                return {k: limpiar_parser_result(v) for k, v in data.items()}
            elif isinstance(data, list):
                return [limpiar_parser_result(elem) for elem in data]
            elif isinstance(data, str):
                return data.strip('"')
            else:
                return data

        # Limpiar el resultado antes de guardar
        parser_result_limpio = limpiar_parser_result(parser_result)

        # Ruta de guardado junto a main.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        output_path = os.path.join(script_dir, "salida_parser.json")

        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(parser_result_limpio, f, indent=2, ensure_ascii=False)
            print(f"✅ Diccionario guardado en: {output_path}")
        except Exception as json_err:
            print(f"❌ Error al guardar JSON: {json_err}")
            print("Contenido del parser (fallido):", parser_result)

        return resultado_parser

    except Exception as e:
        builtins.print = __builtins__.print
        return f"Error: {e}"

def analizar_archivo():
    global last_filename
    archivo = filedialog.askopenfilename(filetypes=[('Archivos JSON', '*.json'), ('Todos los archivos', '*.*')])
    if archivo:
        last_filename = archivo
        with open(archivo, 'r', encoding='utf-8') as f:
            texto = f.read()
        txt_entrada.delete('1.0', tk.END)
        txt_entrada.insert(tk.END, texto)

def ejecutar_lexer():
    texto = txt_entrada.get("1.0", tk.END)
    resultado = analizar_lexer(texto)
    txt_salida.config(state=tk.NORMAL)
    txt_salida.delete("1.0", tk.END)
    txt_salida.insert(tk.END, resultado)
    txt_salida.config(state=tk.DISABLED)

def ejecutar_parser():
    texto = txt_entrada.get("1.0", tk.END)
    resultado = analizar_parser(texto)
    txt_salida.config(state=tk.NORMAL)
    txt_salida.delete("1.0", tk.END)
    txt_salida.insert(tk.END, resultado)
    txt_salida.config(state=tk.DISABLED)

def exportar_html():
    global parser_result, last_filename
    if not parser_result:
        messagebox.showerror("Error", "Debes analizar la sintaxis antes de exportar.")
        return
    # --- CORRECCIÓN: Forzar dict si es string ---
    data = parser_result
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo convertir el resultado del parser a dict: {e}")
            return
    if last_filename:
        base = os.path.splitext(os.path.basename(last_filename))[0]
        archivo_html = filedialog.asksaveasfilename(
            defaultextension=".html",
            initialfile=base + ".html",
            filetypes=[('Archivo HTML', '*.html'), ('Todos los archivos', '*.*')]
        )
    else:
        archivo_html = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[('Archivo HTML', '*.html'), ('Todos los archivos', '*.*')]
        )
    if archivo_html:
        try:
            exportar_a_html5(data, archivo_html)
            messagebox.showinfo("Exportado", f"Archivo {archivo_html} generado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar: {e}")

root = tk.Tk()
root.title("Lexer & Parser Demo")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Button(frame, text="Abrir archivo", command=analizar_archivo).pack(side=tk.LEFT)
tk.Button(frame, text="Analizar Léxico", command=ejecutar_lexer).pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Analizar Sintaxis", command=ejecutar_parser).pack(side=tk.LEFT)
tk.Button(frame, text="Exportar a HTML", command=exportar_html).pack(side=tk.LEFT, padx=5)

txt_entrada = tk.Text(root, height=15, width=80)
txt_entrada.pack(padx=10, pady=5)

txt_salida = tk.Text(root, height=10, width=80, state=tk.DISABLED, bg="#222", fg="#0f0")
txt_salida.pack(padx=10, pady=5)

root.mainloop()