import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QDialog, QTextEdit, QVBoxLayout, QFileDialog,
    QMessageBox, QLabel, QInputDialog, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import ply.lex as lex

# === Analizador Léxico ===
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
    '"tarea"': 'TAREA',
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
    if t.value in reserved:
        t.type = reserved[t.value]
        t.value = t.type
    return t

t_ignore = ' \t\n'

def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# === Interfaz Gráfica ===

class EntradaManualDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Entrada Manual")
        self.setMinimumSize(500, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #121212;
            }
            QTextEdit {
                background-color: #1e1e1e;
                color: #e0f7fa;
                font-family: Courier;
                font-size: 12px;
                border: 1px solid #00bcd4;
                border-radius: 6px;
                padding: 8px;
            }
            QPushButton {
                background-color: #323232;
                color: white;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #4a4a4a;
            }
        """)

        layout = QVBoxLayout()
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Aceptar")
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_ok.clicked.connect(self.accept)
        self.btn_cancel.clicked.connect(self.reject)

        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def get_text(self):
        return self.text_edit.toPlainText()

class AnalizadorLexicoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analizador Léxico")
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #202020; color:  #1ec974;")

        layout = QVBoxLayout()

        # Título
        titulo = QLabel("Analizador Léxico")
        subTitulo = QLabel("Grupo X - Nombre en Trámite")
        titulo.setFont(QFont("Arial", 20, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("margin-bottom: 20px;")
        subTitulo.setFont(QFont("Arial", 18, QFont.Bold))
        subTitulo.setAlignment(Qt.AlignCenter)
        subTitulo.setStyleSheet("margin-bottom: 20px; color: #ffffff; ")
        layout.addWidget(titulo)
        layout.addWidget(subTitulo)

       # Layout horizontal para los botones
        botones_layout = QHBoxLayout()

        boton_manual = QPushButton(" Analizar Texto")
        boton_manual.setStyleSheet(self.boton_estilo())
        boton_manual.clicked.connect(self.analizar_manual)
        boton_manual.setFixedSize(180, 60)

        boton_archivo = QPushButton(" Analizar Archivo JSON")
        boton_archivo.setStyleSheet(self.boton_estilo())
        boton_archivo.clicked.connect(self.analizar_archivo)
        boton_archivo.setFixedSize(180, 60)

        boton_salir = QPushButton(" Salir")
        boton_salir.setStyleSheet(self.boton_estilo("#1ec974"))
        boton_salir.clicked.connect(self.close)
        boton_salir.setFixedSize(180, 60)

        # Añadir botones al layout horizontal
        botones_layout.addStretch()
        botones_layout.addWidget(boton_manual)
        botones_layout.addWidget(boton_archivo)
        botones_layout.addWidget(boton_salir)
        botones_layout.addStretch()

        layout.addLayout(botones_layout)


        # Área de resultados
        contenedor_resultado = QWidget()
        contenedor_resultado.setFixedWidth(560)  # 3 botones de 180px
        contenedor_layout = QVBoxLayout()
        contenedor_layout.setContentsMargins(0, 0, 0, 0)

        self.resultado = QLabel()
        self.resultado.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.resultado.setWordWrap(True)
        self.resultado.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.resultado.setStyleSheet("""
            background-color: #ffffff;
            color: #000000;
            padding: 20px;
            font-family: Courier;
            font-size: 12px;
            min-height: 180px;
            border-radius: 8px;
        """)
        self.resultado.setFont(QFont("Courier", 11))

        contenedor_layout.addWidget(self.resultado)
        contenedor_resultado.setLayout(contenedor_layout)

        # Centrar el contenedor en el layout principal
        layout_centrado = QHBoxLayout()
        layout_centrado.addStretch()
        layout_centrado.addWidget(contenedor_resultado)
        layout_centrado.addStretch()

        layout.addLayout(layout_centrado)

        self.setLayout(layout)

    def boton_estilo(self, color="#3c3f41"):
        return f"""
        QPushButton {{
            background-color: {color};
            color: #ffffff;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            border: 1px solid #555;
        }}
        QPushButton:hover {{
            background-color: #505354;
        }}
    """

    def analizar_manual(self):
        dialogo = EntradaManualDialog()
        if dialogo.exec_() == QDialog.Accepted:
            texto = dialogo.get_text()
            if texto:
                resultado = ""
                lexer.input(texto)
                while True:
                    tok = lexer.token()
                    if not tok:
                        break
                    resultado += f"Token: {tok.value} - Tipo: {tok.type}\n"
                self.resultado.setText(resultado)

    def analizar_archivo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo JSON", "", "Archivos JSON (*.json)")
        if archivo:
            try:
                with open(archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    self.resultado.clear()
                    lexer.input(contenido)
                    resultado = ""
                    while True:
                        tok = lexer.token()
                        if not tok:
                            break
                        resultado += f"Token: {tok.value} - Tipo: {tok.type}\n"
                    self.resultado.setText(resultado)
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo leer el archivo:\n{str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AnalizadorLexicoApp()
    ventana.show()
    sys.exit(app.exec_())
