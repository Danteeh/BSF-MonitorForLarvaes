# ADR-001: Raspberry Pi 5 Centralizada con Nodos de Zona

## Contexto
El biorreactor de mosca soldado negra cuenta con 3 áreas separadas físicamente (`ZONE-REP`, `ZONE-INC`, `ZONE-LAR`). Llevar cableado analógico/I2C/1-Wire de larga distancia directamente a los pines GPIO de una única Raspberry genera pérdidas de señal, interferencias electromagnéticas y ruido.

## Decisión
Utilizar una Raspberry Pi 5 como concentrador/coordinador central, comunicándose con nodos locales de zona (microcontroladores dedicados) a través de un bus industrial robusto (RS-485 / Modbus) o red local con MQTT.

## Consecuencias
- **Positivas**: Reducción de ruido eléctrico, modularidad por zona, escalabilidad a nuevas naves o biorreactores.
- **Negativas**: Mayor número de microcontroladores que requieren firmware individual.
