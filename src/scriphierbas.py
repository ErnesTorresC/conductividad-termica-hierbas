import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==========================================
# DETECCIÓN AUTOMÁTICA DE ARCHIVOS EN LA CARPETA
# ==========================================
ruta_script = os.path.dirname(os.path.abspath(__file__))
archivos_en_carpeta = os.listdir(ruta_script)

print(f"Buscando archivos de Excel en: {ruta_script}\n")

# Buscar archivos .xlsx usando coincidencias aproximadas
archivo1_name = next((f for f in archivos_en_carpeta if "PerejilPrueba" in f and f.endswith('.xlsx')), None)
archivo2_name = next((f for f in archivos_en_carpeta if "Perejil.1" in f and f.endswith('.xlsx')), None)

# ==========================================
# 1. PARÁMETROS FÍSICOS DEL PROTOTIPO
# ==========================================
A_cm2 = 38.704       
dx_cm = 0.552        
I_max = 0.088        
V_operacion = 127.0  

A_m2 = A_cm2 / 10000.0  
dx_m = dx_cm / 100.0    

# ==========================================
# 2. PROCESAMIENTO DE LA PRUEBA 1 (Estado Estacionario)
# ==========================================
if archivo1_name:
    print(f"-> Encontrado archivo de Excel para Prueba 1: '{archivo1_name}'")
    archivo1 = os.path.join(ruta_script, archivo1_name)
    # Leemos el archivo de Excel. Si tiene varias hojas, leerá la primera por defecto.
    df1 = pd.read_excel(archivo1)
else:
    print("X No se encontró ningún archivo Excel (.xlsx) que contenga 'PerejilPrueba'")
    df1 = None

if df1 is not None:
    df1['Temperatura Inicial'] = pd.to_numeric(df1['Temperatura Inicial'], errors='coerce')
    df1['Temperatura Final'] = pd.to_numeric(df1['Temperatura Final'], errors='coerce')
    
    # Filtrado de ruido / Outliers
    df1_clean = df1[(df1['Temperatura Inicial'] > 20) & (df1['Temperatura Final'] < 40)].copy()
    
    df1_clean['I_real'] = I_max * (df1_clean['Corriente'] / 100.0)
    df1_clean['Q_W'] = df1_clean['Voltaje'] * df1_clean['I_real']
    df1_clean['dT'] = df1_clean['Temperatura Inicial'] - df1_clean['Temperatura Final']
    df1_clean['k'] = (df1_clean['Q_W'] * dx_m) / (A_m2 * df1_clean['dT'])
    
    Q1_promedio = df1_clean['Q_W'].mean()
    dT1_promedio = df1_clean['dT'].mean()
    k1_promedio = df1_clean['k'].mean()
    k1_desviacion = df1_clean['k'].std()
    
    print("\n--- RESULTADOS PRUEBA 1 (ESTADO ESTACIONARIO) ---")
    print(f"Potencia térmica inyectada (q): {Q1_promedio:.3f} W")
    print(f"Diferencia de temperatura promedio (ΔT): {dT1_promedio:.2f} °C")
    print(f"Conductividad Térmica del Perejil (k): {k1_promedio:.4f} W/(m·°C)")
    print(f"Desviación Estándar de k: {k1_desviacion:.4f} W/(m·°C)")
    
    plt.figure(figsize=(10, 5))
    plt.plot(df1_clean['Hora'].astype(str), df1_clean['Temperatura Inicial'], label='T_caliente (Cara Superior)', color='#d9534f', linewidth=2)
    plt.plot(df1_clean['Hora'].astype(str), df1_clean['Temperatura Final'], label='T_fría (Cara Inferior)', color='#0275d8', linewidth=2)
    
    plt.title('Comportamiento Térmico del Perejil Deshidratado en Estado Estacionario', fontsize=12, fontweight='bold')
    plt.xlabel('Tiempo (Hora)', fontsize=10)
    plt.ylabel('Temperatura (°C)', fontsize=10)
    
    paso = max(1, len(df1_clean) // 6)
    plt.xticks(df1_clean['Hora'].astype(str).values[::paso], rotation=15)
    
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='center right')
    plt.tight_layout()
    
    ruta_grafica = os.path.join(ruta_script, 'Grafica_Conductividad_Perejil.png')
    plt.savefig(ruta_grafica, dpi=300)
    print(f"\nGráfica guardada exitosamente en: {ruta_grafica}")
    plt.show()

# ==========================================
# 3. PROCESAMIENTO DE LA PRUEBA 2 (Datos Transitorios)
# ==========================================
print("\n-------------------------------------------")
if archivo2_name:
    print(f"-> Encontrado archivo de Excel para Prueba 2: '{archivo2_name}'")
    archivo2 = os.path.join(ruta_script, archivo2_name)
    
    # Especificamos que busque la hoja llamada 'Datos' que viene en tus archivos de LabVIEW
    try:
        df2 = pd.read_excel(archivo2, sheet_name='Datos')
    except Exception:
        # Si por algo no se llama así la hoja, lee la primera disponible
        df2 = pd.read_excel(archivo2)
else:
    print("X No se encontró ningún archivo Excel (.xlsx) que contenga 'Perejil.1'")
    df2 = None

if df2 is not None:
    df2['Temperatura Inicial'] = pd.to_numeric(df2['Temperatura Inicial'], errors='coerce')
    df2['Temperatura Final'] = pd.to_numeric(df2['Temperatura Final'], errors='coerce')
    
    df2_clean = df2.dropna(subset=['Temperatura Inicial', 'Temperatura Final']).copy()
    df2_clean = df2_clean[(df2_clean['Temperatura Inicial'] > 5) & (df2_clean['Temperatura Final'] >= 0)].copy()
    
    df2_clean['I_real'] = I_max * (df2_clean['Corriente'] / 100.0)
    df2_clean['Q_W'] = df2_clean['Voltaje'] * df2_clean['I_real']
    df2_clean['dT'] = df2_clean['Temperatura Inicial'] - df2_clean['Temperatura Final']
    
    print("\nPrimeras líneas limpias de la fase transitoria:")
    print(df2_clean[['Hora', 'Temperatura Inicial', 'Temperatura Final', 'Corriente', 'dT']].head())

if not archivo1_name and not archivo2_name:
    print("\n[!] Archivos actuales detectados en la carpeta:")
    for f in archivos_en_carpeta:
        print(f" - {f}")