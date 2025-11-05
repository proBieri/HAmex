"""Sensor platform for HAmex integration."""
from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import PERCENTAGE, UnitOfVolume
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import HAmexDataUpdateCoordinator
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up HAmex sensor based on a config entry."""
    coordinator: HAmexDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities = []

    if coordinator.data and "Items" in coordinator.data:
        # Create sensors for each tank
        for tank in coordinator.data["Items"]:
            tank_name = tank.get("MexName", f"Tank {tank.get('SensorId')}")
            sensor_id = tank.get("SensorId")

            # Current volume percentage
            entities.append(
                HAmexTankPercentageSensor(coordinator, sensor_id, tank_name)
            )

            # Current volume in liters
            entities.append(
                HAmexTankVolumeSensor(coordinator, sensor_id, tank_name)
            )

            # Battery percentage
            entities.append(
                HAmexBatterySensor(coordinator, sensor_id, tank_name)
            )

            # Usage rate
            entities.append(
                HAmexUsageSensor(coordinator, sensor_id, tank_name)
            )

            # Remaining days
            entities.append(
                HAmexRemainingDaysSensor(coordinator, sensor_id, tank_name)
            )

        # Add price sensors
        if "PriceComparedToYesterdayPercentage" in coordinator.data:
            entities.append(HAmexPriceComparisonSensor(coordinator))

        if "PriceForecastPercentage" in coordinator.data:
            entities.append(HAmexPriceForecastSensor(coordinator))

    async_add_entities(entities)


class HAmexTankPercentageSensor(CoordinatorEntity, SensorEntity):
    """Sensor for tank fill percentage."""

    def __init__(
        self,
        coordinator: HAmexDataUpdateCoordinator,
        sensor_id: int,
        tank_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._tank_name = tank_name
        self._attr_name = f"{tank_name} Füllstand"
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}_percentage"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:gauge"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        tank = self._get_tank_data()
        return tank.get("CurrentVolumePercentage") if tank else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        tank = self._get_tank_data()
        if not tank:
            return {}

        return {
            "max_volume": tank.get("MaxVolume"),
            "is_main_tank": tank.get("IsMain"),
            "zip_code": tank.get("ZipCode"),
            "last_measurement": tank.get("LastMeasurementTimeStamp"),
            "measurement_successful": tank.get("LastMeasurementWasSuccessfully"),
        }

    def _get_tank_data(self) -> dict[str, Any] | None:
        """Get tank data from coordinator."""
        if not self.coordinator.data or "Items" not in self.coordinator.data:
            return None

        for tank in self.coordinator.data["Items"]:
            if tank.get("SensorId") == self._sensor_id:
                return tank
        return None


class HAmexTankVolumeSensor(CoordinatorEntity, SensorEntity):
    """Sensor for tank volume in liters."""

    def __init__(
        self,
        coordinator: HAmexDataUpdateCoordinator,
        sensor_id: int,
        tank_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._tank_name = tank_name
        self._attr_name = f"{tank_name} Volumen"
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}_volume"
        self._attr_native_unit_of_measurement = UnitOfVolume.LITERS
        self._attr_device_class = SensorDeviceClass.VOLUME
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:oil-temperature"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        tank = self._get_tank_data()
        return tank.get("CurrentVolume") if tank else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        tank = self._get_tank_data()
        if not tank:
            return {}

        return {
            "max_volume": tank.get("MaxVolume"),
            "yearly_usage": tank.get("YearlyOilUsage"),
            "usage_rate": tank.get("Usage"),
        }

    def _get_tank_data(self) -> dict[str, Any] | None:
        """Get tank data from coordinator."""
        if not self.coordinator.data or "Items" not in self.coordinator.data:
            return None

        for tank in self.coordinator.data["Items"]:
            if tank.get("SensorId") == self._sensor_id:
                return tank
        return None


class HAmexBatterySensor(CoordinatorEntity, SensorEntity):
    """Sensor for MEX device battery."""

    def __init__(
        self,
        coordinator: HAmexDataUpdateCoordinator,
        sensor_id: int,
        tank_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._tank_name = tank_name
        self._attr_name = f"{tank_name} Batterie"
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}_battery"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        tank = self._get_tank_data()
        return tank.get("BatteryPercentage") if tank else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        tank = self._get_tank_data()
        if not tank:
            return {}

        return {
            "battery_voltage": tank.get("Battery"),
        }

    def _get_tank_data(self) -> dict[str, Any] | None:
        """Get tank data from coordinator."""
        if not self.coordinator.data or "Items" not in self.coordinator.data:
            return None

        for tank in self.coordinator.data["Items"]:
            if tank.get("SensorId") == self._sensor_id:
                return tank
        return None


class HAmexUsageSensor(CoordinatorEntity, SensorEntity):
    """Sensor for daily oil usage."""

    def __init__(
        self,
        coordinator: HAmexDataUpdateCoordinator,
        sensor_id: int,
        tank_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._tank_name = tank_name
        self._attr_name = f"{tank_name} Verbrauch"
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}_usage"
        self._attr_native_unit_of_measurement = "L/Tag"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:chart-line"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        tank = self._get_tank_data()
        if tank and tank.get("Usage"):
            return round(tank.get("Usage"), 2)
        return None

    def _get_tank_data(self) -> dict[str, Any] | None:
        """Get tank data from coordinator."""
        if not self.coordinator.data or "Items" not in self.coordinator.data:
            return None

        for tank in self.coordinator.data["Items"]:
            if tank.get("SensorId") == self._sensor_id:
                return tank
        return None


class HAmexRemainingDaysSensor(CoordinatorEntity, SensorEntity):
    """Sensor for estimated remaining days."""

    def __init__(
        self,
        coordinator: HAmexDataUpdateCoordinator,
        sensor_id: int,
        tank_name: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._tank_name = tank_name
        self._attr_name = f"{tank_name} Reichweite"
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}_remaining_days"
        self._attr_native_unit_of_measurement = "Tage"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:calendar-clock"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        tank = self._get_tank_data()
        return tank.get("RemainingDays") if tank else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        tank = self._get_tank_data()
        if not tank:
            return {}

        remains_until = tank.get("RemainsUntil")
        remains_combined = tank.get("RemainsUntilCombined", {})

        return {
            "remains_until": remains_until,
            "remains_formatted": f"{remains_combined.get('RemainsValue')} {remains_combined.get('RemainsUnit')}",
            "month_year": remains_combined.get("MonthAndYear"),
        }

    def _get_tank_data(self) -> dict[str, Any] | None:
        """Get tank data from coordinator."""
        if not self.coordinator.data or "Items" not in self.coordinator.data:
            return None

        for tank in self.coordinator.data["Items"]:
            if tank.get("SensorId") == self._sensor_id:
                return tank
        return None


class HAmexPriceComparisonSensor(CoordinatorEntity, SensorEntity):
    """Sensor for price comparison to yesterday."""

    def __init__(self, coordinator: HAmexDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Heizöl Preis Vergleich"
        self._attr_unique_id = f"{DOMAIN}_price_comparison"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:chart-line-variant"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data:
            value = self.coordinator.data.get("PriceComparedToYesterdayPercentage")
            if value is not None:
                return round(value * 100, 2)
        return None


class HAmexPriceForecastSensor(CoordinatorEntity, SensorEntity):
    """Sensor for price forecast."""

    def __init__(self, coordinator: HAmexDataUpdateCoordinator) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Heizöl Preis Prognose"
        self._attr_unique_id = f"{DOMAIN}_price_forecast"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:crystal-ball"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data:
            value = self.coordinator.data.get("PriceForecastPercentage")
            if value is not None:
                return round(value * 100, 2)
        return None
