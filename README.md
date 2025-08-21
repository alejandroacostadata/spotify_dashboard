# Spotify Analytics Dashboard

## Resumen Ejecutivo

Este proyecto presenta una solución de análisis de datos avanzada para el procesamiento y visualización de historiales de reproducción de Spotify. La aplicación desarrollada en Python utiliza Streamlit como framework principal, proporcionando una interfaz web interactiva que transforma datos de streaming musical en insights accionables mediante técnicas de análisis exploratorio de datos y visualización avanzada.

## Características Principales

### Análisis Temporal
- Seguimiento de patrones de escucha a lo largo del tiempo
- Identificación de tendencias estacionales y mensuales
- Análisis de comportamiento por horas del día y días de la semana
- Mapeo de actividad mediante gráficos polares y timeline interactivos

### Métricas de Comportamiento
- Cálculo de tasas de omisión de canciones (skip rate)
- Análisis de lealtad hacia artistas basado en tiempo de escucha y duración temporal
- Identificación de streaks de escucha consecutivos
- Segmentación de preferencias por franjas horarias

### Visualizaciones Interactivas
- Dashboards responsivos con temática oscura profesional
- Gráficos de dispersión para análisis de correlaciones
- Mapas de calor temporales para patrones de uso
- Diagramas polares para visualización de ciclos temporales

### Funcionalidades Técnicas
- Procesamiento automático de archivos CSV de Spotify Extended Streaming History
- Sistema de caché optimizado para rendimiento mejorado
- Generación de datos de muestra para demostración
- Compatibilidad con múltiples formatos de datos de Spotify
![Spotify Analytics Dashboard](https://raw.githubusercontent.com/alejandroacostadata/spotify_dashboard/main/spotify-dashboard-main.png)


## Arquitectura del Sistema

### Stack Tecnológico
- **Frontend**: Streamlit con CSS customizado
- **Visualización**: Plotly, Plotly Express, Matplotlib, Seaborn
- **Procesamiento de Datos**: Pandas, NumPy
- **Backend**: Python 3.8+

### Estructura de Datos
La aplicación procesa archivos CSV con la siguiente estructura mínima requerida:
- Timestamp de reproducción
- Nombre de la canción y artista
- Duración de reproducción (ms_played)
- Plataforma de reproducción
- Indicadores de omisión

## Instalación y Configuración

### Requisitos del Sistema
```bash
pip install streamlit pandas plotly numpy seaborn matplotlib
```

### Ejecución
```bash
streamlit run spotify_dashboard.py
```

## Uso de la Aplicación

### Carga de Datos
1. Solicitar datos de Spotify Extended Streaming History desde la cuenta personal
2. Cargar el archivo CSV mediante la interfaz web
3. La aplicación procesa automáticamente los datos y genera visualizaciones

### Navegación
La interfaz se organiza en secciones temáticas:
- **Métricas Generales**: KPIs principales de consumo
![Spotify Analytics Dashboard](https://raw.githubusercontent.com/alejandroacostadata/spotify_dashboard/main/spotify-dashboard-main_2.png)
- **Análisis de Patrones**: Comportamiento temporal y estacional
![Spotify Analytics Dashboard](https://raw.githubusercontent.com/alejandroacostadata/spotify_dashboard/main/spotify-temporal-analysis.png)
- **DNA Musical**: Artistas y canciones más reproducidas
![Spotify Analytics Dashboard](https://raw.githubusercontent.com/alejandroacostadata/spotify_dashboard/main/spotify-artist-dna.png)
- **Análisis de Plataformas**: Distribución por dispositivos
![Spotify Analytics Dashboard](https://raw.githubusercontent.com/alejandroacostadata/spotify_dashboard/main/spotify-mood-patterns.png)

## Métricas y KPIs

### Indicadores Principales
- Total de canciones reproducidas
- Horas totales de escucha
- Número de artistas únicos explorados
![Spotify Analytics Dashboard](https://raw.githubusercontent.com/alejandroacostadata/spotify_dashboard/main/spotify-listening-clock.png)
- Cantidad de canciones únicas
- Tasa de omisión promedio
![Spotify Analytics Dashboard](https://raw.githubusercontent.com/alejandroacostadata/spotify_dashboard/main/spotify-skip-analysis.png)
### Análisis Avanzados
- Índice de lealtad por artista
- Patrones de estado de ánimo por horarios
![Spotify Analytics Dashboard](https://raw.githubusercontent.com/alejandroacostadata/spotify_dashboard/main/spotify-moments-day.png)
- Análisis de completitud de reproducción
- Métricas de descubrimiento musical
![Spotify Analytics Dashboard](https://raw.githubusercontent.com/alejandroacostadata/spotify_dashboard/main/spotify-loyalty-index.png)
## Consideraciones de Privacidad

- Todos los datos se procesan localmente
- No se realiza almacenamiento permanente de información personal
- El sistema incluye generación de datos sintéticos para demostración
- Cumplimiento con estándares de protección de datos personales

## Casos de Uso

### Análisis Personal
- Autoconocimiento de hábitos musicales
- Identificación de patrones de comportamiento
- Seguimiento de evolución de gustos musicales
- Análisis de patrones temporales en entretenimiento
- Investigación en psicología del consumo musical

### Análisis Comercial
- Comprensión de audiencias target
- Identificación de nichos de mercado
- Optimización de estrategias de contenido

## Limitaciones y Consideraciones

- Requiere datos históricos de Spotify Extended Streaming History
- Los análisis de estado de ánimo son aproximaciones basadas en patrones temporales
- La precisión de insights depende de la cantidad y calidad de datos disponibles
- Funcionalidad completa requiere al menos 30 días de datos históricos

## Desarrollador

**Alejandro Acosta**  
Proyecto desarrollado utilizando datasets de Kaggle para análisis de datos musicales avanzado.

## Licencia

Este proyecto se distribuye bajo licencia de uso académico y personal. Para uso comercial, contactar al desarrollador.

---

*Última actualización: Agosto 2025*
