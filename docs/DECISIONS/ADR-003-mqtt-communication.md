# ADR-003: Telemetría Mediante MQTT (Eclipse Mosquitto)

## Contexto
Los sensores transmiten mediciones frecuentes y asíncronas desde múltiples fuentes. Acoplar el backend HTTP directamente a peticiones POST periódicas desde microcontroladores generaría congestión y sobrecarga de conexiones.

## Decisión
Implementar un broker de mensajería **Eclipse Mosquitto (MQTT 3.1.1/5.0)** como canal de telemetría entre nodos/simulador y el backend FastAPI.

## Consecuencias
- **Positivas**: Protocolo ligero, bajo ancho de banda, desacoplamiento temporal de productores y consumidores, soporte nativo de tópicos jerárquicos y LWT (Last Will and Testament).
- **Negativas**: Necesidad de un servicio de infraestructura adicional en el cluster/compose.
