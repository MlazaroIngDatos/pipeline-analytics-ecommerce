import pandas as pd
import pyodbc

# 1. Ruta exacta de tu archivo en Descargas
ruta_archivo_local = r"D:\2026\Big_Data\Nttdata\Proyecto\Pipeline_Analytics_Ecommerce.csv" 

try:
    df_local = pd.read_csv(ruta_archivo_local)
    print(f"✅ Archivo leido correctamente. Filas cargadas: {len(df_local)}")
except Exception as e:
    print(f"❌ Error al leer el archivo CSV: {e}")
    exit()

# 2. Conexion a tu SQL Server Local
try:
    conn = pyodbc.connect(
        'Driver={ODBC Driver 17 for SQL Server};'
        'Server=.\\SQLEXPRESS02;'  
        'Database=master;'          
        'Trusted_Connection=yes;'
    )
    cursor = conn.cursor()
    print("✅ Conexion establecida con SQL Server.")
except Exception as e:
    print(f"❌ Error de conexion a SQL Server: {e}")
    exit()

# 3. Crear la estructura de la tabla
cursor.execute("""
IF OBJECT_ID('dbo.ReporteVentas', 'U') IS NOT NULL DROP TABLE dbo.ReporteVentas;
CREATE TABLE dbo.ReporteVentas (
    provincia_peru VARCHAR(100),
    categoria VARCHAR(100),
    total_pedidos INT,
    ingresos_totales NUMERIC(12,2),
    ticket_promedio NUMERIC(12,2),
    ultima_actualizacion DATETIME
);
""")
conn.commit()
print("✅ Tabla 'dbo.ReporteVentas' preparada.")

# 4. Insercion de los datos
for index, row in df_local.iterrows():
    cursor.execute("""
        INSERT INTO dbo.ReporteVentas (
            provincia_peru, categoria, total_pedidos, 
            ingresos_totales, ticket_promedio, ultima_actualizacion
        ) VALUES (?, ?, ?, ?, ?, ?)
    """, 
    row['provincia_peru'], 
    row['categoria'], 
    int(row['total_pedidos']), 
    float(row['ingresos_totales']), 
    float(row['ticket_promedio']), 
    row['ultima_actualizacion']
    )

conn.commit()
cursor.close()
conn.close()
print("🎉 ¡Pipeline completado con exito! Datos guardados en tu base de datos.")
