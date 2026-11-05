import json
import asyncio
import logging
from datetime import datetime, timezone
import paho.mqtt.client as mqtt
from app.config import settings
from app.websocket.manager import ws_manager
from app.database.session import AsyncSessionLocal
from app.models.entities import SensorReading, Device, Alert

logger = logging.getLogger("bsf.mqtt")

class MQTTConsumer:
    def __init__(self):
        self.client: mqtt.Client = None
        self.is_connected = False
        self.loop: asyncio.AbstractEventLoop = None

    def start(self, loop: asyncio.AbstractEventLoop):
        self.loop = loop
        self.client = mqtt.Client(
            client_id=settings.MQTT_CLIENT_ID,
            callback_api_version=mqtt.CallbackAPIVersion.VERSION2
        )
        if settings.MQTT_USER and settings.MQTT_PASSWORD:
            self.client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

        try:
            logger.info(f"Connecting to MQTT broker at {settings.MQTT_HOST}:{settings.MQTT_PORT}...")
            self.client.connect_async(settings.MQTT_HOST, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
            self.client.loop_start()
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")

    def publish(self, topic: str, payload: dict, qos: int = 1):
        if self.client and self.is_connected:
            self.client.publish(topic, json.dumps(payload), qos=qos)
            logger.info(f"Published message to {topic}")
        else:
            logger.warning(f"Cannot publish to {topic}: MQTT not connected")

    def stop(self):
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.is_connected = False
            logger.info("MQTT Client disconnected and loop stopped")

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        if rc == 0:
            self.is_connected = True
            logger.info("Connected to MQTT Broker successfully!")
            # Suscribirse a todos los tópicos del biorreactor
            client.subscribe("bsf/#", qos=1)
            logger.info("Subscribed to topic: bsf/#")
        else:
            self.is_connected = False
            logger.error(f"MQTT Connection failed with code {rc}")

    def _on_disconnect(self, client, userdata, flags, rc, properties=None):
        self.is_connected = False
        logger.warning(f"Disconnected from MQTT Broker (rc={rc})")

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        try:
            payload_str = msg.payload.decode("utf-8")
            data = json.loads(payload_str)
        except Exception as e:
            logger.error(f"Error decoding MQTT payload from {topic}: {e}")
            return

        # Despachar procesamiento asíncrono en el bucle de eventos principal
        if self.loop and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(self._process_message(topic, data), self.loop)

    async def _process_message(self, topic: str, data: dict):
        try:
            # 1. Mensaje de telemetría de sensor
            if "sensor_id" in data and "value" in data and "zone_id" in data:
                # Transmitir inmediatamente vía WebSocket a los navegadores
                await ws_manager.broadcast_json({
                    "type": "telemetry",
                    "topic": topic,
                    "data": data
                })

                # Persistir en PostgreSQL
                async with AsyncSessionLocal() as session:
                    try:
                        recorded_at_dt = datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
                    except Exception:
                        recorded_at_dt = datetime.now(timezone.utc)

                    reading = SensorReading(
                        sensor_id=data["sensor_id"],
                        zone_id=data["zone_id"],
                        device_id=data.get("device_id"),
                        batch_id=data.get("batch_id"),
                        variable=data["variable"],
                        value=float(data["value"]),
                        unit=data.get("unit", ""),
                        source=data.get("source", "simulation"),
                        quality=data.get("quality", "valid"),
                        recorded_at=recorded_at_dt
                    )
                    session.add(reading)

                    # Detección de anomalías / alertas de umbral
                    val = float(data["value"])
                    if data["variable"] == "substrate_temperature" and val > 42.0:
                        alert = Alert(
                            zone_id=data["zone_id"],
                            sensor_id=data["sensor_id"],
                            severity="CRITICAL",
                            title="Temperatura Crítica de Sustrato",
                            message=f"La temperatura en {data['zone_id']} ha alcanzado {val} °C (umbral máx: 42 °C)."
                        )
                        session.add(alert)
                        await ws_manager.broadcast_json({
                            "type": "alert",
                            "severity": "CRITICAL",
                            "title": alert.title,
                            "message": alert.message,
                            "zone_id": alert.zone_id
                        })

                    await session.commit()

            # 2. Mensaje de estado de dispositivo / nodo
            elif "device_id" in data and "status" in data:
                await ws_manager.broadcast_json({
                    "type": "device_status",
                    "data": data
                })
                async with AsyncSessionLocal() as session:
                    device = await session.get(Device, data["device_id"])
                    if device:
                        device.status = data["status"]
                        device.last_seen = datetime.now(timezone.utc)
                        await session.commit()

        except Exception as e:
            logger.error(f"Error processing MQTT message for topic {topic}: {e}")

mqtt_consumer = MQTTConsumer()
