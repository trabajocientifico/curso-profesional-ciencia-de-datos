import pandas as pd
import numpy as np
import re
import unicodedata
from unidecode import unidecode

# ─── 0. Cargar datos ───
datos = pd.read_excel('datos_ventas.xlsx')
print(f"Shape original: {datos.shape}")
print(f"Duplicados: {datos.duplicated().sum()}")

# ─── 1. Eliminar filas duplicadas ───
datos = datos.drop_duplicates().reset_index(drop=True)
print(f"Shape sin duplicados: {datos.shape}")

# ─── 2. Limpiar ciudad y categoria ───
def normalizar_texto(s):
    """Elimina espacios, estandariza mayúsculas y quita acentos/tildes."""
    if pd.isna(s):
        return s
    s = str(s).strip()
    s = s.upper()                 # unificar mayúsculas
    s = unidecode(s)              # quitar acentos (Á -> A, É -> E, ñ -> n, etc.)
    return s

datos['ciudad'] = datos['ciudad'].apply(normalizar_texto)
datos['categoria'] = datos['categoria'].apply(normalizar_texto)

print("\nCiudades únicas tras limpieza:", sorted(datos['ciudad'].unique()))
print("Categorías únicas tras limpieza:", sorted(datos['categoria'].unique()))

# ─── 3. Convertir cantidad, precio_unitario y total_venta a número ───
def limpiar_numero(val):
    """Elimina '$', espacios y puntos de miles, reemplaza coma decimal.
    Devuelve float o NaN."""
    if pd.isna(val):
        return np.nan
    s = str(val).strip()
    # Quitar símbolo $
    s = s.replace('$', '')
    # Quitar espacios
    s = s.strip()
    # Si hay coma como decimal (ej: "1.234,56") -> raro aquí, pero prevenimos
    # En los datos vemos puntos como separador de miles: "295.200" -> 295200
    # Detectar si el punto es decimal o de miles:
    # Si después del último punto hay exactamente 3 dígitos, es miles
    parts = s.split('.')
    if len(parts) > 1:
        # Si el último grupo tiene 3 dígitos, es miles -> quitar puntos
        if len(parts[-1]) == 3:
            s = s.replace('.', '')
        # Si no, podría ser decimal -> reemplazar coma por punto (manejo genérico)
        else:
            s = s.replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return np.nan

# Aplicar limpieza a las columnas numéricas
datos['precio_unitario'] = datos['precio_unitario'].apply(limpiar_numero)
# cantidad: convertir directamente a número (ya es int, pero por si acaso)
datos['cantidad'] = pd.to_numeric(datos['cantidad'], errors='coerce')
# total_venta: limpiar también por si tiene formato moneda (aunque es float)
datos['total_venta'] = datos['total_venta'].apply(limpiar_numero)

print(f"\nMuestras de precio_unitario tras limpieza:\n{datos['precio_unitario'].head(10)}")

# ─── 4. Recalcular total_venta donde falte ───
# total_venta = cantidad × precio_unitario
mascara_falta = datos['total_venta'].isna()
datos.loc[mascara_falta, 'total_venta'] = (
    datos.loc[mascara_falta, 'cantidad'] * datos.loc[mascara_falta, 'precio_unitario']
)
print(f"\ntotal_venta recalculado para {mascara_falta.sum()} filas")

# ─── 5. Eliminar filas con cantidad ≤ 0 ───
antes = len(datos)
datos = datos[datos['cantidad'] > 0].reset_index(drop=True)
print(f"\nFilas eliminadas por cantidad <= 0: {antes - len(datos)}")
print(f"Shape tras eliminar cantidad <= 0: {datos.shape}")

# ─── 6. Rellenar satisfaccion vacía con la mediana ───
mediana_satisfaccion = datos['satisfaccion'].median()
print(f"\nMediana de satisfaccion: {mediana_satisfaccion}")
datos['satisfaccion'] = datos['satisfaccion'].fillna(mediana_satisfaccion)
print(f"Valores nulos restantes en satisfaccion: {datos['satisfaccion'].isna().sum()}")

# ─── Guardar resultado ───
datos.to_excel('datos_ventas_limpio.xlsx', index=False)
print(f"\n✅ Archivo guardado: datos_ventas_limpio.xlsx")
print(f"Shape final: {datos.shape}")
print(f"\nResumen final:\n{datos.describe(include='all')}")
