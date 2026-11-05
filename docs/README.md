# Índice de Documentación Técnica — BSF MONITOR

Bienvenido al repositorio documental del sistema **BSF MONITOR**. Este compendio define la arquitectura, contratos de datos, especificaciones de hardware y protocolos de prueba.

## Índice General

| Documento | Descripción |
|---|---|
| [ARCHITECTURE.md](ARCHITECTURE.md) | Arquitectura global, capas lógicas, diagramas de flujo y comunicación. |
| [REQUIREMENTS.md](REQUIREMENTS.md) | Requisitos funcionales, no funcionales y criterios de aceptación. |
| [DATA_MODEL.md](DATA_MODEL.md) | Modelo relacional PostgreSQL, tablas, campos, índices y particionamiento. |
| [API_SPECIFICATION.md](API_SPECIFICATION.md) | Endpoints REST de FastAPI, schemas Pydantic, autenticación y WebSockets. |
| [MQTT_SPECIFICATION.md](MQTT_SPECIFICATION.md) | Estructura jerárquica de tópicos, payloads JSON, QoS y reintentos. |
| [HARDWARE_ABSTRACTION.md](HARDWARE_ABSTRACTION.md) | Contratos abstractos HAL, drivers virtuales y drivers físicos. |
| [SIMULATOR_DESIGN.md](SIMULATOR_DESIGN.md) | Motores de generación biológica/ambiental sintética y simulación de fallos. |
| [CHANGELOG.md](CHANGELOG.md) | Registro histórico de versiones y cambios del sistema. |
| [DECISIONS/](DECISIONS/) | Architecture Decision Records (ADRs) con justificaciones técnicas. |
