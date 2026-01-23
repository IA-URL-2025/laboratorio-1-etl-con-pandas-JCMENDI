import pandas as pd
import numpy 

def run_etl():
    """
    Implementa el proceso ETL.
    No cambies el nombre de esta función.
    """
    # 1. Extract: Leer el archivo CSV
    try:
        df = pd.read_csv('data/citas_clinica.csv')
    except FileNotFoundError:
        print("Error: El archivo no se econtró")
        return

    #2. Transform: Aplicacion de reglas de limpieza
    # Normalización de texto: paciente en Title Case 
    df['paciente'] = df['paciente'].str.title()
    
    # Normalización de texto: especialidad en UPPERCASE 
    df['especialidad'] = df['especialidad'].str.upper()
    
    # Manejo de Fechas: Convertir y filtrar inválidas ]
    df['fecha_cita'] = pd.to_datetime(df['fecha_cita'], errors='coerce')
    df = df.dropna(subset=['fecha_cita'])
    
    # Reglas de negocio: Reemplazar teléfonos nulos 
    # Se hace antes de eliminar nulos generales para conservar la fila
    df['telefono'] = df['telefono'].fillna('NO REGISTRA')
    
    # Reglas de negocio: Eliminar filas por condiciones 
    # Conservar solo estado "CONFIRMADA" [cite: 50]
    df = df[df['estado'] == 'CONFIRMADA']
    
    # Conservar solo costo mayor a 0 [cite: 51]
    df = df[df['costo'] > 0]
    
    # Eliminar filas que aún contengan valores nulos 
    df = df.dropna()

    # 3. Load: Guardar el resultado final [cite: 53]
    # Se genera el archivo de salida en  
    df.to_csv('data/output.csv', index=False)

if __name__ == "__main__":
    run_etl()
