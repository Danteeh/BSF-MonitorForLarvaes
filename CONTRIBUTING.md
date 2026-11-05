# Contribución a BSF MONITOR

Este documento establece las pautas de desarrollo para colaboradores y agentes de IA en el proyecto **BSF MONITOR**.

## Principios Fundamentales
1. **Simulación antes de adquisición**: Ningún módulo de negocio debe acoplarse a librerías de hardware físico (`RPi.GPIO`, `smbus2`, etc.). Debe respetarse la capa HAL.
2. **Trazabilidad de datos**: Cada lectura de sensor o evento debe especificar su origen (`simulation` o `hardware`).
3. **Persistencia inmutable**: Las mediciones de telemetría son de solo lectura y nunca se sobrescriben.
4. **Documentación obligatoria**: Cualquier nuevo módulo, endpoint de API o cambio en tópicos MQTT debe actualizar la documentación técnica correspondiente en `docs/`.
5. **Pruebas automatizadas**: Todo código debe contar con pruebas unitarias e integración ejecutables.

## Flujo de Trabajo
1. Seleccionar la tarea de la fase activa del roadmap en [guia_agente.md](file:///e:/BSF%20Moscas/guia_agente.md).
2. Verificar contratos en `docs/ARCHITECTURE.md`, `docs/API_SPECIFICATION.md` y `docs/MQTT_SPECIFICATION.md`.
3. Implementar código con cobertura de pruebas.
4. Si se toma una decisión arquitectónica significativa, documentarla en `docs/DECISIONS/ADR-XXX.md`.
5. Actualizar `docs/CHANGELOG.md`.
