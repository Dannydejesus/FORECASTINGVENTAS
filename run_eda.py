import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load and merge data
path_ventas = 'data/raw/entrenamiento/ventas.csv'
path_competencia = 'data/raw/entrenamiento/competencia.csv'
df_ventas = pd.read_csv(path_ventas, parse_dates=['fecha'])
df_competencia = pd.read_csv(path_competencia, parse_dates=['fecha'])
df_merged = pd.merge(df_ventas, df_competencia, on=['fecha', 'producto_id'], how='inner')

os.makedirs('docs/graficos', exist_ok=True)
sns.set_theme(style="darkgrid", palette="husl")

# CELDA 1
df_ts = df_merged.groupby('fecha')['unidades_vendidas'].sum().reset_index()
df_ts['año'] = df_ts['fecha'].dt.year

plt.figure(figsize=(14, 6))
sns.lineplot(data=df_ts, x='fecha', y='unidades_vendidas', hue='año', palette='husl')

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
plt.savefig('docs/graficos/01_series_temporales_anio.png')
plt.close()

# CELDA 2
plt.figure(figsize=(14, 6))
df_merged['dia_semana'] = df_merged['fecha'].dt.day_name()
orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_dia = df_merged.groupby('dia_semana')['unidades_vendidas'].sum().reindex(orden_dias).reset_index()
sns.barplot(data=df_dia, x='dia_semana', y='unidades_vendidas')
plt.title('Suma de Unidades Vendidas por Día de la Semana')
plt.xlabel('Día de la Semana')
plt.ylabel('Unidades Vendidas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('docs/graficos/02_ventas_dia_semana.png')
plt.close()

# CELDA 3
plt.figure(figsize=(14, 6))
df_cat = df_merged.groupby('categoria')['unidades_vendidas'].sum().sort_values(ascending=False).reset_index()
sns.barplot(data=df_cat, y='categoria', x='unidades_vendidas', orient='h')
plt.title('Suma de Unidades Vendidas por Categoría')
plt.xlabel('Unidades Vendidas')
plt.ylabel('Categoría')
plt.tight_layout()
plt.savefig('docs/graficos/03_ventas_categoria.png')
plt.close()

# CELDA 4
plt.figure(figsize=(14, 6))
df_subcat = df_merged.groupby('subcategoria')['unidades_vendidas'].sum().sort_values(ascending=False).head(15).reset_index()
sns.barplot(data=df_subcat, y='subcategoria', x='unidades_vendidas', orient='h')
plt.title('Top 15 Subcategorías por Suma de Unidades Vendidas')
plt.xlabel('Unidades Vendidas')
plt.ylabel('Subcategoría')
plt.tight_layout()
plt.savefig('docs/graficos/04_ventas_subcategoria.png')
plt.close()

# CELDA 5
plt.figure(figsize=(14, 6))
df_prod = df_merged.groupby('nombre')['unidades_vendidas'].sum().sort_values(ascending=False).head(20).reset_index()
sns.barplot(data=df_prod, y='nombre', x='unidades_vendidas', orient='h')
plt.title('Top 20 Productos por Suma de Unidades Vendidas')
plt.xlabel('Unidades Vendidas')
plt.ylabel('Producto')
plt.tight_layout()
plt.savefig('docs/graficos/05_top20_productos.png')
plt.close()

# CELDA 6
plt.figure(figsize=(14, 6))
sns.kdeplot(data=df_merged, x='precio_venta', fill=True, label='Precio Propio', color='blue', alpha=0.5)
sns.kdeplot(data=df_merged, x='Amazon', fill=True, label='Precio Amazon', color='orange', alpha=0.5)
plt.title('Densidad de Precios: Propio vs Amazon')
plt.xlabel('Precio')
plt.ylabel('Densidad')
plt.legend()
plt.tight_layout()
plt.savefig('docs/graficos/06_densidad_precios.png')
plt.close()
