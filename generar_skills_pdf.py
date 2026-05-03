from fpdf import FPDF
import datetime

# ─── Datos de Skills ─────────────────────────────────────────────────────────
skills = {
    "🔬 Data Science & Machine Learning": [
        ("data-analysis",
         "Análisis de archivos Excel/CSV. Genera estadísticas, resúmenes, tablas pivot, "
         "filtros y exportación a CSV/JSON/Markdown. Soporta múltiples hojas de Excel."),
        ("data-analysis-jupyter",
         "Guía experta para análisis de datos y visualización en Jupyter Notebooks usando "
         "pandas, matplotlib, seaborn y numpy."),
        ("machine-learning",
         "Desarrollo de modelos de ML: entrenamiento, evaluación, pipelines y patrones "
         "de programación funcional con JAX y scikit-learn."),
        ("statistics-math",
         "Estadística, probabilidad, álgebra lineal y fundamentos matemáticos para "
         "ciencia de datos."),
        ("pandas-data-analysis",
         "Manipulación avanzada de DataFrames con pandas: filtros, agrupaciones, "
         "joins, limpieza de datos y análisis exploratorio."),
        ("time-series-analysis",
         "Análisis de series temporales: tendencias, estacionalidad, autocorrelación, "
         "descomposición y modelos de forecasting."),
        ("read-file",
         "Leer cualquier archivo de datos: CSV, JSON, Parquet, Avro, Excel, SQLite o "
         "URLs remotas (S3, HTTPS). Incluye vista previa y perfil del dataset."),
        ("xlsx",
         "Abrir, leer, editar y crear archivos Excel (.xlsx/.csv/.tsv). Ideal para "
         "agregar columnas, calcular fórmulas, formatear, graficar y limpiar datos."),
    ],
    "🐛 Calidad de Código & Testing": [
        ("systematic-debugging",
         "Depuración sistemática ante cualquier bug, fallo de test o comportamiento "
         "inesperado, antes de proponer soluciones."),
        ("python-testing-patterns",
         "Implementación de estrategias de testing con pytest, fixtures, mocking y "
         "desarrollo guiado por pruebas (TDD)."),
        ("clean-code",
         "Transforma código funcional en código limpio siguiendo los principios de "
         'Robert C. Martin ("Uncle Bob").'),
        ("requesting-code-review",
         "Verifica que el trabajo cumple requisitos y está listo para revisión o merge. "
         "Úsala al completar tareas o implementar funcionalidades importantes."),
    ],
    "🌐 Desarrollo Web": [
        ("vercel-react-best-practices",
         "Guías de optimización de rendimiento para React y Next.js desde Vercel Engineering. "
         "Patrones de componentes, data fetching y optimización de bundle."),
        ("nextjs-app-router-patterns",
         "Patrones avanzados de Next.js 14+ App Router con Server Components, streaming, "
         "parallel routes y data fetching optimizado."),
        ("tailwind-design-system",
         "Construcción de sistemas de diseño escalables con Tailwind CSS v4, tokens de "
         "diseño, librerías de componentes y layouts responsivos."),
        ("web-design-guidelines",
         "Auditoría de interfaces web: accesibilidad, UX, diseño responsivo y cumplimiento "
         "de mejores prácticas."),
        ("api-design-principles",
         "Diseño de APIs REST y GraphQL intuitivas, escalables y mantenibles siguiendo "
         "principios modernos de arquitectura."),
    ],
    "🤖 IA & Prompts": [
        ("prompt-engineering-patterns",
         "Técnicas avanzadas de prompt engineering para maximizar rendimiento, "
         "confiabilidad y controlabilidad de LLMs en producción."),
        ("paper-context-resolver",
         "Helper especializado para reproducción de papers de AI/ML. Resuelve detalles "
         "críticos como splits de dataset, protocolos de evaluación y checkpoints."),
        ("sequential-thinking",
         "Razonamiento paso a paso para problemas complejos que requieren análisis "
         "multi-etapa, planificación o descomposición de tareas con alcance dinámico."),
    ],
    "📝 Documentación & Escritura": [
        ("documentation-writer",
         "Escritura técnica experta siguiendo el framework Diátaxis. Crea tutoriales, "
         "guías prácticas, referencias y explicaciones de alta calidad."),
    ],
    "🔧 Productividad & Git": [
        ("git-commit",
         "Ejecuta git commit con análisis de mensajes convencionales, staging inteligente "
         "y generación automática del mensaje desde el diff."),
        ("find-skills",
         "Descubre e instala skills del ecosistema abierto de agentes. Busca por "
         "dominio, tarea o capacidad deseada."),
    ],
    "⚡ Optimización de Tokens & Contexto": [
        ("token-optimizer",
         "Reduce el uso de tokens y costos de API mediante routing inteligente de modelos, "
         "optimización de heartbeat, seguimiento de presupuesto y gestión de sesiones."),
        ("context-window-management",
         "Estrategias para gestionar ventanas de contexto en LLMs: resumen, recorte, "
         "routing y prevención de degradación del contexto."),
        ("compress-prompt",
         "Comprime prompts manteniendo el contenido semántico. Modo lossy (reducción "
         "30-50%) y modo lossless (retención 100%)."),
        ("token-efficiency",
         "Comunicación comprimida usando símbolos y abreviaciones. Ideal cuando el "
         "contexto es limitado o se necesita brevedad máxima."),
    ],
}

# ─── PDF ─────────────────────────────────────────────────────────────────────
class PDF(FPDF):
    def header(self):
        self.set_fill_color(15, 23, 42)       # azul oscuro
        self.rect(0, 0, 210, 30, 'F')
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(255, 255, 255)
        self.set_y(8)
        self.cell(0, 8, "Catalogo de Skills - Agente IA", align="C", new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(148, 163, 184)
        fecha = datetime.datetime.now().strftime("%d/%m/%Y")
        self.cell(0, 6, f"Generado el {fecha}  |  27 skills instaladas", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 10, f"Pagina {self.page_no()}", align="C")

    def section_title(self, title):
        self.ln(3)
        self.set_fill_color(30, 41, 59)
        self.set_text_color(99, 179, 237)
        self.set_font("Helvetica", "B", 11)
        # strip emoji for PDF (basic fonts don't support emoji)
        clean = title.encode('ascii', 'ignore').decode('ascii').strip()
        self.cell(0, 9, clean, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def skill_row(self, name, desc, even):
        bg = (241, 245, 249) if even else (255, 255, 255)
        self.set_fill_color(*bg)

        # Calcular altura necesaria para descripción
        desc_lines = self.get_string_width(desc) / 130
        row_h = max(14, int(desc_lines) * 5 + 14)

        x = self.get_x()
        y = self.get_y()

        # Columna nombre
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(30, 64, 175)
        self.set_fill_color(*bg)
        self.multi_cell(55, 5, name, fill=True, new_x="RIGHT", new_y="TOP", max_line_height=5)

        # Columna descripción
        self.set_xy(x + 57, y)
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(51, 65, 85)
        self.multi_cell(130, 5, desc, fill=True, new_x="LMARGIN", new_y="NEXT", max_line_height=5)

        # Separador
        self.set_draw_color(226, 232, 240)
        self.line(10, self.get_y(), 200, self.get_y())

pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_page()
pdf.set_left_margin(10)
pdf.set_right_margin(10)

# Encabezado de columnas
pdf.set_fill_color(51, 65, 85)
pdf.set_text_color(255, 255, 255)
pdf.set_font("Helvetica", "B", 9)
pdf.cell(55, 7, "SKILL", fill=True)
pdf.cell(2, 7, "")
pdf.cell(130, 7, "FUNCION / DESCRIPCION", fill=True, new_x="LMARGIN", new_y="NEXT")
pdf.ln(1)

# Contenido
for categoria, items in skills.items():
    pdf.section_title(categoria)
    for i, (nombre, descripcion) in enumerate(items):
        pdf.skill_row(nombre, descripcion, i % 2 == 0)
    pdf.ln(2)

# Resumen final
pdf.ln(4)
pdf.set_fill_color(240, 253, 244)
pdf.set_text_color(22, 101, 52)
pdf.set_font("Helvetica", "B", 10)
pdf.cell(0, 8, "  Total: 27 skills instaladas globalmente", fill=True, new_x="LMARGIN", new_y="NEXT")

output_path = r"c:\Users\Danny\Documents\FORECASTINGVENTAS\mis_skills.pdf"
pdf.output(output_path)
print(f"PDF generado exitosamente: {output_path}")
