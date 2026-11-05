# ADR-004: Hardware Abstraction Layer (HAL) Mandatorio

## Contexto
El desarrollo inicia en modo simulación sin hardware físico. Si el código de negocio o controladores estuvieran acoplados a drivers concretos de Raspberry Pi (como GPIO o I2C), el desarrollo se bloquearía y la migración futura sería costosa y propensa a regresiones.

## Decisión
Establecer una capa HAL obligatoria (`raspberry/hal`). Toda lectura de sensor o captura de cámara debe implementarse a través de contratos de clases abstractas (`BaseSensor`, `CameraDevice`). Las implementaciones concretas `Virtual*` emulan el comportamiento y se reemplazan por `Real*` al conectar hardware.

## Consecuencias
- **Positivas**: Desarrollo 100% autónomo y testeable en cualquier sistema operativo (Windows, Linux, macOS), transición transparente al hardware físico.
- **Negativas**: Mayor número inicial de interfaces y clases envolventes.
