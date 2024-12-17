"""Platform for Namedays sensor."""
from datetime import date,timedelta
from homeassistant.components.sensor import SensorEntity
from .const import DOMAIN
import logging
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Namedays sensor."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    async_add_entities([NamedaysSensor(coordinator)])


class NamedaysSensor(SensorEntity):
    """Representation of the Namedays Sensor."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self._name = "Namedays Today"
        self._state = None
        self._next_update = dt_util.now() - timedelta(minutes=1)
        self.update_today()

    def update_today(self):
        """Update today's names based on the stored API data."""
        if dt_util.now() > self._next_update:
            today = dt_util.now()
            for item in self.coordinator.data:
                if item.get("month") == today.month and item.get("day") == today.day:
                    self._state = ", ".join(item.get("names", []))
                    self._next_update = dt_util.start_of_local_day(dt_util.now() + timedelta(days=1))
                    _LOGGER.debug("Opddaterer sensoren %s. Neste oppdatering gjøres: %s",item.get("names",[]),self._next_update.isoformat())
                    return
            self._state = "No nameday"
            self._next_update = dt_util.start_of_local_day(dt_util.now() + timedelta(days=1))

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        return {
            "all_names": [item["names"] for item in self.coordinator.data],
        }

    async def async_update(self):
        """Update the sensor for the new day."""
        self.update_today()
