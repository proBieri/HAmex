"""API client for HAmex integration."""
import asyncio
import logging
from typing import Any

import aiohttp
import async_timeout

from .const import API_LOGIN_URL, API_DASHBOARD_URL

_LOGGER = logging.getLogger(__name__)


class HAmexApiError(Exception):
    """Base exception for HAmex API errors."""


class HAmexAuthError(HAmexApiError):
    """Authentication error."""


class HAmexApiClient:
    """API client for Heizoel24 MEX dashboard."""

    def __init__(self, username: str, password: str, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._username = username
        self._password = password
        self._session = session
        self._authenticated = False

    async def authenticate(self) -> bool:
        """Authenticate with the API using cookie-based session."""
        try:
            async with async_timeout.timeout(10):
                response = await self._session.post(
                    API_LOGIN_URL,
                    json={
                        "Login": {
                            "UserName": self._username,
                            "Password": self._password,
                        }
                    },
                )

                if response.status == 401:
                    raise HAmexAuthError("Invalid username or password")

                response.raise_for_status()
                data = await response.json()

                # Check if login was successful
                if not data.get("Success"):
                    _LOGGER.error("Login failed: %s", data)
                    raise HAmexAuthError("Login failed")

                self._authenticated = True
                _LOGGER.debug("Successfully authenticated")
                return True

        except aiohttp.ClientError as err:
            _LOGGER.error("Connection error during authentication: %s", err)
            raise HAmexApiError(f"Connection error: {err}") from err
        except asyncio.TimeoutError as err:
            _LOGGER.error("Timeout during authentication")
            raise HAmexApiError("Timeout during authentication") from err

    async def get_dashboard_data(self) -> dict[str, Any]:
        """Get dashboard data from the API."""
        if not self._authenticated:
            await self.authenticate()

        try:
            async with async_timeout.timeout(10):
                response = await self._session.get(API_DASHBOARD_URL)

                if response.status == 401:
                    # Session expired, try to re-authenticate
                    _LOGGER.debug("Session expired, re-authenticating")
                    await self.authenticate()

                    # Retry with new session
                    response = await self._session.get(API_DASHBOARD_URL)

                response.raise_for_status()
                data = await response.json()

                _LOGGER.debug("Successfully retrieved dashboard data")
                return data

        except aiohttp.ClientError as err:
            _LOGGER.error("Connection error while fetching data: %s", err)
            raise HAmexApiError(f"Connection error: {err}") from err
        except asyncio.TimeoutError as err:
            _LOGGER.error("Timeout while fetching data")
            raise HAmexApiError("Timeout while fetching data") from err
