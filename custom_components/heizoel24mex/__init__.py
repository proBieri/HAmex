"""The HAmex integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.storage import Store
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util import dt as dt_util

from .api import HAmexApiClient, HAmexApiError
from .const import (
    DOMAIN,
    STORAGE_VERSION,
    UPDATE_INTERVAL,
    USAGE_IDLE_HOURS,
    VOLUME_CHANGE_TOLERANCE,
)

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up HAmex from a config entry."""
    session = async_get_clientsession(hass)
    client = HAmexApiClient(
        username=entry.data[CONF_USERNAME],
        password=entry.data[CONF_PASSWORD],
        session=session,
    )

    coordinator = HAmexDataUpdateCoordinator(hass, client, entry.entry_id)

    # Fetch initial data
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


class HAmexDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching HAmex data."""

    def __init__(self, hass: HomeAssistant, client: HAmexApiClient, entry_id: str) -> None:
        """Initialize."""
        self.client = client
        self._store: Store = Store(hass, STORAGE_VERSION, f"{DOMAIN}.{entry_id}.volume")
        # sensor_id -> {"volume": last significantly changed volume, "since": ISO timestamp}
        self._volume_anchors: dict[str, dict[str, Any]] | None = None

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=UPDATE_INTERVAL),
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            data = await self.client.get_dashboard_data()
        except HAmexApiError as err:
            raise UpdateFailed(f"Error communicating with API: {err}") from err

        await self._async_apply_idle_usage(data)
        return data

    async def _async_apply_idle_usage(self, data: dict[str, Any]) -> None:
        """Add EffectiveUsage per tank: 0 if the volume has not changed recently."""
        if not data or "Items" not in data:
            return

        if self._volume_anchors is None:
            self._volume_anchors = await self._store.async_load() or {}

        now = dt_util.utcnow()
        idle_after = timedelta(hours=USAGE_IDLE_HOURS)
        changed = False

        for tank in data["Items"]:
            volume = tank.get("CurrentVolume")
            if volume is None:
                tank["EffectiveUsage"] = tank.get("Usage")
                continue

            key = str(tank.get("SensorId"))
            anchor = self._volume_anchors.get(key)
            since = dt_util.parse_datetime(anchor["since"]) if anchor else None

            if since is None or abs(volume - anchor["volume"]) > VOLUME_CHANGE_TOLERANCE:
                anchor = {"volume": volume, "since": now.isoformat()}
                self._volume_anchors[key] = anchor
                since = now
                changed = True

            idle = now - since >= idle_after
            tank["VolumeUnchangedSince"] = anchor["since"]
            tank["UsageIdle"] = idle
            tank["EffectiveUsage"] = 0.0 if idle else tank.get("Usage")

        if changed:
            self._store.async_delay_save(lambda: self._volume_anchors, 10)
