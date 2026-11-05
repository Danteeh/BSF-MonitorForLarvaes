import pytest
from raspberry.hal.virtual_sensors import (
    VirtualTemperatureSensor,
    VirtualHumiditySensor,
    VirtualWeightSensor,
    VirtualLightSensor
)
from raspberry.hal.base import QualityEnum, SourceEnum

@pytest.mark.asyncio
async def test_virtual_temperature_sensor_nominal():
    sensor = VirtualTemperatureSensor(
        sensor_id="REP-TEMP-TEST",
        zone_id="ZONE-REP",
        device_id="NODE-REP-TEST",
        base_temp=27.0
    )
    reading = await sensor.read()

    assert reading.sensor_id == "REP-TEMP-TEST"
    assert reading.zone_id == "ZONE-REP"
    assert reading.variable == "ambient_temperature"
    assert reading.unit == "C"
    assert reading.source == SourceEnum.SIMULATION
    assert reading.quality == QualityEnum.VALID
    assert 20.0 <= reading.value <= 35.0

@pytest.mark.asyncio
async def test_virtual_temperature_sensor_disconnected_fault():
    sensor = VirtualTemperatureSensor(
        sensor_id="LAR-TEMP-FAULT",
        zone_id="ZONE-LAR",
        device_id="NODE-LAR-TEST",
        base_temp=33.0
    )
    # Inyectar fallo de desconexión
    sensor.inject_fault("disconnected")
    reading = await sensor.read()

    assert reading.quality == QualityEnum.INVALID
    assert reading.value == 0.0

@pytest.mark.asyncio
async def test_virtual_temperature_sensor_out_of_range_fault():
    sensor = VirtualTemperatureSensor(
        sensor_id="LAR-TEMP-HIGH",
        zone_id="ZONE-LAR",
        device_id="NODE-LAR-TEST",
        base_temp=33.0
    )
    # Inyectar fallo fuera de rango
    sensor.inject_fault("out_of_range")
    reading = await sensor.read()

    assert reading.quality == QualityEnum.DEGRADED
    assert reading.value > 55.0

@pytest.mark.asyncio
async def test_virtual_humidity_sensor():
    sensor = VirtualHumiditySensor(
        sensor_id="INC-HUM-TEST",
        zone_id="ZONE-INC",
        device_id="NODE-INC-TEST",
        base_hum=75.0
    )
    reading = await sensor.read()

    assert reading.variable == "relative_humidity"
    assert reading.unit == "%"
    assert 60.0 <= reading.value <= 90.0
    assert reading.quality == QualityEnum.VALID

@pytest.mark.asyncio
async def test_virtual_weight_sensor():
    sensor = VirtualWeightSensor(
        sensor_id="LAR-WEIGHT-TEST",
        zone_id="ZONE-LAR",
        device_id="NODE-LAR-TEST",
        base_weight=15.0
    )
    reading = await sensor.read()

    assert reading.variable == "weight"
    assert reading.unit == "kg"
    assert 14.0 <= reading.value <= 16.0
    assert reading.quality == QualityEnum.VALID
