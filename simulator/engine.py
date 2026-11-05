import asyncio
import json
import logging
import os
import signal
import sys
from datetime import datetime, timezone
import paho.mqtt.client as mqtt

# HAL virtual sensors
from raspberry.hal.virtual_sensors import (
    VirtualTemperatureSensor,
    VirtualHumiditySensor,
    VirtualLightSensor,
    VirtualWeightSensor
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [SIMULATOR]: %(message)s"
)
logger = logging.getLogger("bsf.simulator")

MQTT_HOST = os.getenv("MQTT_HOST", "mosquitto")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
POLL_INTERVAL = int(os.getenv("SENSOR_POLL_INTERVAL", 5))

TOPIC_MAP = {
    "REP-TEMP-001": "bsf/reproduction/temperature",
    "REP-HUM-001": "bsf/reproduction/humidity",
    "REP-LUX-001": "bsf/reproduction/light",
    "INC-TEMP-001": "bsf/incubation/temperature",
    "INC-HUM-001": "bsf/incubation/humidity",
    "LAR-TEMP-001": "bsf/larvae/temperature",
    "LAR-HUM-001": "bsf/larvae/humidity",
    "LAR-WEIGHT-001": "bsf/larvae/weight"
}

class BioreactorSimulator:
    def __init__(self):
        self.running = False
        self.mqtt_client = mqtt.Client(
            client_id="bsf_iot_simulator",
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        self.sensors = self._initialize_sensors()

    def _initialize_sensors(self):
        return [
            # Zona Reproducción
            VirtualTemperatureSensor("REP-TEMP-001", "ZONE-REP", "NODE-REP-001", base_temp=27.5),
            VirtualHumiditySensor("REP-HUM-001", "ZONE-REP", "NODE-REP-001", base_hum=65.0),
            VirtualLightSensor("REP-LUX-001", "ZONE-REP", "NODE-REP-001"),

            # Zona Incubación
            VirtualTemperatureSensor("INC-TEMP-001", "ZONE-INC", "NODE-INC-001", base_temp=29.0),
            VirtualHumiditySensor("INC-HUM-001", "ZONE-INC", "NODE-INC-001", base_hum=75.0),

            # Zona Larvas (Biorreactor)
            VirtualTemperatureSensor("LAR-TEMP-001", "ZONE-LAR", "NODE-LAR-001", base_temp=33.5, batch_id="BATCH-2026-001"),
            VirtualHumiditySensor("LAR-HUM-001", "ZONE-LAR", "NODE-LAR-001", base_hum=68.0, batch_id="BATCH-2026-001"),
            VirtualWeightSensor("LAR-WEIGHT-001", "ZONE-LAR", "NODE-LAR-001", base_weight=15.8, batch_id="BATCH-2026-001"),
        ]

    def connect_mqtt(self):
        logger.info(f"Connecting simulator to MQTT Broker at {MQTT_HOST}:{MQTT_PORT}...")
        try:
            self.mqtt_client.on_message = self._on_mqtt_message
            self.mqtt_client.connect(MQTT_HOST, MQTT_PORT, keepalive=60)
            self.mqtt_client.loop_start()
            self.mqtt_client.subscribe("bsf/simulator/command", qos=1)
            logger.info("Simulator MQTT client connected and subscribed to bsf/simulator/command.")
        except Exception as e:
            logger.error(f"Could not connect simulator to MQTT: {e}")
            raise

    def _on_mqtt_message(self, client, userdata, msg):
        try:
            payload = json.loads(msg.payload.decode("utf-8"))
            sensor_id = payload.get("sensor_id")
            fault_type = payload.get("fault_type")
            target = next((s for s in self.sensors if s.sensor_id == sensor_id), None)
            if target:
                applied_fault = None if fault_type == "clear" else fault_type
                target.inject_fault(applied_fault)
                logger.info(f"Simulator injected fault '{applied_fault}' on {sensor_id}")
        except Exception as e:
            logger.error(f"Error handling simulator command: {e}")

    async def run(self):
        self.running = True
        self.connect_mqtt()

        devices = ["NODE-REP-001", "NODE-INC-001", "NODE-LAR-001"]
        iteration = 0

        logger.info(f"Bioreactor Simulator active. Emitting data every {POLL_INTERVAL} seconds...")

        while self.running:
            try:
                # 1. Emitir telemetría de cada sensor
                for sensor in self.sensors:
                    reading = await sensor.read()
                    topic = TOPIC_MAP.get(sensor.sensor_id, f"bsf/{sensor.zone_id.lower()}/{sensor.variable}")

                    payload = {
                        "device_id": reading.device_id,
                        "sensor_id": reading.sensor_id,
                        "zone_id": reading.zone_id,
                        "batch_id": reading.batch_id,
                        "variable": reading.variable,
                        "value": reading.value,
                        "unit": reading.unit,
                        "timestamp": reading.timestamp.isoformat(),
                        "source": reading.source.value,
                        "quality": reading.quality.value
                    }

                    self.mqtt_client.publish(topic, json.dumps(payload), qos=1)

                # 2. Heartbeat de dispositivos cada 3 ciclos
                if iteration % 3 == 0:
                    for dev_id in devices:
                        hb_payload = {
                            "device_id": dev_id,
                            "status": "ONLINE",
                            "timestamp": datetime.now(timezone.utc).isoformat()
                        }
                        self.mqtt_client.publish(f"bsf/devices/{dev_id}/status", json.dumps(hb_payload), qos=1)

                iteration += 1
                await asyncio.sleep(POLL_INTERVAL)

            except Exception as e:
                logger.error(f"Error in simulator cycle: {e}")
                await asyncio.sleep(2)

    def stop(self):
        self.running = False
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
        logger.info("Simulator stopped.")

if __name__ == "__main__":
    sim = BioreactorSimulator()

    def handle_sig(sig, frame):
        sim.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, handle_sig)
    signal.signal(signal.SIGTERM, handle_sig)

    asyncio.run(sim.run())
