# Registro de Cambios (Changelog) — BSF MONITOR

Todos los cambios notables en este proyecto se documentarán en este archivo según [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [0.1.0] - 2026-11-05
### Añadido
- **Fase 0 (Preparación)**:
  - Estructura modular completa del repositorio (`backend/`, `frontend/`, `simulator/`, `raspberry/`, `storage/`, `docs/`).
  - Configuración multi-entorno: `.env.example`, `.env.simulation`, `.env.development`.
  - Configuración orquestada de contenedores `docker-compose.yml` (PostgreSQL 16, Mosquitto 2.0, FastAPI Backend, Simulator, React Frontend).
  - Documentación técnica base: `README.md`, `ARCHITECTURE.md`, `REQUIREMENTS.md`, `DATA_MODEL.md`, `API_SPECIFICATION.md`, `MQTT_SPECIFICATION.md`, `HARDWARE_ABSTRACTION.md`, `SIMULATOR_DESIGN.md`.
  - Registros de decisiones arquitectónicas (`ADR-001` a `ADR-006`).
