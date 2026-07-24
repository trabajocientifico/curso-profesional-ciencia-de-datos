import pandas as pd
import os

# ─── Cargar datos ───
datos = pd.read_excel('datos_ventas_limpio.xlsx')

# ─── Calcular utilidad por fila ───
datos['utilidad'] = datos['total_venta'] - (datos['costo_unitario'] * datos['cantidad'])

# ═══════════════════════════════════════════════
# (1) Reportes por ciudad
# ═══════════════════════════════════════════════
os.makedirs('reportes_por_ciudad', exist_ok=True)

for ciudad in sorted(datos['ciudad'].unique()):
    df_ciudad = datos[datos['ciudad'] == ciudad].copy()
    nombre_archivo = f"ventas_{ciudad.lower()}.xlsx"
    ruta = os.path.join('reportes_por_ciudad', nombre_archivo)
    df_ciudad.to_excel(ruta, index=False)
    print(f"  {ruta}  ({len(df_ciudad)} filas)")

print("[1/2] Reportes por ciudad generados")

# ═══════════════════════════════════════════════
# (2) Resumen multi-hoja
# ═══════════════════════════════════════════════
ruta_resumen = 'resumen_ventas.xlsx'
with pd.ExcelWriter(ruta_resumen, engine='openpyxl') as writer:

    # --- Una hoja por categoría ---
    for categoria in sorted(datos['categoria'].unique()):
        df_cat = datos[datos['categoria'] == categoria].copy()
        # Nombre corto de hoja (máx 31 caracteres para Excel)
        sheet_name = categoria.capitalize()
        df_cat.to_excel(writer, sheet_name=sheet_name, index=False)
        print(f"  Hoja '{sheet_name}': {len(df_cat)} filas")

    # --- Hoja Resumen con total_venta y utilidad por ciudad ---
    resumen = datos.groupby('ciudad').agg(
        total_venta=('total_venta', 'sum'),
        total_utilidad=('utilidad', 'sum')
    ).reset_index()

    # Agregar fila de total general
    total_row = pd.DataFrame([{
        'ciudad': 'TOTAL',
        'total_venta': resumen['total_venta'].sum(),
        'total_utilidad': resumen['total_utilidad'].sum()
    }])
    resumen = pd.concat([resumen, total_row], ignore_index=True)

    resumen.to_excel(writer, sheet_name='Resumen', index=False)
    print(f"  Hoja 'Resumen': {len(resumen)} filas")

print(f"[2/2] {ruta_resumen} generado")
print("Listo.")
