import json

notebook_path = r'c:\Users\Danny\Documents\FORECASTINGVENTAS\notebooks\entrenamiento.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Cell 1
code1 = """# CELDA 1: Series temporales por año
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Crear directorio si no existe
os.makedirs('../docs/graficos', exist_ok=True)

# Configuración general
sns.set_theme(style="darkgrid", palette="husl")

# Agrupar datos por fecha
df_ts = df_merged.groupby('fecha')['unidades_vendidas'].sum().reset_index()
df_ts['año'] = df_ts['fecha'].dt.year

plt.figure(figsize=(14, 6))
sns.lineplot(data=df_ts, x='fecha', y='unidades_vendidas', hue='año', palette='husl')

# Black Friday (4to viernes de noviembre)
years = df_ts['año'].unique()
for y in years:
    nov = pd.date_range(start=f'{y}-11-01', end=f'{y}-11-30')
    fridays = nov[nov.weekday == 4]
    if len(fridays) >= 4:
        bf_date = fridays[3]
        plt.axvline(bf_date, color='red', linestyle='--', alpha=0.7, label=f'Black Friday {y}' if y == years[0] else '_nolegend_')

plt.title('Ventas Diarias por Año con Marcas de Black Friday')
plt.xlabel('Fecha')
plt.ylabel('Unidades Vendidas')
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig('../docs/graficos/01_series_temporales_anio.png')
plt.show()"""

# Cell 2
code2 = """# CELDA 2: Ventas por día de la semana
plt.figure(figsize=(14, 6))
sns.set_theme(style="darkgrid", palette="husl")

df_merged['dia_semana'] = df_merged['fecha'].dt.day_name()
orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_dia = df_merged.groupby('dia_semana')['unidades_vendidas'].sum().reindex(orden_dias).reset_index()

sns.barplot(data=df_dia, x='dia_semana', y='unidades_vendidas')
plt.title('Suma de Unidades Vendidas por Día de la Semana')
plt.xlabel('Día de la Semana')
plt.ylabel('Unidades Vendidas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('../docs/graficos/02_ventas_dia_semana.png')
plt.show()"""

# Cell 3
code3 = """# CELDA 3: Ventas por categoría
plt.figure(figsize=(14, 6))
sns.set_theme(style="darkgrid", palette="husl")

df_cat = df_merged.groupby('categoria')['unidades_vendidas'].sum().sort_values(ascending=False).reset_index()

sns.barplot(data=df_cat, y='categoria', x='unidades_vendidas', orient='h')
plt.title('Suma de Unidades Vendidas por Categoría')
plt.xlabel('Unidades Vendidas')
plt.ylabel('Categoría')
plt.tight_layout()
plt.savefig('../docs/graficos/03_ventas_categoria.png')
plt.show()"""

# Cell 4
code4 = """# CELDA 4: Ventas por subcategoría (Top 15)
plt.figure(figsize=(14, 6))
sns.set_theme(style="darkgrid", palette="husl")

df_subcat = df_merged.groupby('subcategoria')['unidades_vendidas'].sum().sort_values(ascending=False).head(15).reset_index()

sns.barplot(data=df_subcat, y='subcategoria', x='unidades_vendidas', orient='h')
plt.title('Top 15 Subcategorías por Suma de Unidades Vendidas')
plt.xlabel('Unidades Vendidas')
plt.ylabel('Subcategoría')
plt.tight_layout()
plt.savefig('../docs/graficos/04_ventas_subcategoria.png')
plt.show()"""

# Cell 5
code5 = """# CELDA 5: Top 20 productos
plt.figure(figsize=(14, 6))
sns.set_theme(style="darkgrid", palette="husl")

df_prod = df_merged.groupby('nombre')['unidades_vendidas'].sum().sort_values(ascending=False).head(20).reset_index()

sns.barplot(data=df_prod, y='nombre', x='unidades_vendidas', orient='h')
plt.title('Top 20 Productos por Suma de Unidades Vendidas')
plt.xlabel('Unidades Vendidas')
plt.ylabel('Producto')
plt.tight_layout()
plt.savefig('../docs/graficos/05_top20_productos.png')
plt.show()"""

# Cell 6
code6 = """# CELDA 6: Densidad de precios (Propios vs Amazon)
plt.figure(figsize=(14, 6))
sns.set_theme(style="darkgrid", palette="husl")

sns.kdeplot(data=df_merged, x='precio_venta', fill=True, label='Precio Propio', color='blue', alpha=0.5)
sns.kdeplot(data=df_merged, x='Amazon', fill=True, label='Precio Amazon', color='orange', alpha=0.5)

plt.title('Densidad de Precios: Propio vs Amazon')
plt.xlabel('Precio')
plt.ylabel('Densidad')
plt.legend()
plt.tight_layout()
plt.savefig('../docs/graficos/06_densidad_precios.png')
plt.show()"""

cells_to_add = [code1, code2, code3, code4, code5, code6]

for code in cells_to_add:
    new_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\\n" for line in code.split("\\n")]
    }
    # Fix the last line missing newline if not intended, actually splitlines keep it easier
    new_cell["source"] = [line + "\\n" for line in code.split("\\n")]
    new_cell["source"][-1] = new_cell["source"][-1][:-2] # remove last \\n
    nb['cells'].append(new_cell)

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1)
