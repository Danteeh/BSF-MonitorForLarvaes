# Diseño del Motor de Simulación — BSF MONITOR

El simulador (`simulator/`) emula el comportamiento físico, ambiental y biológico de las tres zonas de producción de mosca soldado negra sin requerir hardware físico.

## 1. Modelado de Zonas

### ZONE-REP (Reproducción)
- **Temperatura**: Ciclo diurno/nocturno sinusoidal centrado en 27.5 °C (amplitud ±2.5 °C, ruido gaussiano $\sigma=0.2$).
- **Humedad Relativa**: Entre 60% y 75%, correlacionada inversamente con la temperatura.
- **Iluminación**: Fotoperiodo automático (ej. 14h luz / 10h oscuridad) variando de 0 lux a 12.000 lux (emulando lámparas de reproducción).

### ZONE-INC (Incubación)
- **Temperatura**: Entorno estable a 29.0 °C (±0.8 °C).
- **Humedad**: Alta humedad relativa (70% - 80%) para evitar deshidratación de los paquetes de huevos.

### ZONE-LAR (Larvas y Biorreactor)
- **Temperatura de Sustrato**: Entre 30.0 °C y 36.0 °C debido al calor metabólico de la actividad larvaria.
- **Humedad de Sustrato**: 60% - 70%.
- **Masa / Peso**: Aumento paulatino de biomasa conforme consumen el alimento suministrado, con reducciones súbitas al ocurrir cosechas.

---

## 2. Inyección de Escenarios y Fallos

El simulador cuenta con un inyector de eventos anómalos:
1. **Sensor Desconectado**: Envía lectura con `quality: invalid` o deja de publicar en el tópico.
2. **Valor Fuera de Rango**: Emite un valor extremo (ej. temperatura de 55 °C) para comprobar disparadores de alerta.
3. **Pérdida de Comunicación**: Detiene publicaciones de un nodo completo (`NODE-LAR-001`) para verificar detección de timeout en backend.
4. **Valor Congelado (Drift/Stuck)**: Emite repetidamente el mismo número sin fluctuación estocástica.
