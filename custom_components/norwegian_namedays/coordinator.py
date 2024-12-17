"""Coordinator for Namedays integration."""
from datetime import timedelta
import logging
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)
API_URL = "https://webapi.no/api/v1/namedays"


class NamedaysUpdateCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch data from the Namedays API."""

    def __init__(self, hass, session):
        """Initialize the Namedays coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="Namedays Coordinator",
            update_interval=None,  # Ingen periodiske oppdateringer
        )
        self.session = session

    async def _async_update_data(self):
        """Fetch data from the API."""
        try:
            async with self.session.get(API_URL) as response:
                if response.status != 200:
                    raise Exception("Failed to fetch namedays data")

                data = await response.json()
                return data.get("data", [])  # Returner kun 'data'-noden fra APIet

        except Exception as e:
            _LOGGER.error(f"Error fetching namedays: {e}")
            raise
