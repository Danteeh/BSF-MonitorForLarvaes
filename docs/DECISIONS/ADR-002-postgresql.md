# ADR-002: Elección de PostgreSQL como Motor Relacional Principal

## Contexto
El sistema requiere persistencia de telemetría de series temporales, pero a la vez relaciones estrictas de integridad referencial entre lotes, eventos de alimentación, experimentos biológicos, usuarios, dispositivos y metadatos multimedia.

## Decisión
Adoptar **PostgreSQL 16** como motor principal relacional, aprovechando su soporte para particionamiento de tablas por fecha, tipos nativos JSONB para metadatos flexibles, e índices BRIN/B-Tree de alto rendimiento para series temporales.

## Consecuencias
- **Positivas**: Máxima fiabilidad, soporte ACID para transacciones biológicas y de lotes, unificación de modelos sin necesidad de mantener dos bases de datos distintas en el MVP.
- **Negativas**: Mayor consumo de memoria RAM respecto a SQLite embebido.
