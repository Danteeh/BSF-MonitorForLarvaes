# ADR-005: Almacenamiento Multimedia Desacoplado de la Base de Datos

## Contexto
Las cámaras e imágenes de monitoreo generan archivos binarios de alto volumen que degradarían el rendimiento y tamaño de los backups de PostgreSQL si se almacenaran como BLOBs (bytea).

## Decisión
Almacenar los archivos binarios (JPEG, PNG, MP4) en el sistema de archivos (`storage/media/`), registrando únicamente rutas relativas, hashes SHA256, metadatos y dimensiones dentro de la tabla `media_files` de PostgreSQL.

## Consecuencias
- **Positivas**: Base de datos ligera y ágil, entrega estática eficiente mediante FastAPI o Nginx, facilidad para migrar el almacenamiento a S3 o MinIO en el futuro.
- **Negativas**: Necesidad de sincronizar la consistencia entre registros de base de datos y archivos en disco.
