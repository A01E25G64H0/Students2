import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from supabase import create_client
import warnings
import sys
import io

# Configurar codificación para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

warnings.filterwarnings('ignore')

# Configuración de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# Conexión a Supabase
SUPABASE_URL = 'https://yflaeiibqoeslxwpatnn.supabase.co'
SUPABASE_KEY = 'sb_publishable_T_XO4LNuOhnRom787DiryQ_55ruK5Ge'

def cargar_datos():
    """Cargar datos desde Supabase"""
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    response = client.table('students').select('*').execute()
    df = pd.DataFrame(response.data)
    return df

def crear_directorio_output():
    """Crear directorio para guardar gráficas"""
    import os
    if not os.path.exists('graficas'):
        os.makedirs('graficas')
    print("Directorio 'graficas' creado")

def grafica_distribucion_scores(df):
    """Histogramas de distribución de scores"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    scores = ['math_score', 'reading_score', 'writing_score']
    titulos = ['Matemáticas', 'Lectura', 'Escritura']
    colores = ['#0071e3', '#34c759', '#ff9f0a']
    
    for idx, (score, titulo, color) in enumerate(zip(scores, titulos, colores)):
        axes[idx].hist(df[score], bins=20, color=color, alpha=0.7, edgecolor='black')
        axes[idx].axvline(df[score].mean(), color='red', linestyle='--', linewidth=2, label=f'Media: {df[score].mean():.1f}')
        axes[idx].axvline(df[score].median(), color='green', linestyle='--', linewidth=2, label=f'Mediana: {df[score].median():.1f}')
        axes[idx].set_xlabel('Puntaje', fontsize=12)
        axes[idx].set_ylabel('Frecuencia', fontsize=12)
        axes[idx].set_title(f'Distribución de {titulo}', fontsize=14, fontweight='bold')
        axes[idx].legend()
        axes[idx].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('graficas/01_distribucion_scores.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfica 1: Distribución de scores")

def grafica_boxplot_scores(df):
    """Boxplots comparativos de scores"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Por género
    df_melted = df.melt(id_vars=['gender'], value_vars=['math_score', 'reading_score', 'writing_score'], 
                        var_name='Materia', value_name='Score')
    sns.boxplot(data=df_melted, x='gender', y='Score', hue='Materia', ax=axes[0, 0])
    axes[0, 0].set_title('Scores por Género', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Género', fontsize=12)
    axes[0, 0].set_ylabel('Puntaje', fontsize=12)
    axes[0, 0].legend(title='Materia')
    
    # Por lunch
    df_melted = df.melt(id_vars=['lunch'], value_vars=['math_score', 'reading_score', 'writing_score'], 
                        var_name='Materia', value_name='Score')
    sns.boxplot(data=df_melted, x='lunch', y='Score', hue='Materia', ax=axes[0, 1])
    axes[0, 1].set_title('Scores por Tipo de Almuerzo', fontsize=14, fontweight='bold')
    axes[0, 1].set_xlabel('Tipo de Almuerzo', fontsize=12)
    axes[0, 1].set_ylabel('Puntaje', fontsize=12)
    axes[0, 1].legend(title='Materia')
    
    # Por test prep
    df_melted = df.melt(id_vars=['test_prep'], value_vars=['math_score', 'reading_score', 'writing_score'], 
                        var_name='Materia', value_name='Score')
    sns.boxplot(data=df_melted, x='test_prep', y='Score', hue='Materia', ax=axes[1, 0])
    axes[1, 0].set_title('Scores por Preparación de Examen', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Preparación de Examen', fontsize=12)
    axes[1, 0].set_ylabel('Puntaje', fontsize=12)
    axes[1, 0].legend(title='Materia')
    
    # Por ethnicity
    df_melted = df.melt(id_vars=['ethnicity'], value_vars=['math_score', 'reading_score', 'writing_score'], 
                        var_name='Materia', value_name='Score')
    sns.boxplot(data=df_melted, x='ethnicity', y='Score', hue='Materia', ax=axes[1, 1])
    axes[1, 1].set_title('Scores por Grupo Étnico', fontsize=14, fontweight='bold')
    axes[1, 1].set_xlabel('Grupo Étnico', fontsize=12)
    axes[1, 1].set_ylabel('Puntaje', fontsize=12)
    axes[1, 1].legend(title='Materia')
    
    plt.tight_layout()
    plt.savefig('graficas/02_boxplot_scores.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfica 2: Boxplots comparativos")

def grafica_parental_education(df):
    """Promedio de scores por nivel educativo de los padres"""
    orden_educacion = ["some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"]
    df['parental_education'] = pd.Categorical(df['parental_education'], categories=orden_educacion, ordered=True)
    
    df_grouped = df.groupby('parental_education')[['math_score', 'reading_score', 'writing_score']].mean().reset_index()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    
    x = np.arange(len(df_grouped))
    width = 0.25
    
    bars1 = ax.bar(x - width, df_grouped['math_score'], width, label='Matemáticas', color='#0071e3', alpha=0.8)
    bars2 = ax.bar(x, df_grouped['reading_score'], width, label='Lectura', color='#34c759', alpha=0.8)
    bars3 = ax.bar(x + width, df_grouped['writing_score'], width, label='Escritura', color='#ff9f0a', alpha=0.8)
    
    ax.set_xlabel('Nivel Educativo de los Padres', fontsize=12)
    ax.set_ylabel('Promedio de Puntaje', fontsize=12)
    ax.set_title('Promedio de Scores por Nivel Educativo de los Padres', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels([edu.capitalize() for edu in df_grouped['parental_education']], rotation=45, ha='right')
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Agregar valores sobre las barras
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('graficas/03_parental_education.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfica 3: Scores por nivel educativo de padres")

def grafica_correlacion(df):
    """Matriz de correlación entre scores"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    scores = df[['math_score', 'reading_score', 'writing_score']]
    correlation_matrix = scores.corr()
    
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, 
                annot_kws={'size': 12, 'weight': 'bold'}, ax=ax)
    
    ax.set_title('Matriz de Correlación entre Scores', fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('graficas/04_correlacion_scores.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfica 4: Matriz de correlación")

def grafica_distribuciones_categoricas(df):
    """Gráficos de pastel para variables categóricas"""
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    
    categorias = [
        ('gender', 'Género', axes[0, 0]),
        ('ethnicity', 'Grupo Étnico', axes[0, 1]),
        ('parental_education', 'Educación de Padres', axes[0, 2]),
        ('lunch', 'Tipo de Almuerzo', axes[1, 0]),
        ('test_prep', 'Preparación de Examen', axes[1, 1]),
        ('pass_math', 'Aprobación Matemáticas', axes[1, 2])
    ]
    
    colores = ['#0071e3', '#34c759', '#ff9f0a', '#ff3b30', '#af52de', '#5856d6']
    
    for col, titulo, ax in categorias:
        counts = df[col].value_counts()
        
        # Formatear etiquetas para pass_math
        if col == 'pass_math':
            labels = ['Reprobado' if x == 0 else 'Aprobado' for x in counts.index]
        else:
            labels = [str(x).capitalize() for x in counts.index]
        
        wedges, texts, autotexts = ax.pie(counts, labels=labels, autopct='%1.1f%%',
                                          colors=colores[:len(counts)], startangle=90,
                                          textprops={'fontsize': 10})
        
        ax.set_title(f'Distribución: {titulo}', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('graficas/05_distribuciones_categoricas.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfica 5: Distribuciones categóricas")

def grafica_tasa_aprobacion(df):
    """Tasa de aprobación por categoría"""
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # Por género
    pass_gender = df.groupby('gender')['pass_math'].mean() * 100
    axes[0, 0].bar(pass_gender.index, pass_gender.values, color=['#0071e3', '#ff3b30'], alpha=0.8)
    axes[0, 0].set_title('Tasa de Aprobación en Matemáticas por Género', fontsize=12, fontweight='bold')
    axes[0, 0].set_ylabel('Tasa de Aprobación (%)', fontsize=11)
    axes[0, 0].set_ylim(0, 100)
    for i, v in enumerate(pass_gender.values):
        axes[0, 0].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
    
    # Por lunch
    pass_lunch = df.groupby('lunch')['pass_math'].mean() * 100
    axes[0, 1].bar(pass_lunch.index, pass_lunch.values, color=['#34c759', '#ff9f0a'], alpha=0.8)
    axes[0, 1].set_title('Tasa de Aprobación en Matemáticas por Tipo de Almuerzo', fontsize=12, fontweight='bold')
    axes[0, 1].set_ylabel('Tasa de Aprobación (%)', fontsize=11)
    axes[0, 1].set_ylim(0, 100)
    for i, v in enumerate(pass_lunch.values):
        axes[0, 1].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
    
    # Por test prep
    pass_prep = df.groupby('test_prep')['pass_math'].mean() * 100
    axes[1, 0].bar(pass_prep.index, pass_prep.values, color=['#5856d6', '#af52de'], alpha=0.8)
    axes[1, 0].set_title('Tasa de Aprobación en Matemáticas por Preparación de Examen', fontsize=12, fontweight='bold')
    axes[1, 0].set_ylabel('Tasa de Aprobación (%)', fontsize=11)
    axes[1, 0].set_ylim(0, 100)
    for i, v in enumerate(pass_prep.values):
        axes[1, 0].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
    
    # Por ethnicity
    pass_ethnicity = df.groupby('ethnicity')['pass_math'].mean() * 100
    axes[1, 1].bar(pass_ethnicity.index, pass_ethnicity.values, color='#0071e3', alpha=0.8)
    axes[1, 1].set_title('Tasa de Aprobación en Matemáticas por Grupo Étnico', fontsize=12, fontweight='bold')
    axes[1, 1].set_ylabel('Tasa de Aprobación (%)', fontsize=11)
    axes[1, 1].set_ylim(0, 100)
    for i, v in enumerate(pass_ethnicity.values):
        axes[1, 1].text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('graficas/06_tasa_aprobacion.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfica 6: Tasa de aprobación por categoría")

def grafica_scatter_scores(df):
    """Scatter plots entre scores"""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Math vs Reading
    axes[0].scatter(df['math_score'], df['reading_score'], alpha=0.6, color='#0071e3')
    axes[0].set_xlabel('Math Score', fontsize=12)
    axes[0].set_ylabel('Reading Score', fontsize=12)
    axes[0].set_title('Math vs Reading', fontsize=14, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # Math vs Writing
    axes[1].scatter(df['math_score'], df['writing_score'], alpha=0.6, color='#34c759')
    axes[1].set_xlabel('Math Score', fontsize=12)
    axes[1].set_ylabel('Writing Score', fontsize=12)
    axes[1].set_title('Math vs Writing', fontsize=14, fontweight='bold')
    axes[1].grid(True, alpha=0.3)
    
    # Reading vs Writing
    axes[2].scatter(df['reading_score'], df['writing_score'], alpha=0.6, color='#ff9f0a')
    axes[2].set_xlabel('Reading Score', fontsize=12)
    axes[2].set_ylabel('Writing Score', fontsize=12)
    axes[2].set_title('Reading vs Writing', fontsize=14, fontweight='bold')
    axes[2].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('graficas/07_scatter_scores.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfica 7: Scatter plots entre scores")

def grafica_estadisticas_resumen(df):
    """Gráfica de estadísticas resumen"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    scores = ['math_score', 'reading_score', 'writing_score']
    labels = ['Matemáticas', 'Lectura', 'Escritura']
    
    means = [df[score].mean() for score in scores]
    medians = [df[score].median() for score in scores]
    stds = [df[score].std() for score in scores]
    
    x = np.arange(len(labels))
    width = 0.25
    
    bars1 = ax.bar(x - width, means, width, label='Media', color='#0071e3', alpha=0.8)
    bars2 = ax.bar(x, medians, width, label='Mediana', color='#34c759', alpha=0.8)
    bars3 = ax.bar(x + width, stds, width, label='Desviación Estándar', color='#ff9f0a', alpha=0.8)
    
    ax.set_ylabel('Valor', fontsize=12)
    ax.set_title('Estadísticas Resumen por Materia', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    
    # Agregar valores
    for bars in [bars1, bars2, bars3]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}',
                   ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('graficas/08_estadisticas_resumen.png', dpi=300, bbox_inches='tight')
    plt.close()
    print("✓ Gráfica 8: Estadísticas resumen")

def generar_reporte_textual(df):
    """Generar reporte estadístico textual"""
    reporte = []
    reporte.append("=" * 70)
    reporte.append("REPORTE ESTADÍSTICO - DATOS DE ESTUDIANTES")
    reporte.append("=" * 70)
    reporte.append(f"\nTotal de registros: {len(df)}")
    reporte.append(f"\n--- ESTADÍSTICAS DE SCORES ---")
    
    for score, nombre in [('math_score', 'Matemáticas'), ('reading_score', 'Lectura'), ('writing_score', 'Escritura')]:
        reporte.append(f"\n{nombre}:")
        reporte.append(f"  Media: {df[score].mean():.2f}")
        reporte.append(f"  Mediana: {df[score].median():.2f}")
        reporte.append(f"  Desviación Estándar: {df[score].std():.2f}")
        reporte.append(f"  Mínimo: {df[score].min():.2f}")
        reporte.append(f"  Máximo: {df[score].max():.2f}")
    
    reporte.append(f"\n--- TASA DE APROBACIÓN EN MATEMÁTICAS ---")
    reporte.append(f"Total: {df['pass_math'].mean() * 100:.1f}%")
    
    reporte.append(f"\n--- DISTRIBUCIÓN POR GÉNERO ---")
    for gender, count in df['gender'].value_counts().items():
        reporte.append(f"  {gender}: {count} ({count/len(df)*100:.1f}%)")
    
    reporte.append(f"\n--- DISTRIBUCIÓN POR GRUPO ÉTNICO ---")
    for ethnicity, count in df['ethnicity'].value_counts().items():
        reporte.append(f"  {ethnicity}: {count} ({count/len(df)*100:.1f}%)")
    
    reporte.append(f"\n--- DISTRIBUCIÓN POR EDUCACIÓN DE PADRES ---")
    for edu, count in df['parental_education'].value_counts().items():
        reporte.append(f"  {edu}: {count} ({count/len(df)*100:.1f}%)")
    
    reporte.append("\n" + "=" * 70)
    
    with open('graficas/reporte_estadistico.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(reporte))
    
    print("✓ Reporte estadístico generado")

def main():
    print("Iniciando análisis descriptivo de datos de estudiantes...")
    print("-" * 50)
    
    # Crear directorio
    crear_directorio_output()
    
    # Cargar datos
    print("Cargando datos desde Supabase...")
    df = cargar_datos()
    print(f"Datos cargados: {len(df)} registros")
    
    # Generar gráficas
    print("\nGenerando gráficas...")
    grafica_distribucion_scores(df)
    grafica_boxplot_scores(df)
    grafica_parental_education(df)
    grafica_correlacion(df)
    grafica_distribuciones_categoricas(df)
    grafica_tasa_aprobacion(df)
    grafica_scatter_scores(df)
    grafica_estadisticas_resumen(df)
    
    # Generar reporte
    generar_reporte_textual(df)
    
    print("\n" + "=" * 50)
    print("✓ Análisis completado exitosamente")
    print("✓ Gráficas guardadas en directorio 'graficas'")
    print("✓ Reporte estadístico guardado como 'reporte_estadistico.txt'")
    print("=" * 50)

if __name__ == "__main__":
    main()
