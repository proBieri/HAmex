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
from homeassistant.helpers.entity import DeviceInfo
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
            tank_id = tank.get("TankId")

            # Current volume percentage
            entities.append(
                HAmexTankPercentageSensor(coordinator, sensor_id, tank_id, tank_name, entry)
            )

            # Current volume in liters
            entities.append(
                HAmexTankVolumeSensor(coordinator, sensor_id, tank_id, tank_name, entry)
            )

            # Battery percentage
            entities.append(
                HAmexBatterySensor(coordinator, sensor_id, tank_id, tank_name, entry)
            )

            # Usage rate
            entities.append(
                HAmexUsageSensor(coordinator, sensor_id, tank_id, tank_name, entry)
            )

            # Remaining days
            entities.append(
                HAmexRemainingDaysSensor(coordinator, sensor_id, tank_id, tank_name, entry)
            )

        # Add total/summary sensors (virtual device)
        if len(coordinator.data["Items"]) > 0:
            entities.append(HAmexTotalVolumeSensor(coordinator, entry))
            entities.append(HAmexTotalPercentageSensor(coordinator, entry))
            entities.append(HAmexTotalUsageSensor(coordinator, entry))
            entities.append(HAmexTotalRemainingDaysSensor(coordinator, entry))

        # Add price sensors to virtual device
        if "PriceComparedToYesterdayPercentage" in coordinator.data:
            entities.append(HAmexPriceComparisonSensor(coordinator, entry))

        if "PriceForecastPercentage" in coordinator.data:
            entities.append(HAmexPriceForecastSensor(coordinator, entry))

    async_add_entities(entities)


def _get_tank_device_info(tank_id: int, tank_name: str, entry: ConfigEntry) -> DeviceInfo:
    """Get device info for a tank."""
    return DeviceInfo(
        identifiers={(DOMAIN, f"tank_{tank_id}")},
        name=tank_name,
        manufacturer="Heizoel24",
        model="MEX Sensor",
        via_device=(DOMAIN, entry.entry_id),
    )


def _get_summary_device_info(entry: ConfigEntry) -> DeviceInfo:
    """Get device info for the summary/total device."""
    return DeviceInfo(
        identifiers={(DOMAIN, f"summary_{entry.entry_id}")},
        name="Heizöl Gesamt",
        manufacturer="Heizoel24",
        model="MEX Summary",
        via_device=(DOMAIN, entry.entry_id),
    )


# =============================================================================
# Tank Sensors (individual devices)
# =============================================================================


class HAmexTankPercentageSensor(CoordinatorEntity, SensorEntity):
    """Sensor for tank fill percentage."""

    def __init__(
        self,
        coordinator: HAmexDataUpdateCoordinator,
        sensor_id: int,
        tank_id: int,
        tank_name: str,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._tank_id = tank_id
        self._tank_name = tank_name
        self._attr_name = "Füllstand"
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}_percentage"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:gauge"
        self._attr_device_info = _get_tank_device_info(tank_id, tank_name, entry)

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
        tank_id: int,
        tank_name: str,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._tank_id = tank_id
        self._tank_name = tank_name
        self._attr_name = "Volumen"
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}_volume"
        self._attr_native_unit_of_measurement = UnitOfVolume.LITERS
        self._attr_device_class = SensorDeviceClass.VOLUME
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:oil-temperature"
        self._attr_device_info = _get_tank_device_info(tank_id, tank_name, entry)

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
        tank_id: int,
        tank_name: str,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._tank_id = tank_id
        self._tank_name = tank_name
        self._attr_name = "Batterie"
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}_battery"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_device_info = _get_tank_device_info(tank_id, tank_name, entry)

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
        tank_id: int,
        tank_name: str,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._tank_id = tank_id
        self._tank_name = tank_name
        self._attr_name = "Verbrauch"
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}_usage"
        self._attr_native_unit_of_measurement = "L/Tag"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:chart-line"
        self._attr_device_info = _get_tank_device_info(tank_id, tank_name, entry)

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
        tank_id: int,
        tank_name: str,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._sensor_id = sensor_id
        self._tank_id = tank_id
        self._tank_name = tank_name
        self._attr_name = "Reichweite"
        self._attr_unique_id = f"{DOMAIN}_{sensor_id}_remaining_days"
        self._attr_native_unit_of_measurement = "Tage"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:calendar-clock"
        self._attr_device_info = _get_tank_device_info(tank_id, tank_name, entry)

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


# =============================================================================
# Total/Summary Sensors (virtual device)
# =============================================================================


class HAmexTotalVolumeSensor(CoordinatorEntity, SensorEntity):
    """Sensor for total volume across all tanks."""

    def __init__(
        self,
        coordinator: HAmexDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Gesamtvolumen"
        self._attr_unique_id = f"{DOMAIN}_total_volume"
        self._attr_native_unit_of_measurement = UnitOfVolume.LITERS
        self._attr_device_class = SensorDeviceClass.VOLUME
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:oil-temperature"
        self._attr_device_info = _get_summary_device_info(entry)

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or "Items" not in self.coordinator.data:
            return None

        total = sum(tank.get("CurrentVolume", 0) for tank in self.coordinator.data["Items"])
        return total if total > 0 else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data or "Items" not in self.coordinator.data:
            return {}

        total_max = sum(tank.get("MaxVolume", 0) for tank in self.coordinator.data["Items"])
        tank_count = len(self.coordinator.data["Items"])

        return {
            "max_volume": total_max,
            "tank_count": tank_count,
        }


class HAmexTotalPercentageSensor(CoordinatorEntity, SensorEntity):
    """Sensor for total fill percentage across all tanks."""

    def __init__(
        self,
        coordinator: HAmexDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Gesamtfüllstand"
        self._attr_unique_id = f"{DOMAIN}_total_percentage"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:gauge"
        self._attr_device_info = _get_summary_device_info(entry)

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or "Items" not in self.coordinator.data:
            return None

        total_volume = sum(tank.get("CurrentVolume", 0) for tank in self.coordinator.data["Items"])
        total_max = sum(tank.get("MaxVolume", 1) for tank in self.coordinator.data["Items"])

        if total_max == 0:
            return None

        percentage = (total_volume / total_max) * 100
        return round(percentage, 1)


class HAmexTotalUsageSensor(CoordinatorEntity, SensorEntity):
    """Sensor for total daily usage across all tanks."""

    def __init__(
        self,
        coordinator: HAmexDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Gesamtverbrauch"
        self._attr_unique_id = f"{DOMAIN}_total_usage"
        self._attr_native_unit_of_measurement = "L/Tag"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:chart-line"
        self._attr_device_info = _get_summary_device_info(entry)

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or "Items" not in self.coordinator.data:
            return None

        # Sum usage from all tanks (they all report the same usage rate)
        # We take the first tank's usage as it represents the combined system
        first_tank = self.coordinator.data["Items"][0]
        usage = first_tank.get("Usage")

        if usage:
            return round(usage, 2)
        return None


class HAmexTotalRemainingDaysSensor(CoordinatorEntity, SensorEntity):
    """Sensor for estimated remaining days based on total capacity."""

    def __init__(
        self,
        coordinator: HAmexDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Gesamtreichweite"
        self._attr_unique_id = f"{DOMAIN}_total_remaining_days"
        self._attr_native_unit_of_measurement = "Tage"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:calendar-clock"
        self._attr_device_info = _get_summary_device_info(entry)

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        if not self.coordinator.data or "Items" not in self.coordinator.data:
            return None

        total_volume = sum(tank.get("CurrentVolume", 0) for tank in self.coordinator.data["Items"])

        # Use usage rate from first tank (represents system usage)
        first_tank = self.coordinator.data["Items"][0]
        usage = first_tank.get("Usage", 0)

        if usage > 0:
            remaining_days = int(total_volume / usage)
            return remaining_days
        return None


class HAmexPriceComparisonSensor(CoordinatorEntity, SensorEntity):
    """Sensor for price comparison to yesterday."""

    def __init__(
        self,
        coordinator: HAmexDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Preis Vergleich"
        self._attr_unique_id = f"{DOMAIN}_price_comparison"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:chart-line-variant"
        self._attr_device_info = _get_summary_device_info(entry)

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

    def __init__(
        self,
        coordinator: HAmexDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Preis Prognose"
        self._attr_unique_id = f"{DOMAIN}_price_forecast"
        self._attr_native_unit_of_measurement = PERCENTAGE
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_icon = "mdi:crystal-ball"
        self._attr_device_info = _get_summary_device_info(entry)

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        if self.coordinator.data:
            value = self.coordinator.data.get("PriceForecastPercentage")
            if value is not None:
                return round(value * 100, 2)
        return None
