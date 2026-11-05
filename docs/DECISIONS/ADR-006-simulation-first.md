# ADR-006: Metodología Simulation-First

## Contexto
El desarrollo de soluciones IoT suele sufrir retrasos debidos a envíos de componentes, pruebas eléctricas, problemas de soldadura o roturas de sensores.

## Decisión
Adopción estricta de la metodología *Simulation-First*: El MVP se considera funcional y completo cuando la plataforma completa (FastAPI + WebSockets + Mosquitto + PostgreSQL + React Frontend) funciona de punta a punta con datos y escenarios sintéticos realistas.

## Consecuencias
- **Positivas**: Iteración ágil de la interfaz de usuario, validación temprana de flujos de trabajo biológicos y de lotes, cobertura de pruebas sin depender de hardware físico.
- **Negativas**: Necesidad de calibrar los modelos matemáticos una vez que se obtengan lecturas físicas reales.
